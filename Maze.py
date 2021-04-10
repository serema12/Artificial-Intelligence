import numpy as np
import matplotlib
from pylab import *
from matplotlib import colors

matplotlib.use('tkAgg')
class Node():
    def __init__(self,
                 algorithm = None,
                 value = None,
                 row = None,
                 column = None,
                 left = None,
                 right = None,
                 up = None,
                 down = None,
                 parent = None,
                 distance_from_dest = None,
                 distance_from_source = np.inf,
                 distance_from_fire = None,
                 num_nodes_before_this_node = None):
        self.algorithm = algorithm
        self.value = value
        self.row = row
        self.column = column
        self.parent = parent
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.distance_from_dest = distance_from_dest
        self.distance_from_source = distance_from_source
        self.distance_from_fire = distance_from_fire
        self.num_nodes_before_this_node = num_nodes_before_this_node
        self.distance_from_fire = None

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __lt__(self, other):
        if self.algorithm == "firealgo":
            selfPriority = self.distance_from_fire + self.distance_from_dest
            otherPriority = other.distance_from_fire + other.distance_from_dest
        else:
            selfPriority = self.distance_from_source + self.distance_from_dest
            otherPriority = other.distance_from_source + other.distance_from_dest
        return selfPriority <= otherPriority

    def get_heuristic(self):
        if self.algorithm == "firealgo":
            return (self.distance_from_fire + self.distance_from_dest)
        else:
            return (self.distance_from_source + self.distance_from_dest)

    def get_children(self, node, algorithm):
        if algorithm == 'dfs':
            return [node.left, node.up, node.down, node.right]
        elif algorithm == 'bfs':
            return [node.right, node.down, node.up, node.left]
        else:
            return [node.left, node.up, node.down, node.right]
class Graph():
    def __init__(self, maze = None, algorithm = None):
        self.maze = maze
        self.algorithm = algorithm
        self.graph_maze = np.empty(shape = self.maze.shape, dtype = object)

    def create_graph_from_maze(self):
        for row in range(len(self.maze)):
            for column in range(len(self.maze)):
                if self.maze[row, column] == 0:
                    continue
                self.graph_maze[row, column] = Node(value = self.maze[row, column],
                                                    row = row,
                                                    column = column,
                                                    algorithm = self.algorithm)
        #Attach each node's relative to itself
        # Left
        for row in range(len(self.maze)):
            for column in range(len(self.maze)):
                try:
                    if column - 1 >= 0:
                        self.graph_maze[row, column].left = self.graph_maze[row, column - 1]
                except Exception:
                    continue

        # Right
        for row in range(len(self.maze)):
            for column in range(len(self.maze)):
                try:
                    self.graph_maze[row, column].right = self.graph_maze[row, column + 1]
                except Exception:
                    continue

        # Up
        for row in range(len(self.maze)):
            for column in range(len(self.maze)):
                try:
                    if row - 1 >= 0:
                        self.graph_maze[row, column].up = self.graph_maze[row - 1, column]
                except Exception:
                    continue

        # Down
        for row in range(len(self.maze)):
            for column in range(len(self.maze)):
                try:
                    self.graph_maze[row, column].down = self.graph_maze[row + 1, column]
                except Exception:
                    continue
class Maze():
    ProbabilityOfBlockedMaze = 0.4
    DimensionOfMaze = 25

    def __init__(self,
                 n = DimensionOfMaze,
                 p = ProbabilityOfBlockedMaze,
                 fire = None,
                 algorithm = None,
                 maze = None,
                 maze_copy = None,
                 colormesh = None):
        self.n = n
        self.p = p
        self.algorithm = algorithm
        self.maze = maze
        self.maze_copy = maze_copy
        self.colormesh = colormesh
        self.fire = fire
        self.counter = 0

        # The default colormap of our maze - 0: Black, 1: White, 2: Grey
        self.cmap = colors.ListedColormap(['black', 'white', 'grey', 'orange', 'red'])
        self.norm = colors.BoundaryNorm(boundaries = [0, 1, 2, 3, 4], ncolors = 4)

    def generate_maze(self, new_maze = None):

        if new_maze is not None:
            self.maze = new_maze
            self.original_maze = self.maze.copy()
            self.maze_copy = self.maze.copy()
            self.create_graph_from_maze()
            return

        self.maze = np.array([list(np.random.binomial(1, 1 - self.p, self.n)) for _ in range(self.n)])
        self.maze[0, 0] = 4
        self.maze[self.n - 1, self.n - 1] = 4

        if self.fire:
            self.maze[self.n - 1, 0] = 3

        # This will be the original maze
        self.original_maze = self.maze.copy()

        # Create a copy of maze to render and update
        self.maze_copy = self.maze.copy()

    def set_original_maze(self, new_maze):
        self.original_maze = new_maze

    def create_graph_from_maze(self):
        self.graph = Graph(maze = self.maze, algorithm = self.algorithm)
        self.graph.create_graph_from_maze()

    def render_maze(self, title = None, timer = 1e-15):

        # Create a mask for the particular cell and change its color to green
        masked_maze_copy = np.rot90(np.ma.masked_where(self.maze_copy == -1, self.maze_copy), k = 1)
        self.cmap.set_bad(color = 'green')

        # Plot the new maze
        if self.colormesh is None:
            self.colormesh = plt.pcolor(masked_maze_copy,cmap = self.cmap,norm = self.norm,edgecolor = 'k',linewidth = 0.5,antialiased = False)
        else:
            self.colormesh.set_array(masked_maze_copy.ravel())
        plt.xticks([])
        plt.yticks([])
        plt.ion()
        plt.show()
        plt.title(title)
        plt.pause(timer)

    def update_color_of_cell(self, row, column):
        if self.maze[row, column] == 4:
            return
        self.maze_copy[row, column] = -1

    def reset_color_of_cell(self, row, column):
        if self.maze[row, column] == 4:
            return
        self.maze_copy[row, column] = 2

    def wild_fire(self, row, column):
        if (row == 0 and column == 0) or (row == self.n - 1 and column == self.n - 1):
            return
        self.maze_copy[row, column] = 3

    def reset_environment(self):
        self.maze = self.original_maze.copy()
        self.maze_copy = self.maze.copy()
        self.create_graph_from_maze()

    def modify_environment(self, row = None, column = None, new_maze = None):

        if new_maze is not None:
            self.maze = new_maze
        else:

            # If the cell's value is 1 change it to 0 and vice-versa
            if self.maze[row, column] == 0:
                self.maze[row, column] = 1
            else:
                self.maze[row, column] = 0

        # Update copy of maze
        self.maze_copy = self.maze.copy()
        self.create_graph_from_maze()
