import pygame
import random

pygame.init()
pygame.display.set_caption('Sudoku Generator')
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

# Button class for difficulty selection
class Button:
    def __init__(self, rect, text, color):
        self.rect = rect
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(window_surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, pygame.Color('white'))
        text_rect = text.get_rect(center=self.rect.center)
        window_surface.blit(text, text_rect)

    def is_clicked(self, pos, difficulty_selected):
        if not difficulty_selected:
            return self.rect.collidepoint(pos)
        return False

# Generate puzzle function
def generate_puzzle(difficulty):
    if difficulty == 'easy':
        num_remove = 20
    elif difficulty == 'medium':
        num_remove = 30
    elif difficulty == 'hard':
        num_remove = 40

    grid = generate_grid()
    for _ in range(num_remove):
        while True:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if grid[row][col] != 0:
                grid[row][col] = 0
                break

    return grid

# Generate Sudoku grid
def generate_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_grid(grid)
    return grid

# Fill Sudoku grid using backtracking algorithm
def fill_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for number in numbers:
                    if is_valid(grid, i, j, number):
                        grid[i][j] = number
                        if fill_grid(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True

# Check if a number is valid in a given position
def is_valid(grid, row, col, number):
    if number in grid[row]:
        return False
    if number in [grid[i][col] for i in range(9)]:
        return False
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == number:
                return False
    return True

# Create buttons for difficulty selection
buttons = [
    Button(pygame.Rect(50, 500, 100, 50), 'Easy', pygame.Color('green')),
    Button(pygame.Rect(300, 500, 100, 50), 'Medium', pygame.Color('yellow')),
    Button(pygame.Rect(550, 500, 100, 50), 'Hard', pygame.Color('red'))
]

selected_difficulty = None
grid = None
selected_row = None
selected_col = None

# Timer variables
start_time = pygame.time.get_ticks()
elapsed_time = 0
timer_font = pygame.font.Font(None, 36)

# Check if the puzzle is solved
def is_solved(grid):
    for row in grid:
        if 0 in row:
            return False
    return True

# Draw buttons on the screen
def draw_buttons():
    for button in buttons:
        button.draw()

# Handle puzzle interaction
def handle_puzzle():
    global selected_row, selected_col, selected_difficulty, grid, start_time, elapsed_time
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            selected_row = pos[1] // (600 // 9)
            selected_col = pos[0] // (800 // 9)
            if grid[selected_row][selected_col] == 0:
                # The selected cell is empty, so update the selected cell
                selected_row = pos[1] // (600 // 9)
                selected_col = pos[0] // (800 // 9)
            else:
                # The selected cell is already filled, so clear the selection
                selected_row = None
                selected_col = None

    # Handle interaction with the puzzle here
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        selected_row = pos[1] // (600 // 9)
        selected_col = pos[0] // (800 // 9)
        if grid[selected_row][selected_col] == 0:
            # The selected cell is empty, so update the selected cell
            selected_row = pos[1] // (600 // 9)
            selected_col = pos[0] // (800 // 9)
        else:
            # The selected cell is already filled, so clear the selection
            selected_row = None
            selected_col = None

        # Draw the grid
    for i in range(9):
        for j in range(9):
            cell_value = grid[i][j]
            if cell_value != 0:
                # Draw the filled cell
                cell_rect = pygame.Rect(j * (800 // 9), i * (600 // 9), 800 // 9, 600 // 9)
                pygame.draw.rect(window_surface, pygame.Color('white'), cell_rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(cell_value), True, pygame.Color('black'))
                text_rect = text.get_rect(center=cell_rect.center)
                window_surface.blit(text, text_rect)

    if is_solved(grid):
        elapsed_time = pygame.time.get_ticks() - start_time
        solved_text = timer_font.render("Puzzle Solved! Time: {:.2f}s".format(elapsed_time / 1000), True,
                                        pygame.Color('white'))
        window_surface.blit(solved_text, (250, 250))
    elif selected_row is not None and selected_col is not None:
        if pygame.key.get_pressed()[pygame.K_KP1] or pygame.key.get_pressed()[pygame.K_1]:
            number = 1
        elif pygame.key.get_pressed()[pygame.K_KP2] or pygame.key.get_pressed()[pygame.K_2]:
            number = 2
        elif pygame.key.get_pressed()[pygame.K_KP3] or pygame.key.get_pressed()[pygame.K_3]:
            number = 3
        elif pygame.key.get_pressed()[pygame.K_KP4] or pygame.key.get_pressed()[pygame.K_4]:
            number = 4
        elif pygame.key.get_pressed()[pygame.K_KP5] or pygame.key.get_pressed()[pygame.K_5]:
            number = 5
        elif pygame.key.get_pressed()[pygame.K_KP6] or pygame.key.get_pressed()[pygame.K_6]:
            number = 6
        elif pygame.key.get_pressed()[pygame.K_KP7] or pygame.key.get_pressed()[pygame.K_7]:
            number = 7
        elif pygame.key.get_pressed()[pygame.K_KP8] or pygame.key.get_pressed()[pygame.K_8]:
            number = 8
        elif pygame.key.get_pressed()[pygame.K_KP9] or pygame.key.get_pressed()[pygame.K_9]:
            number = 9
        elif pygame.key.get_pressed()[pygame.K_DELETE] or pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            number = 0
        else:
            number = None

        if number is not None:
            if is_valid(grid, selected_row, selected_col, number):
                grid[selected_row][selected_col] = number
            else:
                # Display an error message if the input is invalid
                error_font = pygame.font.Font(None, 24)
                error_text = error_font.render("Invalid input!", True, pygame.Color('red'))
                window_surface.blit(error_text, (650, 550))
                pygame.display.flip()
                pygame.time.wait(1000)  # Wait for 1 second to display the error message

        # Reset the selected cell
        selected_row = None
        selected_col = None

        # Main game loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if selected_difficulty is None:
                for button in buttons:
                    if button.is_clicked(event.pos, selected_difficulty is not None):
                        selected_difficulty = button.text.lower()
                        grid = generate_puzzle(selected_difficulty)
            else:
                handle_puzzle()

    window_surface.blit(background, (0, 0))
    if selected_difficulty is None:
        draw_buttons()
    else:
        handle_puzzle()

    pygame.display.flip()

pygame.quit()

