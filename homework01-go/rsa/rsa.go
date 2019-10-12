package rsa

import (
	"errors"
	"math"
	"math/big"
	"math/rand"
)

type Key struct {
	key int
	n   int
}

type KeyPair struct {
	Private Key
	Public  Key
}

func isPrime(n int) bool {
	if n == 2 || n == 3 {
		return true
	}
	if n < 2 || n%2 == 0 {
		return false
	}
	for i := 5; i < int(math.Sqrt(float64(n)))+1; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func gcd(a int, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func multiplicativeInverse(e int, phi int) int {
	x0, x1, y0, y1, q := 0, 1, 1, 0, 0
	a, b := e, phi
	for a != 0 {
		q, b, a = b/a, a, b%a
		y0, y1 = y1, y0-q*y1
		x0, x1 = x1, x0-q*x1
	}
	if b != 1 {
		errors.New("no inverse exists")
	}
	res := x0 % phi
	if res < 0 {
		res += phi
	}
	return res
}

func GenerateKeypair(p int, q int) (KeyPair, error) {
	if !isPrime(p) || !isPrime(q) {
		return KeyPair{}, errors.New("Both numbers must be prime.")
	} else if p == q {
		return KeyPair{}, errors.New("p and q can't be equal.")
	}

	n := p * q
	phi := (p - 1) * (q - 1)

	e := rand.Intn(phi-1) + 1
	g := gcd(e, phi)
	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	d := multiplicativeInverse(e, phi)
	return KeyPair{Key{e, n}, Key{d, n}}, nil
}

func Encrypt(pk Key, plaintext string) []int {
	cipher := []int{}
	n := new(big.Int)
	for _, ch := range plaintext {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		cipher = append(cipher, int(n.Int64()))
	}
	return cipher
}

func Decrypt(pk Key, cipher []int) string {
	plaintext := ""
	n := new(big.Int)
	for _, ch := range cipher {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		plaintext += string(rune(int(n.Int64())))
	}
	return plaintext
}
