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

    # Definition keywords - major structural elements.
    #
    # Kept in step with riddl's Keywords.scala and the published EBNF grammar
    # (docs/riddl/references/riddl-grammar.ebnf) for RIDDL 2.0.
    #
    # `processor` is the 2.0 keyword for every streaming processor; the
    # dedicated shape keywords (source/sink/flow/merge/split/router) still
    # parse but are deprecated, so they stay highlighted. `application`,
    # `external`, `gateway` and `service` are the context intention prefixes.
    # `version` and `copyright` are leaf definitions as of 2.0.
    DEFINITION_KEYWORDS = (
        'adaptor', 'application', 'author', 'case', 'command', 'connector',
        'constant', 'context', 'copyright', 'domain', 'entity', 'epic',
        'event', 'external', 'field', 'flow', 'function', 'gateway', 'graph',
        'group', 'handler', 'inlet', 'input', 'invariant', 'merge', 'module',
        'nebula', 'outlet', 'output', 'pipe', 'plant', 'processor',
        'projector', 'query', 'record', 'relationship', 'replica',
        'repository', 'result', 'router', 'saga', 'service', 'sink',
        'source', 'split', 'state', 'step', 'streamlet', 'table', 'term',
        'type', 'user', 'version', 'void',
    )

    # Control flow and statement keywords.
    #
    # New in 2.0: `foreach` (bounded iteration), `put`/`return` (boundary and
    # function value statements), `yield` (deprecating `reply`), `get` and
    # `call` (value expressions), and `default` for a match's fallback case.
    # `initial` marks the starting state or handler of an entity.
    CONTROL_KEYWORDS = (
        'become', 'call', 'default', 'do', 'else', 'error', 'execute', 'for',
        'foreach', 'get', 'if', 'initial', 'let', 'match', 'morph', 'on',
        'put', 'return', 'reverted', 'send', 'set', 'stop', 'take', 'tell',
        'then', 'when', 'yield',
    )

    # Boolean-expression operators and literals, new in 2.0. These are
    # context-sensitive in the parser -- legal identifiers everywhere except
    # inside a boolean expression -- so highlighting them is a best-effort
    # convenience, not a guarantee of meaning.
    BOOLEAN_KEYWORDS = (
        'false', 'not', 'true',
    )

    # Import/include keywords
    IMPORT_KEYWORDS = (
        'import', 'include',
    )

    # Other keywords, including the UI element aliases and interaction verbs.
    #
    # New in 2.0: `yields` (a command's or query's declared response),
    # `figma`/`node` (a design reference), `refuses` (an interaction step),
    # `activate`/`passivate` (entity lifecycle on-clauses), and the selection
    # and entry verbs `chooses`/`picks`/`enters`/`provides`.
    OTHER_KEYWORDS = (
        'accepts', 'acquires', 'activate', 'activates', 'admits', 'all',
        'animation', 'any', 'append', 'attachment', 'benefit', 'block',
        'body', 'brief', 'briefly', 'button', 'capability', 'chooses',
        'column', 'commands', 'condition', 'container', 'contains', 'create',
        'described', 'description', 'details', 'dialog', 'direct',
        'displays', 'document', 'email', 'emits', 'end', 'enters', 'example',
        'explained', 'explanation', 'figma', 'file', 'focus', 'form',
        'frame', 'fully', 'index', 'init', 'initiates', 'inlets', 'item',
        'items', 'label', 'link', 'many', 'mapping', 'menu', 'message',
        'name', 'node', 'one', 'option', 'optional', 'options',
        'organization', 'other', 'outlets', 'page', 'pane', 'parallel',
        'passivate', 'picklist', 'picks', 'picture', 'popup', 'presents',
        'provides', 'range', 'reads', 'reference', 'refuses', 'remove',
        'reply', 'required', 'requires', 'results', 'returns', 'schema',
        'section', 'selector', 'selects', 'sequence', 'show', 'shown',
        'shows', 'starts', 'story', 'submits', 'tab', 'title', 'triggers',
        'updates', 'url', 'value', 'where', 'window', 'writes', 'yields',
    )

    # Readability words - prepositions, connectors, and the user-story modal
    # verbs. 2.0 widened the user-story verb from `wants` alone to the modal
    # set {wants, must, shall, should, may, will, can}.
    READABILITY_WORDS = (
        'and', 'are', 'as', 'at', 'by', 'can', 'for', 'from', 'in', 'is',
        'may', 'must', 'of', 'or', 'shall', 'should', 'so', 'that', 'to',
        'wants', 'will', 'with',
    )

    # Streamlet shapes usable in an `as <shape>` ascription, including the
    # synonyms cascade (flow), fanin (merge), and broadcast/fanout (split).
    # The canonical names also appear in DEFINITION_KEYWORDS as the
    # deprecated standalone keywords, so only the synonyms are listed here.
    SHAPE_SYNONYMS = (
        'broadcast', 'cascade', 'fanin', 'fanout',
    )

    # Predefined types (both CamelCase and lowercase variants).
    #
    # 2.0 renamed `Abstract` to `Anything` -- the type assignment-compatible
    # with everything in both directions. `Abstract` still parses and emits a
    # deprecation, so both are highlighted.
    PREDEFINED_TYPES = (
        'Abstract', 'Anything', 'Blob', 'Boolean', 'Currency', 'Current',
        'Date', 'DateTime', 'Decimal', 'Duration', 'Id', 'Integer', 'Length',
        'List', 'Location', 'Luminosity', 'Map', 'Mapping', 'Mass', 'Mole',
        'Natural', 'Nothing', 'Number', 'Pattern', 'Range', 'Real', 'Sequence',
        'Set', 'String', 'Temperature', 'Time', 'Timestamp', 'TimeStamp',
        'Unknown', 'URI', 'URL', 'UserId', 'UUID', 'Whole', 'ZonedDate',
        'ZonedDateTime',
    )

    # Common option values (hyphenated identifiers that should be highlighted).
    #
    # 2.0's option registry consolidation registered several options that were
    # advertised but never recognized -- the entity markers, `css`, and the
    # saga and portlet options below among them.
    OPTION_VALUES = (
        'event-sourced', 'finite-state-machine', 'message-queue',
        'value-object', 'aggregate', 'transient', 'available',
        'device', 'kind', 'css', 'faicon', 'technology', 'persistent',
        'async', 'auto-id', 'compensate', 'consistent', 'ordered',
        'parallel', 'protocol', 'sync', 'unordered', 'value',
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

            # Boolean operators and literals (2.0 boolean expressions)
            (words(BOOLEAN_KEYWORDS, prefix=r'\b', suffix=r'\b'),
             Keyword),

            # Streamlet shape synonyms usable in `as <shape>`
            (words(SHAPE_SYNONYMS, prefix=r'\b', suffix=r'\b'),
             Keyword.Declaration),

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

            # Comparison operators. First-class syntax as of 2.0's boolean
            # expressions (`when total >= Minimum`, `case != Cancelled`), so
            # they must be matched before the single-character rule below --
            # otherwise `>=` splits into an unrecognised `>` and an `=`.
            (r'==|!=|<=|>=|<|>', Operator),

            # Operators. `!` is the negation form of a bare `when !flag`.
            (r'[=+?*@!]', Operator),

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