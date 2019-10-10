package caesar

import (
	"unicode"
)

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string

	// Default value
	if shift == 0 {
		shift = 3
	}

	for _, character := range plaintext {
		if unicode.IsLower(character) {
			ciphertext += string(rune(97 + (int(character)-97+(shift%26))%26))
		} else if unicode.IsUpper(character) {
			ciphertext += string(rune(65 + (int(character)-65+(shift%26))%26))
		} else {
			ciphertext += string(character)
		}
	}

	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string

	// Default value
	if shift == 0 {
		shift = 3
	}

	for _, character := range ciphertext {
		if unicode.IsLower(character) {
			newLetter := (int(character) - 97 - (shift % 26)) % 26
			if newLetter < 0 {
				newLetter += 26
			}
			plaintext += string(rune(97 + newLetter))
		} else if unicode.IsUpper(character) {
			newLetter := (int(character) - 65 - (shift % 26)) % 26
			if newLetter < 0 {
				newLetter += 26
			}
			plaintext += string(rune(65 + newLetter))
		} else {
			plaintext += string(character)
		}
	}

	return plaintext
}
