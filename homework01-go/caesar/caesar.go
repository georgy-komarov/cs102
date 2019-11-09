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
			chrCode := int('a')
			ciphertext += string(rune(chrCode + (int(character)-chrCode+(shift%26))%26))
		} else if unicode.IsUpper(character) {
			chrCode := int('A')
			ciphertext += string(rune(chrCode + (int(character)-chrCode+(shift%26))%26))
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
			chrCode := int('a')
			newLetter := (int(character) - chrCode - (shift % 26)) % 26
			if newLetter < 0 {
				newLetter += 26
			}
			plaintext += string(rune(chrCode + newLetter))
		} else if unicode.IsUpper(character) {
			chrCode := int('A')
			newLetter := (int(character) - chrCode - (shift % 26)) % 26
			if newLetter < 0 {
				newLetter += 26
			}
			plaintext += string(rune(chrCode + newLetter))
		} else {
			plaintext += string(character)
		}
	}

	return plaintext
}
