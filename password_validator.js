class PasswordValidator {
    constructor() {
        this.STAR_TREK = [
            "Picard", "Lorca", "Archer", "Kirk", "Sulu",
            "Janeway", "Spock", "Sisko", "Pike"
        ];

        this.EYE_COLORS = ["BROWN", "BLUE", "GREEN", "HAZEL"];

        this.BEATLES = ["John", "Paul", "George", "Ringo"];

        this.BONDS = [
            "Dalton", "Lazenby", "Connery", "Moore",
            "Craig", "Brosnan"
        ];

        this.MATRIX = [
            "Apoc", "Choi", "Cypher", "Dozer", "DuFour",
            "Morpheus", "Mouse", "Neo", "Oracle", "Rhineheart",
            "Smith", "Switch", "Tank", "Trinity"
        ];

        this.SEVERANCE = [
            "Mark", "Helly", "Irving", "Petey",
            "Dylan", "Huang", "Casey"
        ];
    }

    validatePassword(password) {
        const constraints = [
            this.checkMinLength,
            this.checkHasNumber,
            this.checkHasUppercase,
            this.checkHasSpecialChar,
            this.checkOddVowels,
            this.checkBond,
            this.checkHasMatrixChar,
            this.checkHasRomanNumeral,
            this.checkColor,
            this.checkHasLostNumber,
            this.checkRomansThirtyFive,
            this.checkSeveranceInnie,
            this.checkBeatle,
            this.checkPrimeLength,
            this.checkTrek
        ];

        if (!password) {
            return [false, "Password is required"];
        }

        for (const constraint of constraints) {
            const error = constraint.call(this, password);
            if (error) {
                return [false, error];
            }
        }

        return [true, ""];
    }

    checkMinLength(password) {
        return password.length < 5 ? "Your password must be at least 5 characters." : null;
    }

    checkHasNumber(password) {
        return /\d/.test(password) ? null : "Your password must include a number.";
    }

    checkHasUppercase(password) {
        return /[A-Z]/.test(password) ? null : "Your password must include an uppercase letter.";
    }

    checkHasSpecialChar(password) {
        return /[!@#$%^&*()\-_=+\[\]{}|;:,.<>?/]/.test(password) ?
            null : "Your password must contain a special character.";
    }

    checkHasRomanNumeral(password) {
        return /[IVXLCDM]/.test(password) ?
            null : "Your password must include a Roman numeral.";
    }

    checkHasMatrixChar(password) {
        return this.MATRIX.some(char => password.includes(char)) ?
            null : "Your password must contain a character from The Matrix.";
    }

    checkTrek(password) {
        return this.STAR_TREK.some(char => password.includes(char)) ?
            null : ("Your password must contain your youngest sister's first boyfriend<br/>"  +
                    "(her first real boyfriend, not that kid she fooled around with in high school)'s<br/>" +
                    "favorite Star Trek captain.");
    }

    checkColor(password) {
        return this.EYE_COLORS.some(color => password.toUpperCase().includes(color)) ?
            null : "Your password must contain the color of your mother's eyes.";
    }

    checkBeatle(password) {
        return this.BEATLES.some(beatle => password.includes(beatle)) ?
            null : "Your password must contain the name of your college roommate's brother's favorite Beatle.";
    }

    checkBond(password) {
        return this.BONDS.some(bond => password.includes(bond)) ?
            null : "Your password must contain the last name of your favorite Bond actor.";
    }

    checkHasLostNumber(password) {
        const lostNumbers = ['4', '8', '15', '16', '23', '42'];
        const numbers = password.match(/\d+/g) || [];
        return numbers.some(num => lostNumbers.includes(num)) ?
            null : "Your password must include a number from the TV show LOST.";
    }

    checkRomansThirtyFive(password) {
        const romans = this.extractRomanNumerals(password);
        const numbers = romans.map(r => this.romanToInt(r));
        const product = numbers.reduce((a, b) => a * b, 1);
        return product === 35 ?
            null : "The Roman numerals in your password should multiply to 35";
    }

    checkSeveranceInnie(password) {
        return this.SEVERANCE.some(char => password.includes(char)) ?
            null : "Your password must include the name of your favorite Severance Innie.";
    }

    checkOddVowels(password) {
        const vowelCount = (password.match(/[aeiou]/gi) || []).length;
        return vowelCount % 2 === 1 ?
            null : "Your password must include an odd number of vowels.";
    }

    checkPrimeLength(password) {
        return this.isPrime(password.length) ?
            null : "Your password length must be a prime number.";
    }

    isPrime(n) {
        if (n < 2) return false;
        for (let i = 2; i <= Math.sqrt(n); i++) {
            if (n % i === 0) return false;
        }
        return true;
    }

    romanToInt(s) {
        const romanValues = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        };

        let total = 0;
        let prevValue = 0;

        for (let i = s.length - 1; i >= 0; i--) {
            const value = romanValues[s[i]];
            if (value < prevValue) {
                total -= value;
            } else {
                total += value;
            }
            prevValue = value;
        }

        return total;
    }

    extractRomanNumerals(text) {
        const pattern = /(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))/g;
        const matches = text.match(pattern) || [];
        return matches.filter(Boolean);
    }
}

// Initialize validator and handle input changes
const validator = new PasswordValidator();

document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password');
    const errorElement = document.getElementById('errorMessage');
    const successElement = document.getElementById('successMessage');
    const submitButton = document.getElementById('submitButton');
    
    // Add input event listener for real-time validation
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        const [isValid, errorMessage] = validator.validatePassword(password);
        
        if (!isValid) {
            errorElement.textContent = errorMessage;
            successElement.textContent = '';
            submitButton.disabled = true;
        } else {
            errorElement.textContent = '';
            successElement.textContent = 'Password is valid!';
            submitButton.disabled = false;
        }
    });

    // Add click handler for submit button
    submitButton.addEventListener('click', () => {
        const password = passwordInput.value;
        const [isValid] = validator.validatePassword(password);
        
        if (isValid) {
            // Here you would typically send the password to your server
            alert('Password changed successfully!');
            passwordInput.value = '';
            successElement.textContent = '';
            submitButton.disabled = true;
        }
    });
}); 