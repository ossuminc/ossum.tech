"""
RIDDL Color Style for Pygments

Provides a color scheme matching the RIDDL IntelliJ plugin and VS Code extension.
"""

from pygments.style import Style
from pygments.token import (
    Token, Comment, String, Keyword, Name, Number, Operator, Punctuation,
    Text, Generic, Error
)

__all__ = ['RiddlStyle']


class RiddlStyle(Style):
    """
    Color scheme for RIDDL syntax highlighting.

    Colors are derived from the RIDDL IntelliJ plugin color scheme:
    - Keywords: burnt orange (#fa8b61)
    - Readability words: yellow (#b3ae60)
    - Predefined types: teal (#19c4bf)
    - Punctuation: teal (#0da19e)
    - Strings: sage green (#87a875)
    - Comments: sage green (#87a875)
    - Numbers: blue (#6897bb)
    """

    name = 'riddl'

    # Background and default colors (Darcula-like dark theme)
    background_color = '#2b2b2b'
    default_style = '#a9b7c6'

    styles = {
        # Comments - gray
        Comment: '#808080 italic',
        Comment.Single: '#808080 italic',
        Comment.Multiline: '#808080 italic',

        # Strings - bright green
        String: '#98c379',
        String.Double: '#98c379',
        String.Escape: '#e0be35',
        # Markdown docs - dimmer green
        String.Doc: '#629755 italic',

        # Keywords - burnt orange (main RIDDL keywords)
        Keyword: '#fa8b61',
        Keyword.Declaration: '#fa8b61',  # domain, context, entity, etc.
        Keyword.Namespace: '#fa8b61',    # include, import
        Keyword.Reserved: '#fa8b61',     # other keywords
        Keyword.Constant: '#fa8b61',

        # Readability words - yellow (is, of, by, to, with, etc.)
        Keyword.Pseudo: '#b3ae60',

        # Predefined types - teal/cyan
        Name.Builtin: '#19c4bf',

        # Option values (event-sourced, aggregate, etc.) - green
        Name.Constant: '#57d07c',

        # Identifiers - default text color
        Name: '#a9b7c6',
        Name.Class: '#a9b7c6',
        Name.Function: '#a9b7c6',

        # Numbers - blue
        Number: '#6897bb',

        # Operators
        Operator: '#a9b7c6',

        # Punctuation - teal
        Punctuation: '#0da19e',

        # Errors
        Error: '#c41919',
        Generic.Error: '#c41919',

        # Default text
        Text: '#a9b7c6',
    }
