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