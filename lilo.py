#!/usr/bin/env python3
import curses
import sys
import argparse
import pdb
from curses import wrapper

from pygments.lexers import PythonLexer, CLexer
from pygments.formatters import TerminalFormatter
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Whitespace
from pygments import highlight


class Window:
    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def up(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.row += 1
            
    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < buffer.bottom:
            self.row += 1

    def translate(self, cursor):
        return max(cursor.row - self.row, 0), max(cursor.col - self.col, 0)

    def horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
        n_pages = cursor.col // (self.n_cols - right_margin)
        self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)
    
class Cursor:
    def __init__(self, row=1, col=0, col_hint=None):
        self.row = row
        self._col = col
        self._col_hint = col if col_hint is None else col_hint

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col =  col
        self._col_hint = col
         
    def up(self, buffer):
        if self.row > 1:
            self.row -= 1
            self._clamp_col(buffer)

    def down(self, buffer):
        if self.row < buffer.bottom:
            self.row += 1
            self._clamp_col(buffer)

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

    def right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col +=1
        elif self.row < buffer.bottom:
            self.row += 1
            self.col = 0

    def _clamp_col(self, buffer):
        self._col = min(self._col_hint, len(buffer[self.row]))

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    @property
    def bottom(self):
        return len(self) - 1

    def _current(self, row):
        current = ''
        if len(self.lines) > 0:
            current = self.lines.pop(row) 
        return current 
        
    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col
        current = self._current(row)
        new = current[:col] + string + current[col:]
        self.lines.insert(row, new)

    def split(self, cursor):
        row, col = cursor.row, cursor.col,
        current = self._current(row)
        self.lines.insert(row, current[:col])
        self.lines.insert(row + 1, current[col:])

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if(row, col) < (self.bottom, len(self[row])):
            current = self._current(row)
            if col < len(self[row]):
                new = current[:col] + current[col + 1:]
                self.lines.insert(row, new)
            else:
                next = self.lines.pop(row)
                new = current + next
                self.lines.insert(row, new)

class File:
    def __init__(self, filename = "textfile.txt"):
        self._filename = filename
        self._dirty = False
    
    def hasBeenModified(self):
        return self.dirty
    
    def setFileName(self, filename):
        self._filename = filename

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, dirty):
        self._dirty = dirty

    def open_file(self):
        mode = "w+" if self._filename == 'textfile.txt' else "r+"
        try:
            with open(self._filename, mode) as f:
                buffer = Buffer(f.read().splitlines())
                resp = "buffer"
        except: 
            buffer = Buffer([])
        return buffer

    def save_file(self, buffer):
        with open(self.filename, 'w') as f:
            content = ''.join(buffer.lines)
            f.write(content)
            self.dirty = 0
    
def right(window, buffer, cursor):
    cursor.right(buffer)
    window.down(buffer, cursor)
    window.horizontal_scroll(cursor)

def left(window, buffer, cursor):
    cursor.left(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor) 

def menu_string(src_string):
    if len(src_string) < curses.COLS:
        fill_str =  " " * (curses.COLS - len(src_string))
    return src_string + fill_str

def main(stdscr):

    # parser = argparse.ArgumentParser()
    # parser.add_argument("filename")
    # args = parser.parse_args()
    

    
    file = File()
    if len(sys.argv) == 2:
        file.setFileName("./" + sys.argv[1])

    buffer = file.open_file()

    window = Window(curses.LINES - 1, curses.COLS -1)
    cursor =  Cursor()
    title_string = f"OPEN FILE: CTRL-O : SAVE: CTRL+S    CLOSE: CTRL+Q   "
    title_string = menu_string(title_string)

    while True:
        bottom_string = menu_string(f"File: {file._filename} Current Line:{cursor.row} Dirty: {file.dirty}")
        stdscr.erase()
        stdscr.addstr(0, 0,  title_string, curses.color_pair(3))
       # stdscr.addstr(0, 0, '\n')

        
        if len(buffer.lines) > 0:
            for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
                if row == cursor.row - window.row and window.col > 0:
                    line = "«" + line[window.col + 1:]
                if len(line) > window.n_cols:
                    line = line[:window.n_cols - 1] + "»"
                stdscr.addstr(row + 1, 0, line)                    
        else:
            pass
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
        stdscr.addstr(curses.LINES - 1, 0, bottom_string[:len(bottom_string)-1], curses.color_pair(3))
       
        x, y = window.translate(cursor)
        try:
           
            stdscr.addstr(0, 0, f"OK :{x} {y}".format(x, y))
            stdscr.move(*window.translate(cursor))
            
        except Exception as error:
            stdscr.addstr(0, 0, f"ERR:{x} {y}".format(x, y))

        curses.raw()
        k = stdscr.getkey()
        stdscr.addstr(0, 0, k)  
        curses.noraw()
        
        if  k == 'q':
            sys.exit(0)
        elif ord(k[0]) == 19:
            #grabar
            pass
        elif ord(k[0]) == 17:
            sys.exit(0) 
        elif k == "KEY_UP":
            cursor.up(buffer)
            window.up(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
            window.down(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_LEFT":
            cursor.left(buffer)
            window.up(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)
            window.down(buffer, cursor)
            window.horizontal_scroll(cursor)
        elif k == "\n":
            buffer.split(cursor)
            right(window, buffer, cursor)
        elif k in ("KEY_DELETE",  "\x04", "KEY_DC"):
            buffer.delete(cursor)
        elif k in ("KEY_BACKSPACE", "\x7f"):
            if (cursor.row, cursor.col) > (0, 0):
                left(window, buffer, cursor)
                buffer.delete(cursor)
        else:
            buffer.insert(cursor, k)
            for _ in k:
                right(window, buffer, cursor)

if __name__ == "__main__":
    wrapper(main)
