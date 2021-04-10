import numpy as np
import queue as Q
from Maze import Maze
import time

class PathFinderAlgorithm():
    DfsString = "dfs"
    BfsString = "bfs"
    AStarString = "astar"
    ThinningAStar = "thin_astar"
    FireString = "firealgo"
    def __init__(self, maze = None, algorithm = None, heuristic = None, q = None,time=np.inf):
        self.maze = maze
        self.graph_maze = self.maze.graph.graph_maze
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.visited = []
        self.path = []
        self.max_fringe_length = 0
        self.q = q
        self.time = time
        if self.algorithm in ['dfs', 'bfs','firealgo']:
            self.title = "Algorithm: " + self.algorithm
        else:
            self.title = "Algorithm: " + self.algorithm + "    Heuristic: " + self.heuristic
        
    def _get_unvisited_children(self, node_children):

        # If the algorithm is firealgo, then reorder children based on their heuristic values - distance from fire +
        # distance from destination
        if self.algorithm == "firealgo":
            temp_queue = Q.PriorityQueue()

        unvisited_children = []
        for child in node_children:
            if child is None:
                continue

            if child not in self.visited:
                if self.algorithm == "firealgo":
                    child.distance_from_fire = self._get_fire_distance(child)
                    temp_queue.put(child)
                else:
                    unvisited_children.append(child)

        if self.algorithm == "firealgo":
            unvisited_children = []
            while temp_queue.queue:
                unvisited_children.append(temp_queue.get())
            unvisited_children = unvisited_children[::-1]

        return unvisited_children

    def _get_final_path(self):
        node = self.graph_maze[self.maze.n - 1, self.maze.n - 1]
        while node is not None:
            self.path.append((node.row, node.column))
            node = node.parent

    def _get_euclidien_distance(self, node, dest):
        return np.sqrt((node.row - dest.row)**2 + (node.column - dest.column)**2)

    def _calculate_heuristic(self, node, dest):
        return self._get_euclidien_distance(node, dest)

    def _get_fire_distance(self, node):
        fire_blocks = np.argwhere(self.maze.maze_copy == 3)
        all_that_is_burning = []

        for i in zip(fire_blocks):
            all_that_is_burning.append(tuple((i[0][0], i[0][1])))

        time_taken_to_die = []

        for i in all_that_is_burning:
            temp = np.sqrt((node.row - i[0])**2 + (node.column - i[1])**2)
            time_taken_to_die.append(temp)

        time_before_i_call_fire_engine = min(time_taken_to_die)
        alpha_val = -0.5

        return (alpha_val * time_before_i_call_fire_engine)

    def get_final_path_length(self):
        return len(self.path)

    def get_number_of_nodes_expanded(self):
        return len(self.visited)

    def get_maximum_fringe_length(self):
        return self.max_fringe_length

    def _create_performance_metrics(self):
        self.performance_dict = dict()
        self.performance_dict['path_length'] = self.get_final_path_length()
        self.performance_dict['maximum_fringe_size'] = self.get_maximum_fringe_length()
        self.performance_dict['number_of_nodes_expanded'] = self.get_number_of_nodes_expanded()

    def _run_dfs(self, root, dest):
        elapse = 0
        start = time.time()
        self.fringe = [root]
        self.visited.append(root)
        while self.fringe and elapse < self.time:

            # Keep track of maximum fringe length
            fringe_length = len(self.fringe)
            if fringe_length >= self.max_fringe_length:
                self.max_fringe_length = fringe_length

            node = self.fringe.pop()
            # update color of the cell and render the maze
            self.maze.update_color_of_cell(node.row, node.column)
            self.maze.render_maze(title = self.title)

            # if you reach the destination, then break
            if (node == dest):
                break
            
            if node not in self.visited:
                self.visited.append(node)
            # If there is no further path, then reset the color of the cell. Also, subsequently reset
            # the color of all parent cells along the path who have no other children to explore.
            flag = True
            while(flag):
                node_children = node.get_children(node = node, algorithm = self.algorithm)
                unvisited_children = self._get_unvisited_children(node_children)

                # If no unvisited children found, then reset the color of this cell in the current path
                # because there is no further path from this cell.
                if len(unvisited_children) == 0:
                    self.maze.reset_color_of_cell(node.row, node.column)
                    self.maze.render_maze(title = self.title)
                else:
                    for child in unvisited_children:
                        child.parent = node
                        self.fringe.append(child)
                    flag = False

                node = node.parent
                if node is None:
                    flag = False
            elapse = time.time() - start
            
    def _run_bfs(self, root, dest):
        elapse = 0
        start = time.time()
        
        self.fringe = [root]
        self.visited.append(root)
        
        while self.fringe and elapse <= self.time:

            # Keep track of maximum fringe length
            fringe_length = len(self.fringe)
            if fringe_length >= self.max_fringe_length:
                self.max_fringe_length = fringe_length

            temp_path = []
            node = self.fringe.pop(0)

            if node not in self.visited:
                self.visited.append(node)

            node_children = node.get_children(node = node, algorithm = self.algorithm)
            unvisited_children = self._get_unvisited_children(node_children)

            for child in unvisited_children:

                # If child has been added to the fringe by some previous node, then dont add it again.
                if child not in self.fringe:
                    child.parent = node
                    self.fringe.append(child)
            # Get the path through which you reach this node from the root node
            flag = True
            temp_node = node
            while (flag):
                temp_path.append(temp_node)
                temp_node = temp_node.parent
                if temp_node is None:
                    flag = False
            temp_path_copy = temp_path.copy()

            # Update the color of the path which we found above by popping the root first and the subsequent nodes.
            while (len(temp_path) != 0):
                temp_node = temp_path.pop()
                self.maze.update_color_of_cell(temp_node.row, temp_node.column)
                self.maze.render_maze(title = self.title)

            # if you reach the destination, then break
            if (node == dest):
                break

            # We reset the entire path again to render a new path in the next iteration.
            while (len(temp_path_copy) != 0):
                temp_node = temp_path_copy.pop(0)

                self.maze.reset_color_of_cell(temp_node.row, temp_node.column)
                self.maze.render_maze(title = self.title)
            elapse = time.time() - start

    def _run_astar(self, root, dest):

        
        elapse = 0
        start = time.time()
        # Root is at a distance of 0 from itself
        root.distance_from_source = 0

        self.fringe = Q.PriorityQueue()
        self.fringe.put(root)
        self.visited.append(root)
        
        while self.fringe.queue and elapse <= self.time:

            # Keep track of maximum fringe length
            fringe_length = len(self.fringe.queue)
            if fringe_length >= self.max_fringe_length:
                self.max_fringe_length = fringe_length

            temp_path = []
            node = self.fringe.get()

            if node not in self.visited:
                self.visited.append(node)

            node_children = node.get_children(node = node, algorithm = self.algorithm)

            for child in node_children:
                if child is None or child in self.visited:
                    continue

                if child not in self.fringe.queue:
                    child.parent = node
                    child.distance_from_dest = self._calculate_heuristic(child, dest)
                    child.distance_from_source = node.distance_from_source + 1
                    self.fringe.put(child)
                else:
                    if child.get_heuristic() >= node.distance_from_source + child.distance_from_dest:
                        child.parent = node
                        child.distance_from_source = node.distance_from_source + 1
            
            # Get the path through which you reach this node from the root node
            flag = True
            temp_node = node
            while (flag):
                temp_path.append(temp_node)
                temp_node = temp_node.parent
                if temp_node is None:
                    flag = False
            temp_path_copy = temp_path.copy()

            # Update the color of the path which we found above by popping the root first and the subsequent nodes.
            while (len(temp_path) != 0):
                temp_node = temp_path.pop()

                self.maze.update_color_of_cell(temp_node.row, temp_node.column)
                self.maze.render_maze()

            # if you reach the destination, then break
            if (node == dest):
                break

            # We reset the entire path again to render a new path in the next iteration.
            while (len(temp_path_copy) != 0):
                temp_node = temp_path_copy.pop(0)

                self.maze.reset_color_of_cell(temp_node.row, temp_node.column)
                self.maze.render_maze()
            elapse = time.time() - start
    
    def _charizard(self):

        fire_blocks = np.argwhere(self.maze.maze_copy == 3)
        i_curr_burn = []

        for i in zip(fire_blocks):
            i_curr_burn.append(tuple((i[0][0], i[0][1])))

        for i in i_curr_burn:
            curr = self.maze.graph.graph_maze[i[0], i[1]]
            fire_kids = curr.get_children(node = curr, algorithm = self.algorithm)

            for beta in fire_kids:
                if beta is None:
                    continue

                every_kid = beta.get_children(node = beta, algorithm = self.algorithm)

                k = 0
                for kid in every_kid:
                    if kid is None:
                        continue
                    if kid.value == 3:
                        k += 1
                val = np.random.choice(2, 1, [(0.5**k, 1 - (0.5**k))])
                if val[0] == 1:
                    self.maze.wild_fire(beta.row, beta.column)

    def _run_from_fire(self):

        root = self.graph_maze[0, 0]
        dest = self.graph_maze[self.maze.n - 1, self.maze.n - 1]

        # Assign distance from each node to the destination
        for row in range(len(self.maze.maze)):
            for column in range(len(self.maze.maze)):
                if self.maze.maze[row, column] == 0:
                    continue
                self.graph_maze[row, column].distance_from_dest = self._get_euclidien_distance(self.graph_maze[row, column], dest)

        self.fringe = [root]
        self.visited.append(root)
        while self.fringe:

            # Keep track of maximum fringe length
            fringe_length = len(self.fringe)
            if fringe_length >= self.max_fringe_length:
                self.max_fringe_length = fringe_length

            node = self.fringe.pop()

            # update color of the cell and render the maze
            self.maze.update_color_of_cell(node.row, node.column)
            self._charizard()
            self.maze.render_maze()

            # if you reach the destination, then break
            if (node == dest):
                break

            if node not in self.visited:
                self.visited.append(node)

            # If there is no further path, then reset the color of the cell. Also, subsequently reset
            # the color of all parent cells along the path who have no other children to explore.
            flag = True
            while (flag):
                node_children = node.get_children(node = node, algorithm = self.algorithm)
                unvisited_children = self._get_unvisited_children(node_children)

                # If no unvisited children found, then reset the color of this cell in the current path
                # because there is no further path from this cell.
                if len(unvisited_children) == 0:
                    self.maze.reset_color_of_cell(node.row, node.column)
                    self.maze.render_maze()
                else:
                    for child in unvisited_children:
                        child.parent = node
                        self.fringe.append(child)
                    flag = False

                node = node.parent
                if node is None:
                    flag = False

    def run_path_finder_algorithm(self):
        if self.algorithm == self.DfsString:
            self._run_dfs(root = self.graph_maze[0, 0],
                          dest = self.graph_maze[self.maze.n - 1, self.maze.n - 1])
        elif self.algorithm == self.BfsString:
            self._run_bfs(root = self.graph_maze[0, 0],
                          dest = self.graph_maze[self.maze.n - 1, self.maze.n - 1])
        elif self.algorithm == self.AStarString:
            self._run_astar(root = self.graph_maze[0, 0],
                            dest = self.graph_maze[self.maze.n - 1, self.maze.n - 1])
        else:
            self._run_from_fire()
        # Get the final path
        self._get_final_path()

        # Create performance metrics
        self._create_performance_metrics()

        if len(self.path) == 1:
            return 0

        # Reverse the final saved path
        self.path = self.path[::-1]

        # Display the final highlighted path
        self.maze.render_maze(timer = 0.1)
        return 1
