#!/usr/bin/env python

import aiomqtt
import asyncio
from functools import reduce
import os
import platform
import pygame
from pygame import Color
import pygame.freetype
import re
import string
import sys
from typing import Callable

from pygameasync import Clock
from get_key import get_key
import my_inputs
import hub75

SCALING_FACTOR = 9
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32
GUESS_FONT_SIZE = 13
GUESS_FONT_HEIGHT = 9

MQTT_SERVER = os.environ.get("MQTT_SERVER", "localhost")

CURSOR_OFFSET = 1
LINE_SPACING = 2
GUESS_FIRST_LINE_Y = GUESS_FONT_HEIGHT
GUESS_SECOND_LINE_Y = 2 * GUESS_FONT_HEIGHT + LINE_SPACING
MESSAGE_THIRD_LINE_Y = 24

MATRIX = [
    "APOC",
    "CHOI",
    "CYPHER",
    "DOZER",
    "DUFOUR",
    "MORPHEUS",
    "MOUSE",
    "NEO",
    "ORACLE",
    "RHINEHEART",
    "SMITH",
    "SWITCH",
    "TANK",
    "TRINITY",
]

LOST = [4, 8, 15, 16, 23, 42]

SEVERANCE = [
    "MARK",
    "HELLY",
    "IRVING",
    "PETEY",
    "DYLAN",
    "HUANG",
    "CASEY",
    ]

