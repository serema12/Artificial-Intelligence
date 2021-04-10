import argparse
import sys
from time import time
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from Maze import Maze
from SearchAlgo import PathFinderAlgorithm


class MazeRunner():
    def __init__(self, maze_dimension, probability_of_obstacles,heuristic, algorithm, fire):
        self.algorithm = algorithm
        self.maze_dimension = maze_dimension
        self.heuristic = heuristic
        self.probability_of_obstacles = probability_of_obstacles
        self.fire = fire

    def create_environment(self, new_maze = None,new_p = None):

        # Create the maze
        if new_p is not None:
            self.probability_of_obstacles = new_p
        self.maze = Maze(algorithm = self.algorithm, n = self.maze_dimension, p = self.probability_of_obstacles, fire = self.fire)
        self.maze.generate_maze(new_maze = new_maze)

        # Generate graph from the maze
        self.maze.create_graph_from_maze()

    def run(self):
        # Run the path finding algorithm on the graph
        self.path_finder = PathFinderAlgorithm(maze = self.maze,algorithm = self.algorithm,heuristic = self.heuristic)
        self.path_finder.run_path_finder_algorithm()
    def find_probability_can_be_solved(self):
        prob_list = np.arange(0,1,0.2)
                
        p_solving_maze = []
        for new_p in prob_list:
                        
            solvable = 0
            for i in range(100):
                self.create_environment(new_p = new_p)
                self.path_finder = PathFinderAlgorithm(maze = self.maze,algorithm = self.algorithm,heuristic = self.heuristic)
                result = self.path_finder.run_path_finder_algorithm()
                print(result)
                if result:
                    solvable +=1
            p_solving_maze.append(solvable/100)
        plt.figure()
        plt.xtitle('Probabilty of obstacles')
        plt.ytitle('Probabilty of solving mazes')
        plt.plot(prob_list,p_solving_maze,marker = "o")
        plt.show()
        plt.pause(100)
                
                
    def find_max_dimension(self):
        dim_list = range(10, 300, 10)
        algorithm =  ["astar","bfs","dfs"]
        max_dimension = dict()
        for i in range(5):
            print(f"Trial {i}")
            for algo in algorithm:
                for dim in dim_list:
                    print(f"Dim = {dim} for algo:{algo}")
                    maze = Maze(n = dim,algorithm=algo,p = self.probability_of_obstacles,fire = self.fire)
                    maze.generate_maze(new_maze = None)
                    maze.create_graph_from_maze()

                    if algo == "astar":
                        self.path_finder = PathFinderAlgorithm(maze = maze,algorithm = algo,heuristic = self.heuristic,time=60)
                    else:
                        self.path_finder = PathFinderAlgorithm(maze = maze,algorithm = algo,time=60)
                    result = self.path_finder.run_path_finder_algorithm()
                    if not result:
                        max_dimension[algo] = dim
                        break

        print(max_dimension)
     
    def calculate_performance_between_bfs_astar(self):
        prob_list = np.arange(0,1,0.5)
        algorithm =  ["astar","bfs"]
        average_bfs = []
        average_astar = []
        for algo in algorithm:
            for p in prob_list:
                temp = []
                for n in range(10):
                    #Generate every maze accoring to each trials and probabilities
                    maze = Maze(n = 10,algorithm=algo,p = self.probability_of_obstacles,fire = self.fire)
                    maze.generate_maze(new_maze = None)
                    maze.create_graph_from_maze()
                    if algo == "astar":
                        path_finder = PathFinderAlgorithm(maze = maze,algorithm = algo,heuristic = self.heuristic)
                    else:
                        path_finder = PathFinderAlgorithm(maze = maze,algorithm = algo)
                    result = path_finder.run_path_finder_algorithm()
                    performances = path_finder.performance_dict
                    temp.append(performances['number_of_nodes_expanded'])
                if algo =="astar":
                    average_astar.append(sum(temp)/10)
                else:
                    average_bfs.append(sum(temp)/10)
        plt.figure()
        plt.plot(prob_list,average_bfs,color='green',label='BFS')      
        plt.plot(prob_list, average_astar,color='red',label="Astar" )
        plt.legend()
        plt.show()
        plt.pause(100)
                
                
                
                

if __name__ == "__main__":
        #Algo: astar (with heuristics euclid), bfs, dfs, firealgo
    maze_runner = MazeRunner(maze_dimension = 50,
                                    probability_of_obstacles = 0.3,
                                    algorithm = 'firealgo', # Can be bfs,dfs, firealgo, astar
                                    heuristic = 'euclid', #euclid
                                    fire = True)

    maze_runner.create_environment()
    maze_runner.run()
    #maze_runner.find_solvable_map_size()
    
    #maze_runner.plot_performance_metrics()
        
