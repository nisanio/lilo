import pdb


class Grammar:
    TYPES = []
    SYMBOLS = "=[]{}().+-*/><||:;_,"
    RESERVED_WORDS = []
    LITERALS = []
    BUILT_INS = []
    COMMENT_SYMBOLS = {"Ruby": "#", "Go": "//", "Typescript": "//", "Python": "#"}
    

    @property
    def comment_symbols(self):
        return Grammar.COMMENT_SYMBOLS
    
    def _is_type(self, word: str) -> bool:
        return word in type(self).TYPES

    def _is_reserved_word(self, word: str) -> bool:
        return word in type(self).RESERVED_WORDS

    def _is_literal(self, word: str) -> bool:
        return word in type(self).LITERALS

    def _is_built_in(self, word: str) -> bool:
        return word in type(self).BUILT_INS

    def is_symbol(self, word: str) -> bool:
        return word in "=[]{}().+-*/><||:;_,"
    
    def is_comment_symbol(self, word: str, language: str) -> bool:
        return (word == Grammar.COMMENT_SYMBOLS[language])
        
    def get_type(self, word) -> dict:
        if word.isspace():
            return {"word": word, "type": "white_space"}
        if self._is_type(word):
            return {"word": word, "type": "type"}
        if self.is_symbol(word):
            return {"word": word, "type": "symbol"}
        if self._is_reserved_word(word):
            return {"word": word, "type": "reserved_word"}
        if self._is_literal(word):
            return {"word": word, "type": "literal"}
        if self._is_built_in(word):
            return {"word": word, "type": "built_in"}
        return {"word": word, "type": "other"}