from libs.buffer import Buffer

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
