import pdb
import math
from libs.highlight.file import HLFile
from libs.highlight.grammar import Grammar
from libs.highlight.tokens import TokenList


class HighLighter:
    SPACE = " "
    HTAB = "\t"
    VTAB = "\v"
    NLINE = "\n"
    CR = "\r"
    FEED = "\f"
    TAB_LEN = 4

    def __init__(self, file:HLFile):   
        self._file = file
      
    # @staticmethod
    # def issymbol(c: str) -> bool:
    #     return c in "=[]{}().+-*/><||:;_,"

    # @property
    # def tokens(self):
    #     return self._tokens
    
    @staticmethod
    def _white_to_tabs(white: int) -> str:
        tabs = math.floor(white / HighLighter.TAB_LEN)
        spaces = white % HighLighter.TAB_LEN
        return "".join(HighLighter.HTAB * tabs) + "".join(HighLighter.SPACE * spaces)

    def tokenize(self, line: str)-> TokenList:
        white = 0
        words = TokenList(self._file.grammar)
        idx: int = 0
        while idx < len(line):
            chr: str = line[idx]
            if self._file.grammar.is_comment_symbol(chr, self._file.type):
                words.append(line[idx:])
                idx = len(line)
                continue
            if chr.isspace():
                words.flush()
                white += 1
            else:
                if white > 0:
                    words.append(type(self)._white_to_tabs(white))
                    white = 0
                if self._file.grammar.is_symbol(chr):
                # if self.tokens.grammar.is_symbol(chr):
                    # pdb.set_trace()
                    words.flush()
                    words.append(chr)
                elif chr.isalpha() or chr.isalnum():
                    words.word += chr
            idx += 1
        words.flush()
        return words

    def process_file(self):
        program = []
        with open(self._file.filename) as file:
            for line in file:
                tk = self.tokenize(line)
                tk.enriched = True
                program.append(tk)
        return program