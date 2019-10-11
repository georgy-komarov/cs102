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
            shift = ord(keyword[index % keyword_length].lower()) - 97
            ciphertext += chr(97 + (ord(character) - 97 + shift) % 26)
        elif character.isupper():
            shift = ord(keyword[index % keyword_length].upper()) - 65
            ciphertext += chr(65 + (ord(character) - 65 + shift) % 26)
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
            shift = ord(keyword[index % keyword_length].lower()) - 97
            plaintext += chr(97 + (ord(character) - 97 - shift) % 26)
        elif character.isupper():
            shift = ord(keyword[index % keyword_length].upper()) - 65
            plaintext += chr(65 + (ord(character) - 65 - shift) % 26)
        else:
            plaintext += character
    return plaintext
