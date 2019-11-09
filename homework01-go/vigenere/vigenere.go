package vigenere

import "unicode"
import "unicode/utf8"

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string
	keywordLength := utf8.RuneCountInString(keyword)

	for index, character := range plaintext {
		if unicode.IsLower(character) {
			chrCode := int('a')
			shift := int(unicode.ToLower(rune(keyword[index%keywordLength]))) - chrCode
			ciphertext += string(rune(chrCode + (int(character)-chrCode+shift)%26))
		} else if unicode.IsUpper(character) {
			chrCode := int('A')
			shift := int(unicode.ToUpper(rune(keyword[index%keywordLength]))) - chrCode
			ciphertext += string(rune(chrCode + (int(character)-chrCode+shift)%26))
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
			chrCode := int('a')
			shift := int(unicode.ToLower(rune(keyword[index%keywordLength]))) - chrCode
			newLetter := (int(character) - chrCode - shift) % 26
			if newLetter < 0 {
				newLetter += 26
			}
			plaintext += string(rune(chrCode + newLetter))
		} else if unicode.IsUpper(character) {
			chrCode := int('A')
			shift := int(unicode.ToUpper(rune(keyword[index%keywordLength]))) - chrCode
			newLetter := (int(character) - chrCode - shift) % 26
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
