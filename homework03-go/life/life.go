package life

import (
	"bytes"
	"io/ioutil"
	"math"
	"math/rand"
	"time"
)

type GameOfLife struct {
	Rows               int
	Cols               int
	maxGenerations     float64
	NGeneration        int
	previousGeneration [][]bool
	CurrentGeneration  [][]bool
}

func (game *GameOfLife) Init(rows, cols int, maxGenerations float64) {
	game.Rows = rows
	game.Cols = cols
	game.maxGenerations = maxGenerations
	game.previousGeneration = game.createGrid(false)
	game.CurrentGeneration = game.createGrid(true)
}

func (game *GameOfLife) createGrid(randomize bool) [][]bool {
	grid := make([][]bool, game.Rows, game.Rows)
	for i := range grid {
		grid[i] = make([]bool, game.Cols, game.Cols)
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
			if x1 < 0 || y1 < 0 || game.Cols <= x1 || game.Rows <= y1 { // Проверяем границы
				continue
			}
			if game.CurrentGeneration[y1][x1] {
				count++
			}
		}
	}
	return count
}

func (game *GameOfLife) getNextGeneration() [][]bool {
	nextGrid := game.createGrid(false)
	for y := 0; y < game.Rows; y++ {
		for x := 0; x < game.Cols; x++ {
			neighbourNum := game.getNeighboursCount(x, y)
			if !game.CurrentGeneration[y][x] && neighbourNum == 3 {
				nextGrid[y][x] = true
			} else if game.CurrentGeneration[y][x] && (neighbourNum == 2 || neighbourNum == 3) {
				nextGrid[y][x] = true
			}
		}
	}
	return nextGrid
}

func (game *GameOfLife) IsMaxGenerationsExceed() bool {
	if game.maxGenerations == math.Inf(0) {
		return false
	}
	return float64(game.NGeneration) >= game.maxGenerations
}

func (game *GameOfLife) IsChanging() bool {
	for y := 0; y < game.Rows; y++ {
		for x := 0; x < game.Cols; x++ {
			if game.CurrentGeneration[y][x] != game.previousGeneration[y][x] {
				return true
			}
		}
	}
	return false
}

func (game *GameOfLife) Step() {
	if !game.IsMaxGenerationsExceed() && game.IsChanging() {
		game.previousGeneration = game.CurrentGeneration
		game.CurrentGeneration = game.getNextGeneration()
		game.NGeneration += 1
	}
}

func (game *GameOfLife) FromFile(filename string) *GameOfLife {
	file, _ := ioutil.ReadFile(filename)
	lines := bytes.Split(bytes.Trim(bytes.ReplaceAll(file, []byte("\r\n"), []byte("\n")), "\n"), []byte("\n"))
	grid := make([][]bool, len(lines))
	for i, line := range lines {
		grid[i] = make([]bool, len(lines[i]), len(lines[i]))
		for j, cell := range line {
			grid[i][j] = cell != byte('0')
		}
	}
	game.Init(len(grid), len(grid[0]), math.Inf(1))
	game.CurrentGeneration = grid
	return game
}

func init() {
	rand.Seed(time.Now().UnixNano())
}
