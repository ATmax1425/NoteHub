import random
import string

def generate_verification_code():
    # Define the character sets
    special_characters = "!@#$%^&*()-_=+"
    uppercase_characters = string.ascii_uppercase
    lowercase_characters = string.ascii_lowercase
    digits = string.digits

    # Ensure at least one character from each set is included
    code = [
        random.choice(special_characters),
        random.choice(uppercase_characters),
        random.choice(lowercase_characters),
        random.choice(digits)
    ]

    # Fill the rest of the code with random characters from all sets
    all_characters = special_characters + uppercase_characters + lowercase_characters + digits
    while len(code) < 6:
        code.append(random.choice(all_characters))

    # Shuffle the list to ensure randomness
    random.shuffle(code)

    # Convert list to string and return
    return ''.join(code)

