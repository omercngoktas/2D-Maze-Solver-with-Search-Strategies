from maze import Maze
from collections import deque

# GraphNode class for building the graph
class GraphNode:
    def __init__(self, cell, parent=None):
        self.cell = cell
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.parent = parent
    
    # build the graph using the maze
    def build_graph(self, maze):
        visited_cells = set()
        self._build_graph_recursive(maze, self, visited_cells)

    # build the graph using the maze recursively
    def _build_graph_recursive(self, maze, current_node, visited_cells):
        if current_node.cell in visited_cells:
            return        
        # add the current cell to the visited cells
        visited_cells.add(current_node.cell)
        # get the available moves for the current cell
        available_moves = maze.get_neighbors(current_node.cell)
        
        for available_move in available_moves:
            # because of the directions, we need to clear the visited cells.
            # so that start cell will start checking other directions with empty visited cells
            if current_node.cell == maze.start:
                visited_cells.clear()
                visited_cells.add(current_node.cell)
            # if the movement is valid (there is no wall for the movement)
            if available_moves[available_move]:
                child_cell = GraphNode(cell=available_moves[available_move], parent=current_node)
                setattr(current_node, available_move.lower(), child_cell)
                self._build_graph_recursive(maze=maze, current_node=child_cell, visited_cells=visited_cells)
    
    # check if the current cell is a goal cell
    def _is_cell_goal(self, goals):
        for goal in goals:
            if self.cell == goal.cell:
                return True
        return False

    # check if the current cell is a trap cell
    def _is_cell_trap(self, traps):
        for trap in traps:
            if self.cell == trap:
                return True
        return False
    
    # find the path to the goal cell
    def _find_solution_path_and_cost(self, traps):
        solution_cost = 0
        solution_path = []
        if self:
            current_node = self
            while current_node:
                solution_path.append(current_node.cell.get_position())
                solution_cost += 1
                if current_node._is_cell_trap(traps):    
                    solution_cost += 6
                current_node = current_node.parent
        
        return solution_cost, self.reverse_list(solution_path)
    
    # insertion sort algorithm for sorting the queue by cost or path length (used in greedy best first search and A* search)
    def insertion_sort(self, queue, maze, sort_by=0):
        for i in range(1, len(queue)):
            current_node = queue[i]
            current_node_cost = current_node._find_solution_path_and_cost(maze.traps)[sort_by]
            j = i - 1
            while j >= 0 and current_node_cost < queue[j]._find_solution_path_and_cost(maze.traps)[sort_by]:
                queue[j + 1] = queue[j]
                j -= 1
            queue[j + 1] = current_node
        return queue
    
    # return the result of A* search algorithm using manhattan distance heuristic
    def manhattan_distance(self, cell1, goals):
        distances = []
        for goal in goals:
            distances.append(abs(cell1[0] - goal.cell.row) + abs(cell1[1] - goal.cell.col))
        return min(distances)
    
    # finding the path to the goal cell using depth first search algorithm
    def depth_first_search(self, maze):
        expanded_nodes = []
        return self._depth_first_search_postorder(maze, expanded_nodes)

    # finding the path to the goal cell using depth first search algorithm with postorder traversal
    def _depth_first_search_postorder(self, maze, expanded_nodes):
        directions = ["east",  "south", "west", "north"]
        # if the current node is not empty
        if self:
            # for each direction
            for direction in directions:
                child_node = getattr(self, direction)
                expanded_nodes.append(self.cell)
                # if the child node is not empty
                if child_node:
                    result = child_node._depth_first_search_postorder(maze, expanded_nodes)
                    if result:
                        return result
            # if the current node is a goal cell
            if self._is_cell_goal(maze.goals):
                path_and_cost = self._find_solution_path_and_cost(maze.traps)
                return self.cell, path_and_cost[0], path_and_cost[1], expanded_nodes
        return None
    
    # finding the path to the goal cell using depth first search algorithm
    def breadth_first_search(self, maze):
        expanded_nodes = []
        return self._breadth_first_search(maze.goals, maze.traps, expanded_nodes)
    
    # finding the path to the closest goal cell using breadth first search algorithm
    def _breadth_first_search(self, goals, traps, expanded_nodes):
        directions = ["east",  "south", "west", "north"]
        # if the current node is not empty
        if self:
            queue = deque([self])
            while queue:
                current_node = queue.popleft()
                if current_node.cell in expanded_nodes:
                    continue
                expanded_nodes.append(current_node.cell) 
                if current_node._is_cell_goal(goals):
                    solution_cost_path = current_node._find_solution_path_and_cost(traps)
                    return current_node.cell, solution_cost_path[0], solution_cost_path[1], expanded_nodes
                for direction in directions:
                    child_node = getattr(current_node, direction)
                    if child_node:
                        queue.append(child_node)
            return False
        
    # return the result of iterative deepening search algorithm
    def iterative_deepening_search(self, maze, max_depth):
        # from 0 to max_depth
        for depth in range(max_depth):
            expanded_nodes = list()
            result = self._iterative_deepening_search(maze, depth, expanded_nodes)
            if result:
                return result
        return None
    
    # finding the path to the goal cell using iterative deepening search algorithm
    def _iterative_deepening_search(self, maze, max_depth, expanded_nodes):
        directions = ["east",  "south", "west", "north"]
        # if the current node is not empty
        if self:
            queue = deque([self])
            queue.append(max_depth)
            # while the queue is not empty
            while queue:
                current_node = queue.popleft()
                current_depth = queue.popleft()
                if current_depth == 0:
                    continue
                # if the current node is a goal cell
                if current_node._is_cell_goal(maze.goals):
                    path_and_cost = current_node._find_solution_path_and_cost(maze.traps)
                    return current_node.cell, path_and_cost[0], path_and_cost[1], expanded_nodes
                # for each direction
                for direction in directions:
                    child_node = getattr(current_node, direction)
                    expanded_nodes.append(current_node.cell)
                    if child_node:
                        queue.append(child_node)
                        queue.append(current_depth - 1)
    
    # finding the optimum path to the goal cell using greedy best first search and A* search algorithms and uniform cost search
    def gbfs_astar_ucs(self, maze, algorithm):
        expanded_nodes = []
        return self._gbfs_astar_ucs(maze, expanded_nodes, algorithm)
    
    # finding the goal cell using greedy best first search algorithm
    def _gbfs_astar_ucs(self, maze, expanded_nodes, algorithm):
        directions = ["east",  "south", "west", "north"]
        # if the current node is not empty
        if self:
            queue = [self]
            # while the queue is not empty
            while queue:
                current_node = queue.pop(0)
                if current_node._is_cell_goal(maze.goals):
                    path_and_cost = current_node._find_solution_path_and_cost(maze.traps)
                    return current_node.cell, path_and_cost[0], path_and_cost[1], expanded_nodes
                # for each direction
                for direction in directions:
                    child_node = getattr(current_node, direction)
                    expanded_nodes.append(current_node.cell)
                    if child_node:
                        queue.append(child_node)
                # check the algorithm type and sort the queue by cost or path length 
                if algorithm == "greedy":
                    queue = self.insertion_sort(queue, maze, sort_by=1)
                elif algorithm == "a_star":
                    queue.sort(key=lambda node: node._find_solution_path_and_cost(maze.traps)[0] + self.manhattan_distance(node.cell.get_position(), maze.goals))
                elif algorithm == "ucs":
                    queue = self.insertion_sort(queue, maze, sort_by=0)
    
    # reverse the list (used in finding the path to the goal cell)
    def reverse_list(self, list):
        reversed_list = []
        for i in range(len(list) - 1, -1, -1):
            reversed_list.append(list[i])
        return reversed_list

    # return the results of all search algorithms
    def search_algorithms(self, maze):
        return {
            "DFS result": self.depth_first_search(maze),
            "BFS result": self.breadth_first_search(maze),
            "IDS result": self.iterative_deepening_search(maze, 10),
            "UCS result": self.gbfs_astar_ucs(maze, "ucs"),
            "Greedy Best First Search result": self.gbfs_astar_ucs(maze, "greedy"),
            "A* result": self.gbfs_astar_ucs(maze, "a_star")
        }
    
    def depth_first_search_2(self, maze):
        expanded_nodes = []
        return self._depth_first_search_postorder_2(maze, expanded_nodes)
    
    def _depth_first_search_postorder_2(self, maze, expanded_nodes):
        directions = ["east",  "south", "west", "north"]
        # if the current node is not empty
        if self:
            # for each direction
            for direction in directions:
                child_node = getattr(self, direction)
                expanded_nodes.append(self.cell)
                # if the child node is not empty
                if child_node:
                    result = child_node._depth_first_search_postorder_2(maze, expanded_nodes)
                    if result:
                        return result
            # if the current node is a goal cell
            if self._is_cell_goal(maze.goals):
                path_and_cost = self._find_solution_path_and_cost(maze.traps)
                return self.cell, path_and_cost[0], path_and_cost[1], expanded_nodes
            
        return None