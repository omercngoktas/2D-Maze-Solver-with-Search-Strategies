class Cell:
    def __init__(self, row, col, east, south, west, north):
        self.row = row
        self.col = col
        self.east = east
        self.south = south
        self.west = west
        self.north = north

    # get the row and column of the current cell
    def get_position(self):
        return self.row, self.col

class Goal:
    def __init__(self, id, cell):
        self.id = id
        self.cell = cell
    
    def get_position(self):
        return self.cell.get_position()
