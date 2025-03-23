import pygame

# Initialize Pygame
pygame.init()

# Set up screen and clock
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Default settings
radius = 15
drawing_mode = 'pencil'  # Modes: 'pencil', 'rectangle', 'circle', 'eraser'
current_color = BLUE
start_pos = None
rect_start = None

def main():
    global radius, drawing_mode, current_color, rect_start

    points = []  # Stores points for pencil tool (line drawing)
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Switch between tools
                if event.key == pygame.K_p:  # Pencil tool (draw lines)
                    drawing_mode = 'pencil'
                elif event.key == pygame.K_r:  # Rectangle tool
                    drawing_mode = 'rectangle'
                elif event.key == pygame.K_c:  # Circle tool
                    drawing_mode = 'circle'
                elif event.key == pygame.K_e:  # Eraser tool
                    drawing_mode = 'eraser'
                elif event.key == pygame.K_b:  # Blue color
                    current_color = BLUE
                elif event.key == pygame.K_g:  # Green color
                    current_color = GREEN
                elif event.key == pygame.K_r:  # Red color
                    current_color = RED

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to start drawing
                    if drawing_mode == 'pencil':
                        points.append(event.pos)
                    elif drawing_mode == 'rectangle':
                        rect_start = event.pos
                    elif drawing_mode == 'circle':
                        rect_start = event.pos
                    elif drawing_mode == 'eraser':
                        erase(event.pos)

            if event.type == pygame.MOUSEMOTION:
                if drawing_mode == 'pencil' and pygame.mouse.get_pressed()[0]:
                    points.append(event.pos)

                if drawing_mode == 'rectangle' and rect_start:
                    # Draw rectangle as mouse moves
                    drawRectangle(rect_start, event.pos)
                elif drawing_mode == 'circle' and rect_start:
                    # Draw circle as mouse moves
                    drawCircle(rect_start, event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing_mode == 'rectangle' and rect_start:
                    # Draw the final rectangle on mouse release
                    drawRectangle(rect_start, event.pos)
                    rect_start = None
                elif drawing_mode == 'circle' and rect_start:
                    # Draw the final circle on mouse release
                    drawCircle(rect_start, event.pos)
                    rect_start = None

        # Draw pencil points
        if drawing_mode == 'pencil':
            for i in range(1, len(points)):
                pygame.draw.line(screen, current_color, points[i-1], points[i], radius)

        pygame.display.flip()
        clock.tick(60)

def drawRectangle(start, end):
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    rect = pygame.Rect(start, (width, height))
    pygame.draw.rect(screen, current_color, rect, 3)

def drawCircle(start, end):
    radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
    pygame.draw.circle(screen, current_color, start, radius, 3)

def erase(pos):
    eraser_size = 20  # Size of the eraser
    pygame.draw.circle(screen, WHITE, pos, eraser_size)

if __name__ == "__main__":
    main()
    pygame.quit()
