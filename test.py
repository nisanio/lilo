import pdb
import logging
from random import random, uniform
import sys
import curses
import argparse
import time
from curses import wrapper
from pygments.lexers import PythonLexer, CLexer
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Whitespace
from pygments import highlight
from libs.highlight.file import HLFile
from libs.highlight.highlighter import HighLighter
from pythongrammar import PythonGrammar

class Buffer:
    def __init__(self, lines):
        self.lines = lines
        self._tokens = []

    def _tokenize(self):
        lexer = PythonLexer()
        self._tokens = []
        for line in self.lines:
            l = []
            t_gen = lexer.get_tokens(line)
            for to in t_gen:
                    l.append({
                        "type": to[0],
                        "value": to[1]
                    })
            self._tokens.append(l)

    @property
    def tokens(self):
        self._tokenize()
        return self._tokens
        

def open_file(src, mode):
    try:
        with open(sys.argv[1], mode) as f:
            buffer = Buffer(f.read().splitlines())
    except: 
        pass
    return buffer

def print_word(stdscr, posY, posX, word, color, delay):
    size_word = len(word)
    iter = 0
    time.sleep(0.2)
    logging.info(f"word is {word}".format(word))
    reserved_word = False
    if color == curses.color_pair(2):
        logging.info(f"word is reserved")
        reserved_word = True
    while (iter < size_word):
        start = uniform(0.010, 0.019)
        end = uniform(0.30, 0.39)
        if reserved_word and iter > 3:
            stdscr.addch(posX, (posY + iter), word[iter], color)
        else:
            time.sleep(uniform(start, end))
            stdscr.addch(posX, (posY + iter), word[iter], color)
        stdscr.refresh()        
        iter = iter + 1
    return size_word

def print_line_with_color(stdscr, row, line):
    pos = 0
    
    for idx, token in enumerate(line):

        color = "0"
        if token['type'] == 'reserved_word':
            color = curses.color_pair(2)
        if token['type'] == 'other':
            color = curses.color_pair(1)
        if token['type'] == 'literal':
            color = curses.color_pair(6)
        if token['type'] == 'built_in':
            color = curses.color_pair(4)
        if token['type'] == 'white_space':
            color = curses.color_pair(5)
        if token['type'] == 'symbol':
            color = curses.color_pair(3)
        
        pos = pos + print_word(stdscr, pos, row, token['word'], color, 0)


def main(stdscr):
    stdscr.erase()
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)
    

    if len(sys.argv) == 2:
        buffer = open_file(sys.argv[1], "r+")
    else:
       buffer = []

    file = HLFile(sys.argv[1])
    hl = HighLighter(file)
    program = hl.process_file()

    while True:
        for row, line in enumerate(program):
            if row < 35:
                
                print_line_with_color(stdscr, row, line)
        key = stdscr.getkey()
        if key == 'q':
            break
        
# class FCurses:
#     def __init__(self):
#         pass
    
#     def addstr(self, y, x, str, color):
#         print(str, end="", flush=True)

#     def refresh(self):
#         pass

#     def getkey(self):
#         k = input()
#         return k
     

if __name__ == "__main__":
    # stdscr = FCurses()
    wrapper(main)

