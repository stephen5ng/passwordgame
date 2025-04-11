#!/usr/bin/env python3
import pygame
import pygame_gui
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Login")

# Create UI manager
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# Create UI elements
input_width = 300
input_height = 40
spacing = 20

# Calculate positions
username_y = WINDOW_HEIGHT // 2 - input_height - spacing
password_y = WINDOW_HEIGHT // 2 + spacing
x_pos = (WINDOW_WIDTH - input_width) // 2

# Create text entry lines
username_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((x_pos, username_y), (input_width, input_height)),
    manager=manager,
    placeholder_text="Username"
)

password_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((x_pos, password_y), (input_width, input_height)),
    manager=manager,
    placeholder_text="Password"
)
password_entry.set_text_hidden(True)  # Hide password text

# Create labels
username_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((x_pos, username_y - 30), (input_width, 25)),
    text="Username:",
    manager=manager
)

password_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((x_pos, password_y - 30), (input_width, 25)),
    text="Password:",
    manager=manager
)

# Create login button
login_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((x_pos, password_y + input_height + 20), (input_width, 40)),
    text="Login",
    manager=manager
)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(30) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == login_button:
                username = username_entry.get_text()
                password = password_entry.get_text()
                if username == 'jhulzo' and password == 'password':
                    running = False
                else:
                    password_entry.focus()
                    password_entry.select_range = (0, len(password_entry.get_text()))

        manager.process_events(event)

    manager.update(time_delta)

    # Clear screen
    screen.fill(WHITE)
    
    # Draw UI
    manager.draw_ui(screen)
    
    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit() 