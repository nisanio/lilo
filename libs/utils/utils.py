

def right(window, buffer, cursor):
    cursor.right(buffer)
    window.down(buffer, cursor)
    window.horizontal_scroll(cursor)

def left(window, buffer, cursor):
    cursor.left(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor) 

def menu_string(src_string, cols):
    if len(src_string) < cols:
        fill_str =  " " * (cols - len(src_string))
    return src_string + fill_str