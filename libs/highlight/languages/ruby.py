from libs.highlight.grammar import Grammar
import pdb


class RubyGrammar(Grammar):
    RESERVED_WORDS = [
        "self",
        "super",
        "alias",
        "and",
        "begin",
        "BEGIN",
        "break",
        "case",
        "class",
        "defined",
        "do",
        "else",
        "elsif",
        "end",
        "END",
        "ensure",
        "for",
        "if",
        "in",
        "module",
        "next",
        "not",
        "or",
        "redo",
        "require",
        "rescue",
        "retry",
        "return",
        "then",
        "undef",
        "unless",
        "until",
        "when",
        "while",
        "yield",
        "include",
        "extend",
        "prepend",
        "public",
        "private",
        "protected",
        "raise",
        "throw",
        "def",
    ]
    BUILT_INS = [
        "proc",
        "lambda",
        "attr_accessor",
        "attr_reader",
        "attr_writer",
        "define_method",
        "private_constant",
        "module_function",
    ]
    TYPES = []
    LITERALS = ["true", "false", "nil"]

    