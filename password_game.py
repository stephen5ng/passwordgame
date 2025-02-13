#!/usr/bin/env python

import aiomqtt
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

BUGS_LIFE = [
    "FLIK",
    "ATTA",
    "DOT",
    "QUEEN",
    "THORNY",
    "CORNELIUS",
    "SOIL",
    "FLORA",
    "APHIE",
    "HOPPER",
    "MOLT",
    "THUMPER",
    "AXLE",
    "LOCO",
    "HEIMLICH",
    "FRANCIS",
    "DIM",
    "SLIM",
    "ROSIE",
    "MANNY",
    "GYPSY",
    "FLEA",
    "TUCK",
    "ROLL",
    "HARRY",
    "THUD",
    "GRUB"
]

rules = [("ENTER A PASSWORD", lambda p: p),
         ("AT LEAST 5 CHARACTERS", lambda p: len(p) >= 5),
         ("MUST CONTAIN A NUMBER", lambda p: bool(re.search(r"\d", p))),
         ("NEEDS UPPERCASE LETTER", lambda p: any(c.isupper() for c in p)),
         ("NEEDS A SPECIAL CHAR", lambda p: any(c in string.punctuation for c in p)),
         ("CHARACTER FROM BUG'S LIFE", lambda p: any(character in p.upper() for character in BUGS_LIFE))
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

      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit(0)

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
