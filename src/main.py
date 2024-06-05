from maze import Maze
from graph import GraphNode

def main():
    # create a maze from the json file
    maze = Maze.create_from_json("../bin/maze.json")
    
    # build the graph using the maze
    graph = GraphNode(maze.start)
    graph.build_graph(maze)

    # return the result of searching algorithms
    search_results = graph.search_algorithms(maze)
    
    # print the results
    for search_result in search_results:
        print(f"***** {search_result} *****\n- Found goal: {search_results[search_result][0].get_position()}\n- Solution cost: {search_results[search_result][1]}\n- Solution path: ", end="")
        for solution_path in search_results[search_result][2]:
            print(solution_path, end=" ")
        print("\n- Expanded nodes: ", end="")
        for expanded_node in search_results[search_result][3]:
            print(expanded_node.get_position(), end=" ")
        print("\n- Number of nodes expanded: ", len(search_results[search_result][3]), "\n")    

if __name__ == "__main__":
    main()