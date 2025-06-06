import math
import re

class PasswordValidator:
    STAR_TREK = [
        "Picard",
        "Lorca",
        "Archer",
        "Kirk",
        "Sulu",
        "Janeway",
        "Spock",
        "Sisko",
        "Pike"
        ]

    EYE_COLORS = [
        "BROWN",
        "BLUE",
        "GREEN"
        ]

    BEATLES = [
        "John",
        "Paul",
        "George",
        "Ringo"
        ]

    BONDS = [
        "Dalton",
        "Lazenby",
        "Connery",
        "Moore",
        "Craig",
        "Brosnan"
        ]

    MATRIX = [
        "Apoc",
        "Choi",
        "Cypher",
        "Dozer",
        "DuFour",
        "Morpheus",
        "Mouse",
        "Neo",
        "Oracle",
        "Rhineheart",
        "Smith",
        "Switch",
        "Tank",
        "Trinity",
    ]
    
    SEVERANCE = [
        "Mark",
        "Helly",
        "Irving",
        "Petey",
        "Dylan",
        "Huang",
        "Casey",
        ]

    def __init__(self):
        self.constraints = [
            self.check_min_length,
            self.check_has_number,
            self.check_has_uppercase,
            self.check_has_special_char,
            self.check_odd_vowels,
            self.check_bond,
            self.check_has_matrix_char,
            self.check_has_roman_numeral,
            self.check_color,
            self.check_has_lost_number,
            self.check_romans_thirtyfive,
            self.check_severance_innie,
            self.check_beatle,
            self.check_prime_length,
            self.check_trek
        ]

    def validate_password(self, password):
        """Validates a password against all constraints.
        Returns (bool, str) tuple - (is_valid, error_message)"""
        if not password:
            return False, ""
            
        for constraint in self.constraints:
            error = constraint(password)
            if error:
                return False, error
                
        return True, ""

    def check_min_length(self, password):
        if len(password) < 5:
            return "Your password must be at least 5 characters."
        return None
    
    def check_has_number(self, password):
        if not any(c.isdigit() for c in password):
            return "Your password must include a number."
        return None
    
    def check_has_uppercase(self, password):
        if not any(c.isupper() for c in password):
            return "Your password must include an uppercase letter."
        return None
    
    def check_has_special_char(self, password):
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        if not any(c in special_chars for c in password):
            return "Your password must contain a special character."
        return None

    def check_odd_vowels(self, password):
        print("check odd vowels")
        if not sum(1 for c in password.lower() if c in "aeiou") % 2 == 1:
            return "Your password must include an odd number of vowels."
        return None
        
    def check_bond(self, password):
        if not any(bond in password for bond in self.BONDS):
            return "Your password must contain the last name of your favorite Bond actor."
        return None

    def check_has_matrix_char(self, password):
        if not any(character in password for character in self.MATRIX):
            return "Your password must contain a character from The Matrix."
        return None
    
    def check_has_roman_numeral(self, password):
        roman_numerals = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
        if not any(c in roman_numerals for c in password):
            return "Your password must include a Roman numeral."
        return None
    
    def check_color(self, password):
        if not any(color in password.upper() for color in self.EYE_COLORS):
            return "Your password must contain the color of your mother's eyes."
        return None

    def check_has_lost_number(self, password):
        lost_numbers = {'4', '8', '15', '16', '23', '42'}
        # Split the password into complete numbers
        potential_numbers = re.findall(r'\d+', password)
        if not any(num in lost_numbers for num in potential_numbers):
            return "Your password must include a number from the TV show LOST."
        return None

    def check_romans_thirtyfive(self, password):
        romans = self._extract_roman_numerals(password)
        numbers = [self._roman_to_int(r) for r in romans]
        print(f"roman numerals: {numbers}")
        product = math.prod(numbers)
        if product != 35:
            return "The Roman numerals in your password should multiply to 35"
        return None

    def check_severance_innie(self, password):
        if not any(character in password for character in self.SEVERANCE):
            return "Your password must include the name of your favorite Severance Innie."
        return None


    def check_beatle(self, password):
        if not any(character in password for character in self.BEATLES):
            return "Your password must contain the name of your college roommate's brother's favorite Beatle."
        return None

    def check_prime_length(self, password):
        length = len(password)
        if not self._is_prime(length):
            return "Your password length must be a prime number."
        return None

    def check_trek(self, password):
        if not any(character in password for character in self.STAR_TREK):
            return ("Your password must contain your youngest sister's first boyfriend\n"
                    "(her first real boyfriend, not that kid she fooled around with in high school)'s\n"
                    "favorite Star Trek captain.")
        return None    

    @staticmethod
    def _is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def _roman_to_int(s):
        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        total = 0
        prev_value = 0

        for char in reversed(s):
            value = roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        return total

    @staticmethod
    def _extract_roman_numerals(text):
        pattern = r'(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))'
        matches = re.finditer(pattern, text)
        roman_numerals = []
        last_end = -1

        for match in matches:
            numeral = match.group(1)
            start = match.start()
            if start > last_end:
                roman_numerals.append(numeral)
                last_end = match.end()

        return [r for r in roman_numerals if r] 