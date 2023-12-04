from pathlib import Path

from libs.highlight.grammar import Grammar
from libs.highlight.languages.go import GoGrammar
from libs.highlight.languages.python import PythonGrammar
from libs.highlight.languages.ruby import RubyGrammar
from libs.highlight.languages.typescript import TypescriptGrammar



class HLFile():
    def __init__(self, filename):
        self._filename = filename
        self._type = Path(self.filename).suffix[1:]
        
    @property
    def filename(self):
        return self._filename
    
    @property
    def type(self):
        if self._type == 'rb':
            return "Ruby"
        if self._type == 'go':
            return "Go"
        if self._type == 'ts':
            return "Typescript"
        if self._type == 'py':
            return "Python"
    
    @property
    def grammar(self)-> Grammar:
        if self._type == 'rb':
            return RubyGrammar()
        if self._type == 'go':
            return GoGrammar()
        if self._type == 'ts':
            return TypescriptGrammar()
        if self._type == 'py':
            return PythonGrammar()
        
        # raise GrammarException()