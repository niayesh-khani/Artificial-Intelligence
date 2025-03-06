import heapq

class GameSolution:
    def __init__(self, game):
        """
        Initialize a GameSolution instance.
        Args:
            game (Game): An instance of the Water Sort game.
        """
        self.game = game  # Store the game instance
        self.solution_found = False  # Flag to indicate if a solution is found
        self.moves = []  # List to store the sequence of moves
        self.visited_states = set()  # Set to store visited states for DFS

    def is_victory(self, tube_colors):
        """
        Check if the current tube configuration is a victory.
        Args:
            tube_colors (List[List[int]]): Current state of the tubes.
        Returns:
            bool: True if the game is in a winning state, else False.
        """
        return self.game.check_victory(tube_colors)

    def get_possible_moves(self, tube_colors):
        """
        Generate all possible moves from the current tube configuration.
        Args:
            tube_colors (List[List[int]]): Current state of the tubes.
        Returns:
            List[Tuple[int, int]]: List of possible moves (source, destination).
        """
        moves = []
        for i in range(len(tube_colors)):
            if tube_colors[i]:  # Source tube must have at least one color
                for j in range(len(tube_colors)):
                    # Destination tube must be different, not full, and either empty or have the same color on top
                    if i != j and (not tube_colors[j] or (len(tube_colors[j]) < self.game.NColorInTube and tube_colors[j][-1] == tube_colors[i][-1])):
                        moves.append((i, j))  # Append the move (source, destination)
        return moves

    def make_move(self, tube_colors, move):
        """
        Apply a move to the tube configuration.
        Args:
            tube_colors (List[List[int]]): Current state of the tubes.
            move (Tuple[int, int]): Move to apply (source, destination).
        Returns:
            List[List[int]]: New state of the tubes after the move.
        """
        new_tube_colors = [tube[:] for tube in tube_colors]  # Deep copy to avoid modifying the original state
        src, dst = move  # Unpack the move
        color = new_tube_colors[src].pop()  # Remove the top color from the source tube
        new_tube_colors[dst].append(color)  # Add the top color to the destination tube
        return new_tube_colors

    def solve(self, tube_colors):
        """
        Find any solution to the puzzle using DFS.
        Args:
            tube_colors (List[List[int]]): Initial state of the tubes.
        """
        def dfs(current_colors, path):
            """
            Depth-first search to find a solution.
            Args:
                current_colors (List[List[int]]): Current state of the tubes.
                path (List[Tuple[int, int]]): Current path of moves.
            Returns:
                bool: True if a solution is found, else False.
            """
            if self.is_victory(current_colors):
                self.solution_found = True  # Set the solution found flag
                self.moves = path  # Record the path of moves
                return True
            for move in self.get_possible_moves(current_colors):
                next_colors = self.make_move(current_colors, move)  # Apply the move
                colors_tuple = tuple(tuple(tube) for tube in next_colors)  # Convert to tuple for immutability and hashing
                if colors_tuple not in self.visited_states:  # Check if the state is not visited
                    self.visited_states.add(colors_tuple)  # Add the state to visited
                    if dfs(next_colors, path + [move]):  # Recur with the new state and updated path
                        return True
            return False

        initial_state = tuple(tuple(tube) for tube in tube_colors)  # Initial state as tuple
        self.visited_states.add(initial_state)  # Add initial state to visited
        dfs(tube_colors, [])  # Start DFS from the initial state

    def heuristic(self, tube_colors):
        """
        Heuristic function to estimate the distance to the goal.
        Args:
            tube_colors (List[List[int]]): Current state of the tubes.
        Returns:
            int: Estimated distance to the goal.
        """
        misplaced_tubes = 0
        incomplete_tubes = 0
        for tube in tube_colors:
            if tube and len(set(tube)) > 1:  # Tube contains multiple colors
                misplaced_tubes += 1
            if tube and (0 < len(set(tube)) < self.game.NColorInTube):  # Tube is not completely filled with one color
                incomplete_tubes += 1
        return misplaced_tubes + incomplete_tubes  # Sum of misplaced and incomplete tubes

    def optimal_solve(self, tube_colors):
        """
        Find the optimal solution to the puzzle using A* search.
        Args:
            tube_colors (List[List[int]]): Initial state of the tubes.
        """
        def a_star_search(start_colors):
            """
            A* search to find the optimal solution.
            Args:
                start_colors (List[List[int]]): Initial state of the tubes.
            Returns:
                bool: True if a solution is found, else False.
            """
            initial_state = tuple(tuple(tube) for tube in start_colors)  # Initial state as tuple
            g = {initial_state: 0}  # Cost from start to the current state
            h = {initial_state: self.heuristic(start_colors)}  # Heuristic cost estimate to the goal
            f = {initial_state: g[initial_state] + h[initial_state]}  # Total estimated cost
            priority_queue = [(f[initial_state], start_colors, [])]  # Priority queue with initial state
            visited = set()  # Set to store visited states
            visited.add(initial_state)  # Add initial state to visited

            while priority_queue:
                _, current_colors, path = heapq.heappop(priority_queue)  # Pop the state with the lowest cost
                if self.is_victory(current_colors):
                    self.solution_found = True  # Set the solution found flag
                    self.moves = path  # Record the path of moves
                    return True

                for move in self.get_possible_moves(current_colors):
                    next_colors = self.make_move(current_colors, move)  # Apply the move
                    colors_tuple = tuple(tuple(tube) for tube in next_colors)  # Convert to tuple for immutability and hashing
                    if colors_tuple not in visited:  # Check if the state is not visited
                        visited.add(colors_tuple)  # Add the state to visited
                        g[colors_tuple] = g[tuple(tuple(tube) for tube in current_colors)] + 1  # Update cost from start to the current state
                        h[colors_tuple] = self.heuristic(next_colors)  # Calculate heuristic cost estimate to the goal
                        f[colors_tuple] = g[colors_tuple] + h[colors_tuple]  # Calculate total estimated cost
                        heapq.heappush(priority_queue, (f[colors_tuple], next_colors, path + [move]))  # Push the new state to the priority queue
            return False

        a_star_search(tube_colors)  # Start A* search from the initial state
