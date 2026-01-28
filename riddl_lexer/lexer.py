"""
RIDDL Language Lexer for Pygments

Provides syntax highlighting for RIDDL specifications. Token patterns are
derived from the VS Code extension's TextMate grammar for consistency.
"""

import re
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import (
    Comment, String, Keyword, Name, Number, Operator, Punctuation, Text,
    Generic
)

__all__ = ['RiddlLexer']


class RiddlLexer(RegexLexer):
    """
    Lexer for the RIDDL (Reactive Interface to Domain Definition Language).

    RIDDL is a specification language for defining reactive, distributed
    systems using Domain-Driven Design concepts.
    """

    name = 'RIDDL'
    aliases = ['riddl']
    filenames = ['*.riddl']
    mimetypes = ['text/x-riddl']
    flags = re.MULTILINE

    # Definition keywords - major structural elements
    DEFINITION_KEYWORDS = (
        'adaptor', 'application', 'author', 'case', 'command', 'connector',
        'constant', 'context', 'domain', 'entity', 'epic', 'event',
        'field', 'flow', 'function', 'graph', 'group', 'handler', 'inlet',
        'input', 'invariant', 'merge', 'module', 'nebula', 'outlet',
        'output', 'pipe', 'plant', 'projector', 'query', 'record',
        'relationship', 'replica', 'repository', 'result', 'router', 'saga',
        'sink', 'source', 'split', 'state', 'step', 'streamlet', 'table',
        'term', 'type', 'user', 'void',
    )

    # Control flow keywords
    CONTROL_KEYWORDS = (
        'become', 'call', 'do', 'else', 'error', 'execute', 'for',
        'foreach', 'if', 'match', 'morph', 'on', 'return', 'reverted',
        'send', 'set', 'stop', 'take', 'tell', 'then', 'when',
    )

    # Import/include keywords
    IMPORT_KEYWORDS = (
        'import', 'include',
    )

    # Other keywords
    OTHER_KEYWORDS = (
        'acquires', 'all', 'any', 'append', 'attachment', 'benefit',
        'body', 'brief', 'briefly', 'capability', 'commands', 'condition',
        'container', 'contains', 'create', 'described', 'description',
        'details', 'direct', 'email', 'end', 'example', 'explained',
        'explanation', 'file', 'focus', 'fully', 'index', 'init', 'inlets',
        'items', 'label', 'link', 'many', 'mapping', 'message', 'name',
        'one', 'option', 'optional', 'options', 'organization', 'other',
        'outlets', 'parallel', 'presents', 'range', 'reference', 'remove',
        'reply', 'required', 'requires', 'results', 'returns', 'schema',
        'selects', 'sequence', 'show', 'shown', 'story', 'title', 'updates',
        'url', 'value', 'where',
    )

    # Readability words - prepositions and connectors
    READABILITY_WORDS = (
        'and', 'are', 'as', 'at', 'by', 'for', 'from', 'in', 'is', 'of',
        'or', 'so', 'that', 'to', 'wants', 'with',
    )

    # Predefined types (both CamelCase and lowercase variants)
    PREDEFINED_TYPES = (
        'Abstract', 'Blob', 'Boolean', 'Currency', 'Current', 'Date',
        'DateTime', 'Decimal', 'Duration', 'Id', 'Integer', 'Length',
        'List', 'Location', 'Luminosity', 'Map', 'Mapping', 'Mass', 'Mole',
        'Natural', 'Nothing', 'Number', 'Pattern', 'Range', 'Real', 'Sequence',
        'Set', 'String', 'Temperature', 'Time', 'Timestamp', 'TimeStamp',
        'Unknown', 'URI', 'URL', 'UserId', 'UUID', 'Whole', 'ZonedDate',
        'ZonedDateTime',
    )

    # Common option values (hyphenated identifiers that should be highlighted)
    OPTION_VALUES = (
        'event-sourced', 'finite-state-machine', 'message-queue',
        'value-object', 'aggregate', 'transient', 'available',
        'device', 'kind', 'css', 'faicon', 'technology', 'persistent',
    )

    tokens = {
        'root': [
            # Comments
            (r'//.*$', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline-comment'),

            # Triple-quoted code blocks (embedded code)
            (r'```', String.Doc, 'code-block'),

            # Markdown documentation lines (| followed by content to end of line)
            # Must check before whitespace rule consumes leading spaces
            (r'\|[^\n]*', String.Doc),

            # Strings
            (r'"', String.Double, 'string'),

            # Undefined placeholder
            (r'\?\?\?', Generic.Error),

            # Option values (hyphenated identifiers - match before keywords)
            (words(OPTION_VALUES, prefix=r'\b', suffix=r'\b'),
             Name.Constant),

            # Keywords - definitions (purple in dark theme)
            (words(DEFINITION_KEYWORDS, prefix=r'\b', suffix=r'\b'),
             Keyword.Declaration),

            # Keywords - control flow
            (words(CONTROL_KEYWORDS, prefix=r'\b', suffix=r'\b'),
             Keyword),

            # Keywords - imports
            (words(IMPORT_KEYWORDS, prefix=r'\b', suffix=r'\b'),
             Keyword.Namespace),

            # Keywords - other
            (words(OTHER_KEYWORDS, prefix=r'\b', suffix=r'\b'),
             Keyword.Reserved),

            # Readability words (yellow in dark theme)
            (words(READABILITY_WORDS, prefix=r'\b', suffix=r'\b'),
             Keyword.Pseudo),

            # Predefined types (support types)
            (words(PREDEFINED_TYPES, prefix=r'\b', suffix=r'\b'),
             Name.Builtin),

            # Numbers
            (r'\b[0-9]+(\.[0-9]+)?\b', Number),

            # Operators
            (r'[=+?*@]', Operator),

            # Punctuation - braces (teal in dark theme)
            (r'[{}]', Punctuation),
            (r'[()]', Punctuation),
            (r'[\[\]]', Punctuation),
            (r'[,:]', Punctuation),
            (r'\.', Punctuation),

            # Identifiers (may contain hyphens, e.g., event-sourced)
            (r'\b[a-zA-Z_][a-zA-Z0-9_-]*\b', Name),

            # Whitespace
            (r'\s+', Text),
        ],

        'multiline-comment': [
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^*]+', Comment.Multiline),
            (r'\*', Comment.Multiline),
        ],

        'string': [
            (r'\\.', String.Escape),
            (r'"', String.Double, '#pop'),
            (r'[^"\\]+', String.Double),
        ],

        'code-block': [
            (r'```', String.Doc, '#pop'),
            (r'[^`]+', String.Doc),
            (r'`', String.Doc),
        ],
    }