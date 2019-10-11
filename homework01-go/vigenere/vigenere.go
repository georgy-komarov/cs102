package vigenere

import "unicode"
import "unicode/utf8"

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string
	keywordLength := utf8.RuneCountInString(keyword)

	for index, character := range plaintext {
		if unicode.IsLower(character) {
			shift := int(unicode.ToLower(rune(keyword[index%keywordLength]))) - 97
			ciphertext += string(rune(97 + (int(character)-97+shift)%26))
		} else if unicode.IsUpper(character) {
			shift := int(unicode.ToUpper(rune(keyword[index%keywordLength]))) - 65
			ciphertext += string(rune(65 + (int(character)-65+shift)%26))
		} else {
			ciphertext += string(character)
		}
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string
	keywordLength := utf8.RuneCountInString(keyword)

	for index, character := range ciphertext {
		if unicode.IsLower(character) {
			shift := int(unicode.ToLower(rune(keyword[index%keywordLength]))) - 97
			newLetter := (int(character) - 97 - shift) % 26
			if newLetter < 0 {
				newLetter += 26
			}
			plaintext += string(rune(97 + newLetter))
		} else if unicode.IsUpper(character) {
			shift := int(unicode.ToUpper(rune(keyword[index%keywordLength]))) - 65
			newLetter := (int(character) - 65 - shift) % 26
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
