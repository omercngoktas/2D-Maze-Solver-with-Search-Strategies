from cell import Cell, Goal
import json

class Maze:
    def __init__(self, start, goals, traps, cells):
        self.start = start
        self.goals = goals
        self.traps = traps
        self.cells = cells

    # create a maze from a json file (maze.json)
    @classmethod
    def create_from_json(cls, maze_file):
        with open(maze_file, "r") as file:
            maze_data = json.load(file)
            
        start_data = maze_data["start"]
        goals_data = [{"id": goal["id"], "row": goal["row"], "col": goal["col"]} for goal in maze_data["goals"]]
        traps_data = [{"row": trap["row"], "col": trap["col"]} for trap in maze_data["traps"]]
        goals = []
        traps = []
        cells = []
        
        for cell_data in maze_data["cells"]:
            cell = Cell(
                cell_data["row"],
                cell_data["col"],
                cell_data["East"],
                cell_data["South"],
                cell_data["West"],
                cell_data["North"]
            )
            cells.append(cell)
        
        for cell in cells:
            if cell.row == start_data["row"] and cell.col == start_data["col"]:
                start = cell
                
            for goal in goals_data:
                if cell.row == goal["row"] and cell.col == goal["col"]:
                    current_goal = Goal(goal["id"], cell)
                    goals.append(current_goal)
            
            for trap in traps_data:
                if cell.row == trap["row"] and cell.col == trap["col"]:
                    traps.append(cell)   
        return cls(start, goals, traps, cells)
    
    # get the neighbor cell of the current cell
    def _get_neighbor(self, current_cell, direction):
        row, col = current_cell.get_position()
        
        if (direction == "North") and (row > 1) and (current_cell.north == 0):
            return self.cells[(row - 2) * 8 + col - 1]
        elif (direction == "South") and (row < 8) and (current_cell.south == 0):
            return self.cells[row * 8 + col - 1]
        elif (direction == "West") and (col > 1) and (current_cell.west == 0):
            return self.cells[(row - 1) * 8 + col - 2]
        elif (direction == "East") and (col < 8) and (current_cell.east == 0):
            return self.cells[(row - 1) * 8 + col]
        
        return None

    # get the neighbors of the current cell (north, east, south, west) and return them as a dictionary
    def get_neighbors(self, current_cell):
        directions = ["North", "East", "South", "West"]
        available_moves = {"North": None, "East": None, "South": None, "West": None}
        
        for direction in directions:
            temp = {direction : self._get_neighbor(current_cell, direction)}
            available_moves.update(temp)
            
        return available_moves