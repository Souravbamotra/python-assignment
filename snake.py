
import tkinter as tk
import random

# Constants for game settings
WIDTH = 500  # Width of the game window
HEIGHT = 500  # Height of the game window
CELL_SIZE = 20  # Size of each cell in the grid

class SnakeGame:
    def _init_(self, root):
        """Initialize the game window and variables."""
        self.root = root
        self.root.title("Snake Game")
        
        # Create canvas for game rendering
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        # Initialize snake (list of tuples representing its body parts)
        self.snake = [(100, 100), (90, 100), (80, 100)]
        
        # Generate initial food position
        self.food = self.create_food()


        
        
        # Set initial movement direction
        self.direction = "Right"
        self.running = True
        
        # Bind keyboard events for direction changes
        self.root.bind("<KeyPress>", self.change_direction)
        
        # Start game loop
        self.update_game()
    
    def create_food(self):
        """Generate a new food position at a random location on the grid."""
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        return (x, y)
    
    def change_direction(self, event):
        """Change the direction of the snake based on user input."""
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            # Prevent the snake from reversing direction
            opposite_directions = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
            if opposite_directions.get(event.keysym) != self.direction:
                self.direction = event.keysym
    
    def move_snake(self):
        """Move the snake in the current direction and handle collisions."""
        head_x, head_y = self.snake[0]
        
        # Determine new head position based on direction
        if self.direction == "Left":
            head_x -= CELL_SIZE
        elif self.direction == "Right":
            head_x += CELL_SIZE
        elif self.direction == "Up":
            head_y -= CELL_SIZE
        elif self.direction == "Down":
            head_y += CELL_SIZE
        
        new_head = (head_x, head_y)
        
        # Check for collisions with walls or itself
        if (
            new_head in self.snake or
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT
        ):
            self.running = False
            return
        
        # Insert new head at the front of the snake
        self.snake.insert(0, new_head)
        
        # Check if snake has eaten food
        if new_head == self.food:
            self.food = self.create_food()  # Generate new food
        else:
            self.snake.pop()  # Remove tail segment to maintain length
    
    def draw_elements(self):
        """Render the snake and food on the canvas."""
        self.canvas.delete("all")  # Clear canvas before drawing
        
        # Draw snake body
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green")
        
        # Draw food
        food_x, food_y = self.food
        self.canvas.create_oval(food_x, food_y, food_x + CELL_SIZE, food_y + CELL_SIZE, fill="red")
    
    def update_game(self):
        """Update the game state and refresh the screen."""
        if self.running:
            self.move_snake()
            self.draw_elements()
            self.root.after(100, self.update_game)  # Schedule next update
        else:
            # Display Game Over message
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=("Arial", 20))

if _name_ == "_main_":
    # Create game window and start game loop
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()