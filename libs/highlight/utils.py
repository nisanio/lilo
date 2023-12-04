from libs.highlight.languages.go import GoGrammar
from libs.highlight.languages.python import PythonGrammar
from libs.highlight.languages.ruby import RubyGrammar
from libs.highlight.languages.typescript import TypescriptGrammar

GRAMMARS = {
    "rb": RubyGrammar,
    "go": GoGrammar,
    "py": PythonGrammar,
    "ts": TypescriptGrammar,
}

LANGUAGES = {"rb": "ruby", "go": "go", "py": "python", "ts": "typescript"}