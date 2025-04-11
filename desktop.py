#!/usr/bin/env python3
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Login")

# Font setup
font = pygame.font.SysFont('Arial', 32)
label_font = pygame.font.SysFont('Arial', 24)

# Input box properties
input_width = 300
input_height = 40
spacing = 20

username_box = pygame.Rect(
    (WINDOW_WIDTH - input_width) // 2,
    WINDOW_HEIGHT // 2 - input_height - spacing,
    input_width,
    input_height
)
password_box = pygame.Rect(
    (WINDOW_WIDTH - input_width) // 2,
    WINDOW_HEIGHT // 2 + spacing,
    input_width,
    input_height
)

color_inactive = GRAY
color_active = BLUE

# Input states
username = ''
password = ''
active_field = 'username'  # Set username field as active by default
clock = pygame.time.Clock()
cursor_visible = True
last_cursor_toggle = time.time()
password_selected = False  # Track if password text is selected

# Main game loop
running = True
while running:
    current_time = time.time()
    if current_time - last_cursor_toggle > 0.5:  # Toggle cursor every 0.5 seconds
        cursor_visible = not cursor_visible
        last_cursor_toggle = current_time
    print(f"password: {password}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check which field was clicked
            if username_box.collidepoint(event.pos):
                active_field = 'username'
                password_selected = False
            elif password_box.collidepoint(event.pos):
                active_field = 'password'
                password_selected = False
            else:
                active_field = None
                password_selected = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Switch between fields when tab is pressed
                if active_field == 'username':
                    active_field = 'password'
                else:
                    active_field = 'username'
                password_selected = False
            elif active_field:
                if event.key == pygame.K_RETURN:
                    if username == 'jhulzo' and password == 'password':
                        running = False
                    else:
                        active_field = 'password'
                        password_selected = True
                    print(f"Username: {username}")
                    print(f"Password: {password}")
                    if username == 'jhulzo' and password == 'password':
                        username = ''
                        password = ''
                elif event.key == pygame.K_BACKSPACE:
                    if active_field == 'username':
                        username = username[:-1]
                    else:
                        password = password[:-1]
                    password_selected = False
                else:
                    if active_field == 'username':
                        username += event.unicode
                    else:
                        password += event.unicode
                    password_selected = False

    # Clear screen
    screen.fill(WHITE)
    
    # Draw labels
    username_label = label_font.render("Username:", True, BLACK)
    password_label = label_font.render("Password:", True, BLACK)
    
    screen.blit(username_label, (username_box.x, username_box.y - 30))
    screen.blit(password_label, (password_box.x, password_box.y - 30))
    
    # Render the text
    username_surface = font.render(username, True, BLACK)
    password_surface = font.render('*' * len(password), True, BLACK)
    
    # Draw the input boxes
    username_color = color_active if active_field == 'username' else color_inactive
    password_color = color_active if active_field == 'password' else color_inactive
    
    pygame.draw.rect(screen, username_color, username_box, 2)
    pygame.draw.rect(screen, password_color, password_box, 2)
    
    # Draw text and cursor
    if active_field == 'username':
        screen.blit(username_surface, (username_box.x + 5, username_box.y + 5))
        if cursor_visible and not password_selected:
            cursor_x = username_box.x + 5 + username_surface.get_width()
            pygame.draw.line(screen, BLACK, 
                           (cursor_x, username_box.y + 5),
                           (cursor_x, username_box.y + input_height - 5), 2)
    else:
        screen.blit(username_surface, (username_box.x + 5, username_box.y + 5))
    
    if active_field == 'password':
        if password_selected:
            # Draw selection background
            pygame.draw.rect(screen, (200, 200, 255), 
                           (password_box.x + 5, password_box.y + 5,
                            password_surface.get_width(), input_height - 10))
        screen.blit(password_surface, (password_box.x + 5, password_box.y + 5))
        if cursor_visible and not password_selected:
            cursor_x = password_box.x + 5 + password_surface.get_width()
            pygame.draw.line(screen, BLACK,
                           (cursor_x, password_box.y + 5),
                           (cursor_x, password_box.y + input_height - 5), 2)
    else:
        screen.blit(password_surface, (password_box.x + 5, password_box.y + 5))
    
    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit() 