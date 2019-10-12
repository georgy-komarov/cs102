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
            chr_code = ord('a')
            ciphertext += chr(chr_code + (ord(character) - chr_code + (shift % 26)) % 26)
        elif character.isupper():
            chr_code = ord('A')
            ciphertext += chr(chr_code + (ord(character) - chr_code + (shift % 26)) % 26)
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
            chr_code = ord('a')
            plaintext += chr(chr_code + (ord(character) - chr_code - (shift % 26)) % 26)
        elif character.isupper():
            chr_code = ord('A')
            plaintext += chr(chr_code + (ord(character) - chr_code - (shift % 26)) % 26)
        else:
            plaintext += character

    return plaintext
