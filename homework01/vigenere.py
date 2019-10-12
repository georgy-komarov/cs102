def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    keyword_length = len(keyword)

    for index, character in enumerate(plaintext):
        if character.islower():
            chr_code = ord('a')
            shift = ord(keyword[index % keyword_length].lower()) - chr_code
            ciphertext += chr(chr_code + (ord(character) - chr_code + shift) % 26)
        elif character.isupper():
            chr_code = ord('A')
            shift = ord(keyword[index % keyword_length].upper()) - chr_code
            ciphertext += chr(chr_code + (ord(character) - chr_code + shift) % 26)
        else:
            ciphertext += character

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    keyword_length = len(keyword)

    for index, character in enumerate(ciphertext):
        if character.islower():
            chr_code = ord('a')
            shift = ord(keyword[index % keyword_length].lower()) - chr_code
            plaintext += chr(chr_code + (ord(character) - chr_code - shift) % 26)
        elif character.isupper():
            chr_code = ord('A')
            shift = ord(keyword[index % keyword_length].upper()) - chr_code
            plaintext += chr(chr_code + (ord(character) - chr_code - shift) % 26)
        else:
            plaintext += character
    return plaintext