def load_text_file_to_array(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:  # Use utf-8 encoding for broader character support
        lines = file.readlines()  # Read all lines into a list
        lines = [line.strip().upper() for line in lines]
    return lines

palindromes = load_text_file_to_array("palindromes5.txt")

def digits(p):
    return [int(n) for n in re.findall(r"\d+", p)]

def numbers_pow(p):
    numbers = digits(p)
    sum = reduce(lambda x, y: x + y, numbers, 0) if isinstance(numbers, list) else 0
    return (sum & (sum - 1)) == 0

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6  # Skip even numbers and multiples of 3

    return True

def extract_roman_numerals(text):
    # Define a regex pattern for valid Roman numerals
    pattern = r'(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))'

    # Use re.finditer to extract matches
    matches = re.finditer(pattern, text)

    # Extract full Roman numerals
    roman_numerals = []
    last_end = -1

    for match in matches:
        numeral = match.group(1)
        start = match.start()

        # Ensure numerals are not overlapping (prevent partial matches)
        if start > last_end:
            roman_numerals.append(numeral)
            last_end = match.end()

    return [r for r in roman_numerals if r]

def roman_to_int(s):
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    for char in reversed(s):  # Process from right to left
        value = roman_values[char]

        if value < prev_value:
            total -= value  # Subtractive notation (e.g., IV = 4)
        else:
            total += value

        prev_value = value  # Update previous value

    return total

def romans_prime(p):
    romans = extract_roman_numerals(p)
    numbers = [roman_to_int(r) for r in romans]
    s = sum(numbers)
    ip = is_prime(s)
    # print(f"romans:{romans} number:{numbers} sum:{s} is_prime:{ip}")
    return ip

rules = [("ENTER A PASSWORD", lambda p: p),
    ("MUST CONTAIN A NUMBER", lambda p: bool(re.search(r"\d", p))),
    ("AND AN UPPERCASE LETTER", lambda p: any(c.isupper() for c in p)),
    ("ALSO A SPECIAL CHAR", lambda p: any(c in string.punctuation for c in p)),
    ("AND A ROMAN NUMERAL", lambda p: extract_roman_numerals(p)),
    ("AT LEAST 5 CHARACTERS", lambda p: len(p) >= 5),
    ("CHAR FROM *THE MATRIX*", lambda p: any(character in p.upper() for character in MATRIX)),
    ("INCLUDE A PALINDROME", lambda p: any(character in p.upper() for character in palindromes)),
    ("A NUMBER FROM *LOST*", lambda p: set(digits(p)).intersection(set(LOST))),
    ("NAME A SEVERANCE INNIE", lambda p: any(character in p.upper() for character in SEVERANCE)),
    ("AN ODD NUMBER OF VOWELS", lambda p: sum(1 for c in p.lower() if c in "aeiou") % 2 == 1),
    ("NUMBERS SUM TO A POW OF 2", numbers_pow),
    ("ROMAN #'S SUM TO A PRIME", romans_prime),
    ]

quit_app = False

async def trigger_events_from_mqtt(subscribe_client: aiomqtt.Client):
    global quit_app
    async for message in subscribe_client.messages:
        if message.topic.matches("password_game/quit"):
            quit_app = True

async def run_game():
    global quit_app

    clock = Clock()
    pygame.freetype.init()
    display_surface = pygame.display.set_mode(
       (SCREEN_WIDTH*SCALING_FACTOR, SCREEN_HEIGHT*SCALING_FACTOR))

    pygame.display.set_caption('Circus Circus')

    font_guess = pygame.freetype.Font("raize-13.pcf", GUESS_FONT_SIZE)
    char_width = 8

    font_small = pygame.freetype.Font("scientifica-11.bdf", 11)
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    letters = rules[0][0]
    guess = ""
    cursor_pos = 0
    
    # Key repeat settings
    pygame.key.set_repeat(500, 50)  # 500ms initial delay, 50ms repeat interval
    
    # Pre-create cursor surface
    cursor_height = 1
    cursor = pygame.Surface((char_width, cursor_height))
    cursor.fill(Color("green"))
    
    while True:
        if quit_app:
            return
        screen.fill((0, 0, 0))
        show_cursor = (pygame.time.get_ticks()*2 // 1000) % 2 == 0

        # Draw the guess text without cursor
        # r = [x, y, w, h] of rendered text box
        line_surf, r = font_guess.render(guess[:16], Color("green"), Color("black"))
        screen.blit(line_surf, (0, GUESS_FIRST_LINE_Y - r[3]))
        line_surf, r = font_guess.render(guess[16:], Color("green"), Color("black"))
        screen.blit(line_surf, (0, GUESS_SECOND_LINE_Y - r[3]))

        # Draw cursor line if it should be shown
        if show_cursor:
            cursor_y = GUESS_FIRST_LINE_Y + CURSOR_OFFSET if cursor_pos < 16 else GUESS_SECOND_LINE_Y + CURSOR_OFFSET
            cursor_x = (cursor_pos % 16) * char_width
            screen.blit(cursor, (cursor_x, cursor_y))

        font_small.render_to(screen, (0, MESSAGE_THIRD_LINE_Y), letters, Color("red"), Color("black"))

        # Handle pygame events for key repeat
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    guess = ""
                    cursor_pos = 0
                elif event.key == pygame.K_BACKSPACE:
                    if cursor_pos > 0:
                        guess = guess[:cursor_pos-1] + guess[cursor_pos:]
                        cursor_pos -= 1
                elif event.key == pygame.K_LEFT:
                    cursor_pos = max(0, cursor_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_pos = min(len(guess), cursor_pos + 1)
                elif event.key == pygame.K_TAB:
                    continue
                elif len(event.unicode) == 1 and len(guess) < 32:
                    guess = guess[:cursor_pos] + event.unicode + guess[cursor_pos:]
                    cursor_pos = min(cursor_pos + 1, 31)

        # Keep the get_key() for other input handling
        for key in get_key():
            if key == "quit":
                return

        for rule in rules:
            if not rule[1](guess):
                letters = rule[0]
                break
            else:
                letters = "THANK YOU"

        hub75.update(screen)
        pygame.transform.scale(screen,
        display_surface.get_rect().size, dest_surface=display_surface)
        pygame.display.update()
        await clock.tick(30)

async def main():
    async with aiomqtt.Client(MQTT_SERVER) as subscribe_client:
        await subscribe_client.subscribe("#")
        subscribe_task = asyncio.create_task(
            trigger_events_from_mqtt(subscribe_client),
            name="mqtt subscribe handler")

        await run_game()
        subscribe_task.cancel()
        pygame.quit()

if __name__ == "__main__":
    if platform.system() != "Darwin":
        my_inputs.get_key()

    hub75.init()
    pygame.init()

    asyncio.run(main())
