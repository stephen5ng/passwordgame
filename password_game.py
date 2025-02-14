#!/usr/bin/env python

import aiomqtt
from functools import reduce
import pygame
from pygame import Color
import pygame.freetype
import re
import string
import sys
import hub75

SCALING_FACTOR = 9
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32

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

shifted = {
   "1": "!",
   "/": "?",
   "-": "_",
   "=": "+"
}

MATRIX = [
    "NEO",
    "TRINITY",
    "MORPHEUS",
    "SMITH",
    "ORACLE",
    "CYPHER",
    "TANK",
    "DOZER",
    "APOC",
    "SWITCH",
    "MOUSE",
    "RHINEHEART",
    "CHOI",
    "DUFOUR"
]

LOST = [ "4", "8", "15", "16", "23", "42"]

def load_text_file_to_array(filepath):
     with open(filepath, 'r', encoding='utf-8') as file:  # Use utf-8 encoding for broader character support
         lines = file.readlines()  # Read all lines into a list
         lines = [line.strip().upper() for line in lines]
         return lines

palindromes = load_text_file_to_array("palindromes5.txt")

def numbers_pow(p):
   numbers = [int(n) for n in re.findall(r"\d+", p)]
   print(f"numbers: {numbers}")
   sum = reduce(lambda x, y: x + y, numbers, 0) if isinstance(numbers, list) else 0
   print(f"sum: {sum}")
   return (sum & (sum - 1)) == 0
   # return True


rules = [("ENTER A PASSWORD", lambda p: p),
         ("AT LEAST 5 CHARACTERS", lambda p: len(p) >= 5),
         ("MUST CONTAIN A NUMBER", lambda p: bool(re.search(r"\d", p))),
         ("NEEDS UPPERCASE LETTER", lambda p: any(c.isupper() for c in p)),
         ("NEEDS A SPECIAL CHAR", lambda p: any(c in string.punctuation for c in p)),
         ("A NUMBER FROM *LOST*", lambda p: any(character in p.upper() for character in LOST)),
         ("CHAR FROM *THE MATRIX*", lambda p: any(character in p.upper() for character in MATRIX)),
         ("INCLUDE A PALINDROME", lambda p: any(character in p.upper() for character in palindromes)),
         ("NUMBERS SUM TO A POW OF 2", numbers_pow),
         # ("HULZO'S FAVORITE COLOR",)
         ]
letters = rules[0][0]

while True:
   screen.fill((0, 0, 0))
   show_cursor = (pygame.time.get_ticks()*2 // 1000) % 2 == 0
   print_guess = guess + ("_" if show_cursor else " ")
   first_y = 0 if guess else 10
   # for some weird reason font.render skips the first empty space
   font_guess.render_to(screen, (0, first_y), print_guess[:16], Color("green"), Color("black"))
   font_guess.render_to(screen, (0, 10), print_guess[16:], Color("green"), Color("black"))
   font_small.render_to(screen, (0, 23), letters, Color("red"), Color("black"))

   for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
         key = pygame.key.name(event.key).upper()
         print(f"{key}")
         if event.key == pygame.K_ESCAPE:
            guess = ""
         elif event.key == pygame.K_BACKSPACE:
            guess = guess[:-1]
         elif event.key == pygame.K_SPACE:
            guess += ' '
         elif event.unicode:  # Check if it's a valid unicode character
            unicode_char = event.unicode  # Use event.unicode for characters
            guess += unicode_char

         for rule in rules:
            if not rule[1](guess):
               letters = rule[0]
               break
         else:
            letters = "THANK YOU"
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit(0)

   hub75.update(screen)
   pygame.transform.scale(screen,
   display_surface.get_rect().size, dest_surface=display_surface)
   pygame.display.update()
