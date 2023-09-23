import tkinter as tk
import random
import time

# Constants
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
SPEED = 0.4  # Adjust this for snake speed
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
BLACK = "black"
WHITE = "white"
GREEN = "green"

# Directions
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.canvas = tk.Canvas(self, bg=BLACK)
        self.canvas.pack()
        self.snake = [(2, 2)]
        self.food = self.new_food_position()
        self.direction = RIGHT
        self.score = 0
        self.bind("<Key>", self.change_direction)
        self.game_over = False
        self.update()

    def new_food_position(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def change_direction(self, event):
        key = event.keysym
        if (key == "Up" or key == "w") and self.direction != DOWN:
            self.direction = UP
        elif (key == "Down" or key == "s") and self.direction != UP:
            self.direction = DOWN
        elif (key == "Left" or key == "a") and self.direction != RIGHT:
            self.direction = LEFT
        elif (key == "Right" or key == "d") and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        head_x, head_y = self.snake[0]
        if self.direction == UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == LEFT:
            new_head = (head_x - 1, head_y)
        elif self.direction == RIGHT:
            new_head = (head_x + 1, head_y)

        # Check if the snake hit the wall or itself
        if (
            new_head in self.snake
            or new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check if the snake ate the food
        if new_head == self.food:
            self.score += 1
            self.food = self.new_food_position()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=GREEN,
            )
        x, y = self.food
        self.canvas.create_oval(
            x * CELL_SIZE,
            y * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            fill=WHITE,
        )

    def update(self):
        if not self.game_over:
            self.move()
            self.draw()
            self.after(int(SPEED * 1000), self.update)
        else:
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2,
                text=f"Game Over\nScore: {self.score}",
                fill=WHITE,
                font=("Helvetica", 20),
                justify="center",
            )

if __name__ == "__main__":
    app = SnakeGame()
    app.mainloop()
