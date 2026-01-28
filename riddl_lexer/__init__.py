"""
RIDDL Language Lexer for Pygments

This module provides syntax highlighting for RIDDL (Reactive Interface to
Domain Definition Language) files in MkDocs and other Pygments-based tools.
"""

from .lexer import RiddlLexer
from .style import RiddlStyle

__all__ = ['RiddlLexer', 'RiddlStyle']
__version__ = '1.0.0'