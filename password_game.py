#!/usr/bin/env python

import aiomqtt
from functools import reduce
import platform
import pygame
from pygame import Color
import pygame.freetype
import re
import string
import sys

from get_key import get_key
import my_inputs
import hub75

SCALING_FACTOR = 9
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32

if platform.system() != "Darwin":
    my_inputs.get_key()

pygame.init()
hub75.init()

pygame.freetype.init()

display_surface = pygame.display.set_mode(
   (SCREEN_WIDTH*SCALING_FACTOR, SCREEN_HEIGHT*SCALING_FACTOR))

pygame.display.set_caption('Circus Circus')

font_guess = pygame.freetype.Font("raize-13.pcf", 13)
font_small = pygame.freetype.Font("scientifica-11.bdf", 11)
guess = ""

screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

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


rules = [("ENTER A PASSWORD", lambda p: p),
    ("A NUMBER FROM *LOST*", lambda p: set(digits(p)).intersection(set(LOST))),
    ("AT LEAST 5 CHARACTERS", lambda p: len(p) >= 5),
    ("MUST CONTAIN A NUMBER", lambda p: bool(re.search(r"\d", p))),
    ("NEEDS UPPERCASE LETTER", lambda p: any(c.isupper() for c in p)),
    ("INCLUDE A PALINDROME", lambda p: any(character in p.upper() for character in palindromes)),
    ("NEEDS A SPECIAL CHAR", lambda p: any(c in string.punctuation for c in p)),
    ("CHAR FROM *THE MATRIX*", lambda p: any(character in p.upper() for character in MATRIX)),
    ("INCLUDE A SEVERANCE INNIE", lambda p: any(character in p.upper() for character in SEVERANCE)),
    ("NUMBERS SUM TO A POW OF 2", numbers_pow),
    # ("HULZO'S FAVORITE COLOR",)
    ]
letters = rules[0][0]

while True:
    screen.fill((0, 0, 0))
    show_cursor = (pygame.time.get_ticks()*2 // 1000) % 2 == 0
    print_guess = guess + ("_" if show_cursor else " ")
    line_surf, r = font_guess.render(print_guess[:16], Color("green"), Color("black"))
    screen.blit(line_surf, (0, 10-r[1]))
    line_surf, r = font_guess.render(print_guess[16:], Color("green"), Color("black"))
    screen.blit(line_surf, (0, 20-r[1]))
    font_small.render_to(screen, (0, 23), letters, Color("red"), Color("black"))

    for key in get_key():
        if key == "escape":
            guess = ""
        elif key == "backspace":
            guess = guess[:-1]
        elif len(key) == 1:
            guess += key

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
