from maze import Maze
from agent import Agent
from tree import TreeNode
import json

def main():
    maze = Maze.create_from_json("maze.json")
    agent = Agent(row=maze.start.row, col=maze.start.col, total_points=0, followed_path=())
    print(agent)
    TreeNode(maze.start).build_tree(maze)
    
if __name__ == "__main__":
    main()