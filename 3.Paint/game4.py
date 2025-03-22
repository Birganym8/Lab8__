import pygame
import math

# === НАСТРОЙКИ ===
WIDTH, HEIGHT = 1000, 600
ROWS, COLS = 30, 40
PIXEL_SIZE = WIDTH // COLS
DRAW_GRID_LINES = False
TOOLBAR_HEIGHT = HEIGHT - ROWS * PIXEL_SIZE
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BG_COLOR = WHITE

# === Шрифт ===
def get_font(size):
    return pygame.font.SysFont("comicsans", size)

# === Кнопка ===
class Button:
    def __init__(self, x, y, width, height, color, text=None, text_color=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2)
        if self.text:
            button_font = get_font(18)
            text_surface = button_font.render(self.text, 1, self.text_color)
            win.blit(
                text_surface,
                (
                    self.x + self.width / 2 - text_surface.get_width() / 2,
                    self.y + self.height / 2 - text_surface.get_height() / 2,
                ),
            )

    def clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

# === Сетка ===
def init_grid(rows, cols, color):
    return [[color for _ in range(cols)] for _ in range(rows)]

def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

# === Основной отрисовщик ===
def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)
    for button in buttons:
        button.draw(win)
    pygame.display.update()

def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE
    if row >= ROWS:
        raise IndexError
    return row, col

# === Фигуры ===
def draw_square(grid, row, col, color):
    for i in range(3):
        for j in range(3):
            if row + i < ROWS and col + j < COLS:
                grid[row + i][col + j] = color

def draw_right_triangle(grid, row, col, color):
    for i in range(3):
        for j in range(i + 1):
            if row + i < ROWS and col + j < COLS:
                grid[row + i][col + j] = color

def draw_equilateral_triangle(grid, row, col, color):
    # Пирамидка шириной 5
    offsets = [-2, -1, 0, 1, 2]
    for i in range(3):
        for j in range(-i, i + 1):
            r, c = row + i, col + j
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r][c] = color

def draw_rhombus(grid, row, col, color):
    # Алмазная форма из 5 точек
    offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in offsets:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid[r][c] = color

# === Основная функция ===
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Drawing Program - Lab 8 Extended")
    clock = pygame.time.Clock()

    grid = init_grid(ROWS, COLS, BG_COLOR)
    drawing_color = BLACK
    current_shape = None

    # Кнопки выбора цвета
    button_y = HEIGHT - TOOLBAR_HEIGHT / 2 - 25
    buttons = [
        Button(10, button_y, 50, 50, BLACK),
        Button(70, button_y, 50, 50, RED),
        Button(130, button_y, 50, 50, GREEN),
        Button(190, button_y, 50, 50, BLUE),
        Button(250, button_y, 60, 50, WHITE, "Erase", BLACK),
        Button(320, button_y, 60, 50, WHITE, "Clear", BLACK),

        # Новые кнопки фигур
        Button(400, button_y, 70, 50, WHITE, "Square", BLACK),
        Button(480, button_y, 70, 50, WHITE, "R-Tri", BLACK),
        Button(560, button_y, 70, 50, WHITE, "E-Tri", BLACK),
        Button(640, button_y, 70, 50, WHITE, "Rhombus", BLACK),
    ]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                try:
                    row, col = get_row_col_from_pos(pos)
                    # Рисуем выбранную фигуру
                    if current_shape == "square":
                        draw_square(grid, row, col, drawing_color)
                    elif current_shape == "right_triangle":
                        draw_right_triangle(grid, row, col, drawing_color)
                    elif current_shape == "equilateral_triangle":
                        draw_equilateral_triangle(grid, row, col, drawing_color)
                    elif current_shape == "rhombus":
                        draw_rhombus(grid, row, col, drawing_color)
                    else:
                        grid[row][col] = drawing_color
                except IndexError:
                    for button in buttons:
                        if not button.clicked(pos):
                            continue

                        if button.text == "Clear":
                            grid = init_grid(ROWS, COLS, BG_COLOR)
                            drawing_color = BLACK
                            current_shape = None
                        elif button.text == "Erase":
                            drawing_color = WHITE
                            current_shape = None
                        elif button.text == "Square":
                            current_shape = "square"
                        elif button.text == "R-Tri":
                            current_shape = "right_triangle"
                        elif button.text == "E-Tri":
                            current_shape = "equilateral_triangle"
                        elif button.text == "Rhombus":
                            current_shape = "rhombus"
                        else:
                            drawing_color = button.color
                            current_shape = None

        draw(win, grid, buttons)

    pygame.quit()


if __name__ == "__main__":
    main()
