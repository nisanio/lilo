from collections.abc import MutableSequence
from typing import Union

import pdb

from libs.highlight.grammar import Grammar


class TokenList(MutableSequence):
    def __init__(self, grammar: Grammar):
        self._word = ''
        self._enriched = False
        self._tokens = []
        self._rich_tokens = []
        self._grammar = grammar

    @property
    def filename(self):
        return self._filename
    
    @property
    def type(self):
        return self._type
    
    @property
    def grammar(self):
        return self._grammar
    
    @property
    def word(self) -> str:
        return self._word
        
    @word.setter
    def word(self, value):
        self._word = value
        
    @property
    def enriched(self) -> bool:
        return self._enriched

    @enriched.setter
    def enriched(self, value: bool):
        self._enriched = value
        
    def __len__(self):
        return len(self._tokens)

    def __getitem__(self, index: int) -> Union[int, dict]:
        if self._enriched:
            return self._rich_tokens[index]
        return self._tokens[index]

    def __setitem__(self, index: int, value: str):
        self._tokens[index] = value
        self._rich_tokens[index] = self._grammar.get_type(value)

    def __delitem__(self, index: int):
        del self._tokens[index]
        del self._rich_tokens[index]

    def __repr__(self):
        if self._enriched:
            return repr(self._rich_tokens)
        return repr(self._tokens)

    def append(self, token):
        self._tokens.append(token)
        self._rich_tokens.append(self._grammar.get_type(token))

    def insert(self, index: int, value: str):
        self._tokens.insert(index, value)
        self._rich_tokens.insert(index, self._grammar.get_type(value))

    def flush(self):
        if len(self._word):
            self.append(self._word)
            self._word = ''