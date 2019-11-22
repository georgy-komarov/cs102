package life

import (
	"bytes"
	"io/ioutil"
	math2 "math"
	"math/rand"
	"time"
)

type GameOfLife struct {
	rows               int
	cols               int
	maxGenerations     float64
	nGeneration        int
	previousGeneration [][]bool
	currentGeneration  [][]bool
}

func (game *GameOfLife) init(rows, cols int, maxGenerations float64) {
	game.rows = rows
	game.cols = cols
	game.maxGenerations = maxGenerations
	game.currentGeneration = game.createGrid(true)
}

func (game *GameOfLife) createGrid(randomize bool) [][]bool {
	grid := make([][]bool, game.rows, game.cols)
	for i := range grid {
		grid[i] = make([]bool, game.cols, game.cols)
	}

	if randomize {
		for i, row := range grid {
			for j := range row {
				grid[i][j] = rand.Intn(2) != 0
			}
		}
	}
	return grid
}

func (game *GameOfLife) getNeighboursCount(x, y int) int {
	count := 0
	for j := -1; j <= 1; j++ {
		for i := -1; i <= 1; i++ {
			if i == 0 && j == 0 { // Не рассматриваем текущую клетку
				continue
			}
			x1, y1 := x+i, y+j
			if x1 < 0 || y1 < 0 || game.cols <= x1 || game.rows <= y1 { // Проверяем границы
				continue
			}
			if game.currentGeneration[y1][x1] {
				count++
			}
		}
	}
	return count
}

func (game *GameOfLife) getNextGeneration() [][]bool {
	nextGrid := game.createGrid(false)
	for y := 0; y < game.rows; y++ {
		for x := 0; x < game.cols; x++ {
			neighbourNum := game.getNeighboursCount(x, y)
			if !game.currentGeneration[y][x] && neighbourNum == 3 {
				nextGrid[y][x] = true
			} else if game.currentGeneration[y][x] && (neighbourNum == 2 || neighbourNum == 3) {
				nextGrid[y][x] = true
			}
		}
	}
	return nextGrid
}

func (game *GameOfLife) isMaxGenerationsExceed() bool {
	return float64(game.nGeneration) >= game.maxGenerations
}

func (game *GameOfLife) isChanging() bool {
	for y := 0; y < game.rows; y++ {
		for x := 0; x < game.cols; x++ {
			if game.currentGeneration[y][x] != game.previousGeneration[y][x] {
				return false
			}
		}
	}
	return true
}

func (game *GameOfLife) step() {
	if !game.isMaxGenerationsExceed() && game.isChanging() {
		game.previousGeneration = game.currentGeneration
		game.currentGeneration = game.getNextGeneration()
		game.nGeneration += 1
	}
}

func fromFile(filename string) *GameOfLife {
	file, _ := ioutil.ReadFile(filename)
	lines := bytes.Split(bytes.Trim(bytes.ReplaceAll(file, []byte("\r\n"), []byte("\n")), "\n"), []byte("\n"))
	grid := make([][]bool, len(lines))
	for i, line := range lines {
		grid[i] = make([]bool, len(lines[i]), len(lines[i]))
		for j, cell := range line {
			grid[i][j] = cell != byte('0')
		}
	}
	game := &GameOfLife{}
	game.init(len(grid), len(grid[0]), math2.Inf(1))
	game.currentGeneration = grid
	return game
}

func init() {
	rand.Seed(time.Now().UnixNano())
}
