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
from libs.utils.utils import menu_string, left, right
from libs.file import File 
from libs.window import Window
from libs.cursor import Cursor


def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)
    
    file = File()
    if len(sys.argv) == 2:
        file.setFileName("./" + sys.argv[1])

    buffer = file.open_file()

    window = Window(curses.LINES - 1, curses.COLS -1)
    cursor =  Cursor()
    title_string = f"OPEN FILE: CTRL-O : SAVE: CTRL+S    CLOSE: CTRL+Q   "
    title_string = menu_string(title_string, curses.COLS)

    while True:
        bottom_string = menu_string(f"File: {file._filename} Current Line:{cursor.row} Dirty: {file.dirty}", curses.COLS)
        stdscr.erase()
        stdscr.addstr(0, 0,  title_string, curses.color_pair(3))
        
        # for i in range(curses.LINES):
        #     if i > len(buffer.lines):
        #         stdscr.addstr(i, 2, "~")

        if len(buffer.lines) > 0:
            for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
                if row == cursor.row - window.row and window.col > 0:
                    line = "«" + line[window.col + 1:]
                if len(line) > window.n_cols:
                    line = line[:window.n_cols - 1] + "»"
                if not line:
                    stdscr.addstr(row + 1, 2, "")
                else: 
                    stdscr.addstr(row + 1, 2, line)                    
        
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
