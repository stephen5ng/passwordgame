import my_inputs
import platform
import pygame
import sys

shifted = {
   "`": "~",
   "1": "!",
   "2": "@",
   "3": "#",
   "4": "$",
   "5": "%",
   "6": "^",
   "7": "&",
   "8": "*",
   "9": "(",
   "0": ")",
   "-": "_",
   "=": "+",
   "[": "{",
   "]": "}",
   "\\": "|",
   ",": "<",
   ".": ">",
   "/": "?"
}

NAMES_TO_KEYS = {
    "SPACE": " ",
    "GRAVE": "`",
    "LEFTBRACE": "{",
    "RIGHTBRACE": "}",
    "SEMICOLON": ";",
    "APOSTROPHE": "'",
    "COMMA": ",",
    "DOT": ".",
    "SLASH": "/"
}

is_shifted = False
def get_key():
    global is_shifted
    if platform.system() != "Darwin":
        events = my_inputs.get_key()
        if not events:
            return
        for event in events:
            if event.ev_type == "Key":
                key = event.code[4:]
                if key in NAMES_TO_KEYS.keys():
                    key = NAMES_TO_KEYS[key]

                if "SHIFT" in key:
                    is_shifted = False if event.state == 0 else True
                elif event.state:
                    if len(key) == 1:
                        if key.isalpha():
                            yield key.upper() if shifted else key
                        elif is_shifted and key in shifted.keys():
                    else:
                        yield key
        return

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if len(key) == 1:
                is_shifted = 0 != pygame.key.get_mods() & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT)
                print(f"shifted: {is_shifted} K: {key} alpha: {key.isalpha()}")
                if key.isalpha():
                    yield key.upper() if is_shifted else key.lower()
                elif is_shifted and key in shifted.keys():
                    yield shifted[key]
                else:
                    yield key
            else:
                yield key
        elif event.type == pygame.QUIT:
             pygame.quit()
             sys.exit(0)