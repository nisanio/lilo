from libs.highlight.highlighter import HighLighter
from libs.highlight import HLFile
import sys
import pdb
import time 



class FCurses:
    def __init__(self):
        pass
    
    def addstr(self, y, x, str, color):
        print(str, end="", flush=True)

    def refresh(self):
        pass

    def getkey(self):
        k = input()
        return k
     

class Buffer:
    def __init__(self, lines):
        self.lines = lines

def print_word(word, color):
    print(word + ":" + color)
    

    

def print_line_with_color(stdscr, row, line):
    pos = 0
    
    for idx, token in enumerate(line):

        color = "0"
        if token['type'] == 'reserved_word':
            color = "1"
        if token['type'] == 'other':
            color = "2"
        if token['type'] == 'literal':
            color = "3)"
        if token['type'] == 'built_in':
            color = "4"
        if token['type'] == 'white_space':
            color = "5"
        if token['type'] == 'symbol':
            color = "6"
        
        print_word(token['type'], color)


def open_file(src, mode):
    try:
        with open(sys.argv[1], mode) as f:
            # buffer = Buffer(f.read().splitlines())
            buffer = Buffer(f.read())
    except: 
        pass
    return buffer

if __name__ == "__main__":
    stdscr =FCurses()
    if len(sys.argv) == 2:
        buffer = open_file(sys.argv[1], "r+")
    else:
       buffer = []
    
    file = HLFile('./test.py')
    hl = HighLighter(file)
    program = hl.process_file()
    
    while True:
        for row, line in enumerate(program):
            if row < 35:
                print_line_with_color(stdscr, row, line)
        key = stdscr.getkey()
        if key == 'q':
            break
   