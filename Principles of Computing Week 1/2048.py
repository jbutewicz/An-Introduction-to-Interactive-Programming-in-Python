# Clone of 2048 game for Principles of Computing Coursera class
# @jbutewicz

import poc_2048_gui   
import random     

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    # Helper function that merges a single row or column in 2048
    # Move all non-zero values of list to the left
    nonzeros_removed = []
    result = []
    merged = False
    for number in line:
        if number != 0:
            nonzeros_removed.append(number)

    while len(nonzeros_removed) != len(line):
        nonzeros_removed.append(0)
        
    # Double sequental tiles if same value
    for number in range(0, len(nonzeros_removed) - 1):
        if nonzeros_removed[number] == nonzeros_removed[number + 1] and merged == False:
            result.append(nonzeros_removed[number] * 2)
            merged = True
        elif nonzeros_removed[number] != nonzeros_removed[number + 1] and merged == False:
            result.append(nonzeros_removed[number])
        elif merged == True:
            merged = False
    
    if nonzeros_removed[-1] != 0 and merged == False:
        result.append(nonzeros_removed[-1])

    while len(result) != len(nonzeros_removed):
        result.append(0)

    return result

class TwentyFortyEight:
    # Class to run the game logic.

    def __init__(self, grid_height, grid_width):
        # Initialize class
        self.grid_height = grid_height
        self.grid_width = grid_width
		self.cells = []
        self.reset()

		# Compute inital row dictionary to make move code cleaner
		self.initial = {
			UP : [[0,element] for element in range(self.get_grid_width())],
			DOWN : [[self.get_grid_height() - 1, element] for element in range(self.get_grid_width())],
			LEFT : [[element, 0] for element in range(self.get_grid_height())],
			RIGHT : [[element, self.get_grid_width() - 1] for element in range (self.get_grid_height())]
		}
		
    def reset(self):
        # Reset the game so the grid is empty.
        self.cells = [[0 for col in range(self.get_grid_height())] for row in range(self.get_grid_width())]
        
    def __str__(self):
        # Print a string representation of the grid for debugging.
        for number in range(0, self.get_grid_height()):
            print self.cells[number]
    
    def get_grid_height(self):
        # Get the height of the board.
        return self.grid_height
    
    def get_grid_width(self):
        # Get the width of the board.
        return self.grid_width

    def move(self, direction):
        # Move all tiles in the given direction and add
        # a new tile if any tiles moved.
		initial_list = self.initial[direction]
		temporary_list = []

		if(direction == UP):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_height())
		elif(direction == DOWN):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_height())
		elif(direction == LEFT):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_width())
		elif(direction == RIGHT):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_width())
			
	def move_helper(self, initial_list, direction, temporary_list, row_or_column):
		# Move all columns and merge
		before_move = str(self.cells)

		for element in initial_list:
			temporary_list.append(element)
			
			for index in range(1, row_or_column):
				temporary_list.append([x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])
			
			indices = []
			
			for index in temporary_list:
				indices.append(self.get_tile(index[0], index[1]))
			
			merged_list = merge(indices)
			
			for index_x, index_y in zip(merged_list, temporary_list):
				self.set_tile(index_y[0], index_y[1], index_x)
		
			temporary_list = []
		
		after_move = str(self.cells)
		
		if before_move != after_move:
			self.new_tile()
				
    def new_tile(self):
        # Create a new tile in a randomly selected empty 
        # square.  The tile should be 2 90% of the time and
        # 4 10% of the time.
        available_positions = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] == 0:
                    available_positions.append([row, col])
 
        if not available_positions:
            print "There are no available positions."
        else:
            random_tile = random.choice(available_positions)
 
			weighted_choices = [(2, 9), (4, 1)]
			population = [val for val, cnt in weighted_choices for i in range(cnt)]
			tile = random.choice(population)

            self.set_tile(random_tile[0],random_tile[1], tile)
        
    def set_tile(self, row, col, value):
        # Set the tile at position row, col to have the given value.
        self.cells[row][col] = value
            
    def get_tile(self, row, col):
        # Return the value of the tile at position row, col.
        return self.cells[row][col]
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))