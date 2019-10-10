def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''

    for character in plaintext:
        if character.islower():
            ciphertext += chr(97 + (ord(character) - 97 + (shift % 26)) % 26)
        elif character.isupper():
            ciphertext += chr(65 + (ord(character) - 65 + (shift % 26)) % 26)
        else:
            ciphertext += character

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''

    for character in ciphertext:
        if character.islower():
            plaintext += chr(97 + (ord(character) - 97 - (shift % 26)) % 26)
        elif character.isupper():
            plaintext += chr(65 + (ord(character) - 65 - (shift % 26)) % 26)
        else:
            plaintext += character

    return plaintext
