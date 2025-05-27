import pytest
from password_validator import PasswordValidator

@pytest.fixture
def validator():
    return PasswordValidator()

def test_check_min_length(validator):
    # Test strings shorter than 5 chars
    assert validator.check_min_length("") is not None
    assert validator.check_min_length("abc") is not None
    assert validator.check_min_length("1234") is not None
    
    # Test strings of exactly 5 chars and longer
    assert validator.check_min_length("12345") is None
    assert validator.check_min_length("123456") is None

def test_check_has_number(validator):
    # Test strings without numbers
    assert validator.check_has_number("abcde") is not None
    assert validator.check_has_number("!@#$%") is not None
    
    # Test strings with numbers
    assert validator.check_has_number("abc123") is None
    assert validator.check_has_number("1abcde") is None
    assert validator.check_has_number("abcd5") is None

def test_check_has_uppercase(validator):
    # Test strings without uppercase
    assert validator.check_has_uppercase("abcde") is not None
    assert validator.check_has_uppercase("123!@#") is not None
    
    # Test strings with uppercase
    assert validator.check_has_uppercase("Abcde") is None
    assert validator.check_has_uppercase("abcdE") is None
    assert validator.check_has_uppercase("ABC123") is None

def test_check_has_special_char(validator):
    # Test strings without special chars
    assert validator.check_has_special_char("abcde") is not None
    assert validator.check_has_special_char("abc123") is not None
    assert validator.check_has_special_char("ABC123") is not None
    
    # Test strings with special chars
    assert validator.check_has_special_char("abc!de") is None
    assert validator.check_has_special_char("abc@123") is None
    assert validator.check_has_special_char("abc#ABC") is None

def test_check_has_roman_numeral(validator):
    # Test strings without roman numerals
    assert validator.check_has_roman_numeral("abcde") is not None
    assert validator.check_has_roman_numeral("123!@#") is not None
    
    # Test strings with roman numerals
    assert validator.check_has_roman_numeral("abcIde") is None
    assert validator.check_has_roman_numeral("Vabc123") is None
    assert validator.check_has_roman_numeral("abcXYZ") is None

def test_check_has_matrix_char(validator):
    # Test strings without Matrix characters
    assert validator.check_has_matrix_char("abcde") is not None
    assert validator.check_has_matrix_char("123!@#") is not None
    
    # Test strings with Matrix characters
    assert validator.check_has_matrix_char("NEOabc") is None
    assert validator.check_has_matrix_char("abc123TRINITY") is None
    assert validator.check_has_matrix_char("morpheus123") is None  # Should work case-insensitive

def test_check_has_lost_number(validator):
    # Test strings without Lost numbers
    assert validator.check_has_lost_number("abcde") is not None
    assert validator.check_has_lost_number("123") is not None
    assert validator.check_has_lost_number("789") is not None
    
    # Test strings with Lost numbers
    assert validator.check_has_lost_number("abc4def") is None
    assert validator.check_has_lost_number("abc15def") is None
    assert validator.check_has_lost_number("abc42def") is None

def test_check_romans_thirtyfive(validator):
    # Test strings without roman numerals that multiply to 35
    assert validator.check_romans_thirtyfive("I") is not None  # 1
    assert validator.check_romans_thirtyfive("VI") is not None  # 6
    assert validator.check_romans_thirtyfive("X") is not None  # 10
    
    # Test strings with roman numerals that multiply to 35
    assert validator.check_romans_thirtyfive("XXXV") is None  # 35
    assert validator.check_romans_thirtyfive("VIIpassV") is None  # 7 * 5 = 35

def test_check_severance_innie(validator):
    # Test strings without Severance characters
    assert validator.check_severance_innie("abcde") is not None
    assert validator.check_severance_innie("123!@#") is not None
    
    # Test strings with Severance characters
    assert validator.check_severance_innie("HELLYabc") is None
    assert validator.check_severance_innie("abc123MARK") is None
    assert validator.check_severance_innie("irving123") is None  # Should work case-insensitive

def test_check_prime_length(validator):
    # Test strings with non-prime lengths
    assert validator.check_prime_length("abcd") is not None  # length 4
    assert validator.check_prime_length("abcdef") is not None  # length 6
    assert validator.check_prime_length("abcdefgh") is not None  # length 8
    assert validator.check_prime_length("abcdefghi") is not None  # length 9
    
    # Test strings with prime lengths
    assert validator.check_prime_length("abcde") is None  # length 5
    assert validator.check_prime_length("abcdefg") is None  # length 7
    assert validator.check_prime_length("abcdefghijk") is None  # length 11

def test_validate_password(validator):
    # Test an invalid password missing various requirements
    is_valid, error = validator.validate_password("abc")
    assert not is_valid
    assert error is not None
    
    # Test a valid password meeting all requirements
    valid_password = "abcde5K$VNeo4VIIMarkjjj"
    is_valid, error = validator.validate_password(valid_password)
    assert is_valid
    assert error == ""

def test_utility_methods(validator):
    # Test _is_prime
    assert validator._is_prime(2)
    assert validator._is_prime(3)
    assert validator._is_prime(5)
    assert validator._is_prime(7)
    assert validator._is_prime(11)
    assert not validator._is_prime(1)
    assert not validator._is_prime(4)
    assert not validator._is_prime(6)
    assert not validator._is_prime(9)
    
    # Test _roman_to_int
    assert validator._roman_to_int("I") == 1
    assert validator._roman_to_int("V") == 5
    assert validator._roman_to_int("X") == 10
    assert validator._roman_to_int("IV") == 4
    assert validator._roman_to_int("IX") == 9
    assert validator._roman_to_int("XL") == 40
    
    # Test _extract_roman_numerals
    assert validator._extract_roman_numerals("abc") == []
    assert validator._extract_roman_numerals("abcIdef") == ["I"]
    assert validator._extract_roman_numerals("XXXV") == ["XXXV"]  # Single complete numeral 