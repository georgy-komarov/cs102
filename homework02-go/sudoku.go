package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"math"
	"math/rand"
	"path/filepath"
	"sort"
	"time"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {
	var result [][]byte

	for i := 0; i < len(values); i += n {
		result = append(result, values[i:i+n])
	}

	return result
}

func getRow(grid [][]byte, row int) []byte {
	return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
	var result []byte

	for _, row := range grid {
		result = append(result, row[col])
	}

	return result
}

func getBlock(grid [][]byte, row int, col int) []byte {
	var result []byte

	row3 := row / 3 * 3
	col3 := col / 3 * 3

	for row := row3; row < row3+3; row++ {
		for col := col3; col < col3+3; col++ {
			result = append(result, grid[row][col])
		}
	}
	return result
}

func findEmptyPosition(grid [][]byte) (int, int) {
	for y, row := range grid {
		for x, el := range row {
			if el == '.' {
				return y, x
			}
		}
	}
	return -1, -1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func remove(values []byte, item byte) []byte {
	pos := bytes.IndexByte(values, item)
	return append(values[:pos], values[pos+1:]...)
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	digits := make([]byte, 0, 9)

	for i := '1'; i <= '9'; i++ {
		digits = append(digits, byte(i))
	}

	for _, digit := range getRow(grid, row) {
		if digit != '.' && contains(digits, digit) {
			digits = remove(digits, digit)
		}
	}

	for _, digit := range getCol(grid, col) {
		if digit != '.' && contains(digits, digit) {
			digits = remove(digits, digit)
		}
	}

	for _, digit := range getBlock(grid, row, col) {
		if digit != '.' && contains(digits, digit) {
			digits = remove(digits, digit)
		}
	}

	sort.Slice(digits, func(i, j int) bool {
		return digits[i] < digits[j]
	})

	return digits
}

func solve(grid [][]byte) ([][]byte, bool) {
	row, col := findEmptyPosition(grid)
	if row == -1 && col == -1 { // Всё решено?
		return grid, true
	}

	values := findPossibleValues(grid, row, col)
	for _, value := range values {
		grid[row][col] = value
		newResult, result := solve(grid)
		if result { // Есть прогресс?
			return newResult, true
		}
		grid[row][col] = byte('.')
	}
	return grid, false
}

func checkCorrect(array []byte) bool {
	digits := make([]byte, 0, 9)
	for i := '1'; i <= '9'; i++ {
		digits = append(digits, byte(i))
	}

	arrayS := make([]byte, 9, 9)
	copy(arrayS, array)
	sort.Slice(arrayS, func(i, j int) bool {
		return arrayS[i] < arrayS[j]
	})

	for i := 0; i < len(digits); i++ {
		if digits[i] != arrayS[i] {
			return false
		}
	}
	return true
}

func checkSolution(grid [][]byte) bool {
	for _, row := range grid {
		if !checkCorrect(row) {
			return false
		}
	}

	for i := range grid {
		if !checkCorrect(getCol(grid, i)) {
			return false
		}
	}

	for _, i := range []int{0, 3, 6} {
		for _, j := range []int{0, 3, 6} {
			if !checkCorrect(getBlock(grid, i, j)) {
				return false
			}
		}
	}
	return true
}

func generateSudoku(N int) [][]byte {
	// Initialize random
	rand.Seed(time.Now().UTC().UnixNano())

	dotsToFill := int(81 - math.Min(float64(N), 81))

	emptyGrid := make([][]byte, 9, 9)
	for i := 0; i < 9; i++ {
		emptyGrid[i] = make([]byte, 9, 9)
		for j := 0; j < 9; j++ {
			emptyGrid[i][j] = byte('.')
		}
	}

	// To generate random Sudoku every time
	dotsToRemove := int(math.Min(float64(dotsToFill), float64(rand.Intn(10)+5)))
	for dotsToRemove > 0 {
		randomX, randomY := rand.Intn(9), rand.Intn(9)

		if emptyGrid[randomY][randomX] == '.' {
			values := findPossibleValues(emptyGrid, randomY, randomX)
			emptyGrid[randomY][randomX] = values[rand.Intn(len(values))]

			dotsToRemove -= 1
		}
	}

	newGrid, _ := solve(emptyGrid)

	for dotsToFill > 0 {
		randomX, randomY := rand.Intn(9), rand.Intn(9)
		if newGrid[randomY][randomX] == '.' {
			continue
		}
		newGrid[randomY][randomX] = '.'
		dotsToFill -= 1
	}
	return newGrid
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
