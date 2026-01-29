#!/usr/bin/env python3
"""
Hugo to MkDocs Migration Script

Converts Hugo-formatted Markdown files to MkDocs Material format:
1. Copies .md files from source to destination
2. Renames _index.md to index.md
3. Converts {{< relref "..." >}} to relative links
4. Converts {{< hint type=X >}} to !!! X admonitions
5. Strips {{< toc >}} and {{< toc-tree >}}
6. Cleans frontmatter (removes type, normalizes draft)
"""

import os
import re
import sys
import shutil
from pathlib import Path
from typing import Optional


def convert_relref(match: re.Match, current_file: Path, source_root: Path) -> str:
    """Convert Hugo relref shortcode to relative markdown link."""
    ref_path = match.group(1).strip('"\'')

    # Remove any leading ../ and normalize
    ref_path = ref_path.lstrip('./')

    # Handle various path formats
    if ref_path.startswith('../'):
        # Keep relative paths as-is but convert to .md
        parts = ref_path.split('/')
        # Convert to proper relative path
        result = ref_path
    else:
        # Simple reference - convert to relative path
        result = ref_path

    # Ensure .md extension
    if not result.endswith('.md'):
        # Check if it's a directory reference (should become index.md)
        if '/' in result or not '.' in result.split('/')[-1]:
            if not result.endswith('/'):
                result += '/'
            result += 'index.md'
        else:
            result += '.md'

    # Replace _index.md with index.md
    result = result.replace('_index.md', 'index.md')

    return result


def convert_hint_to_admonition(match: re.Match) -> str:
    """Convert Hugo hint shortcode to MkDocs admonition."""
    hint_type = match.group(1)
    # Map Hugo hint types to MkDocs admonition types
    type_map = {
        'note': 'note',
        'info': 'info',
        'warning': 'warning',
        'danger': 'danger',
        'tip': 'tip',
        'important': 'warning',
    }
    admon_type = type_map.get(hint_type, 'note')
    return f'!!! {admon_type}'


def clean_frontmatter(content: str) -> str:
    """Clean and normalize YAML frontmatter."""
    # Match frontmatter block
    fm_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    match = fm_pattern.match(content)

    if not match:
        return content

    frontmatter = match.group(1)
    rest = content[match.end():]

    # Parse frontmatter lines
    lines = frontmatter.split('\n')
    new_lines = []

    for line in lines:
        # Skip 'type' field
        if line.strip().startswith('type:'):
            continue
        # Skip 'date' field (Hugo-specific)
        if line.strip().startswith('date:'):
            continue
        # Normalize draft field
        if line.strip().startswith('draft:'):
            if 'true' in line.lower():
                new_lines.append('draft: true')
            # Skip if draft: false (no need to include)
            continue
        # Keep other fields
        if line.strip():
            new_lines.append(line)

    if new_lines:
        return '---\n' + '\n'.join(new_lines) + '\n---\n\n' + rest.lstrip()
    else:
        return rest.lstrip()


def convert_file(source_path: Path, dest_path: Path, source_root: Path) -> None:
    """Convert a single Hugo markdown file to MkDocs format."""
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean frontmatter
    content = clean_frontmatter(content)

    # 2. Convert {{< relref "..." >}} to relative links
    # Pattern matches: [text]({{< relref "path" >}})
    relref_pattern = re.compile(r'\{\{<\s*relref\s+["\']?([^"\'}>]+)["\']?\s*>\}\}')
    content = relref_pattern.sub(
        lambda m: convert_relref(m, source_path, source_root),
        content
    )

    # 3. Convert {{< hint type=X >}} to !!! X
    hint_start_pattern = re.compile(r'\{\{<\s*hint\s+type=(\w+)\s*>\}\}')
    content = hint_start_pattern.sub(convert_hint_to_admonition, content)

    # Remove {{< /hint >}} end tags
    content = re.sub(r'\{\{<\s*/hint\s*>\}\}', '', content)

    # 4. Strip {{< toc >}} and {{< toc-tree >}}
    content = re.sub(r'\{\{<\s*toc\s*>\}\}', '', content)
    content = re.sub(r'\{\{<\s*toc-tree\s*>\}\}', '', content)

    # 5. Clean up any remaining Hugo shortcodes (warn about them)
    remaining = re.findall(r'\{\{<.*?>\}\}', content)
    if remaining:
        print(f"  Warning: Remaining shortcodes in {source_path}: {remaining}")

    # 6. Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Ensure parent directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)


def migrate_directory(source_dir: Path, dest_dir: Path, source_root: Optional[Path] = None) -> int:
    """Migrate all markdown files from source to destination."""
    if source_root is None:
        source_root = source_dir

    file_count = 0

    for source_path in source_dir.rglob('*.md'):
        # Calculate relative path
        rel_path = source_path.relative_to(source_dir)

        # Rename _index.md to index.md
        parts = list(rel_path.parts)
        if parts[-1] == '_index.md':
            parts[-1] = 'index.md'

        # Convert camelCase filenames to kebab-case
        new_name = parts[-1]
        if new_name != 'index.md':
            # Convert camelCase to kebab-case
            new_name = re.sub(r'([a-z])([A-Z])', r'\1-\2', new_name).lower()
            parts[-1] = new_name

        dest_path = dest_dir / Path(*parts)

        print(f"  {source_path.name} -> {dest_path.relative_to(dest_dir)}")
        convert_file(source_path, dest_path, source_root)
        file_count += 1

    return file_count


def main():
    if len(sys.argv) < 3:
        print("Usage: migrate-hugo.py <source_dir> <dest_dir>")
        print()
        print("Example:")
        print("  migrate-hugo.py ../riddl/doc/src/main/hugo/content/tutorial/ docs/riddl/tutorials/")
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    dest_dir = Path(sys.argv[2])

    if not source_dir.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        sys.exit(1)

    print(f"Migrating Hugo content from: {source_dir}")
    print(f"                        to: {dest_dir}")
    print()

    file_count = migrate_directory(source_dir, dest_dir)

    print()
    print(f"Migrated {file_count} files successfully.")
    print()
    print("Next steps:")
    print("  1. Review converted files for any remaining issues")
    print("  2. Update mkdocs.yml navigation")
    print("  3. Run 'mkdocs serve' to verify rendering")


if __name__ == '__main__':
    main()
