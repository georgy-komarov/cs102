package main

import (
	"github.com/hajimehoshi/ebiten"
	"image/color"
	"log"
	"math/rand"
	"time"
)

type GameOfLife struct {
	width      int
	height     int
	cellSize   int
	colsNumber int
	rowsNumber int
	grid       [][]bool
}

func (game *GameOfLife) init(width, height, cellSize int) {
	game.width = width
	game.height = height
	game.cellSize = cellSize
	game.colsNumber = game.width / game.cellSize
	game.rowsNumber = game.height / game.cellSize
	game.grid = game.createGrid(true)
}

func (game *GameOfLife) createGrid(randomize bool) [][]bool {
	grid := make([][]bool, game.rowsNumber, game.rowsNumber)
	for i := range grid {
		grid[i] = make([]bool, game.colsNumber, game.colsNumber)
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

func (game *GameOfLife) drawLines(screen *ebiten.Image) {
	verticalLine, _ := ebiten.NewImage(1, game.height, ebiten.FilterDefault)
	_ = verticalLine.Fill(color.Black)

	horizontalLine, _ := ebiten.NewImage(game.width, 1, ebiten.FilterDefault)
	_ = horizontalLine.Fill(color.Black)

	for x := 0; x < game.width; x += game.cellSize {
		lineOpts := &ebiten.DrawImageOptions{}
		lineOpts.GeoM.Translate(float64(x), 0)
		_ = screen.DrawImage(verticalLine, lineOpts)
	}
	for y := 0; y < game.height; y += game.cellSize {
		lineOpts := &ebiten.DrawImageOptions{}
		lineOpts.GeoM.Translate(0, float64(y))
		_ = screen.DrawImage(horizontalLine, lineOpts)
	}
}

func (game *GameOfLife) drawGrid(screen *ebiten.Image) {
	cell, _ := ebiten.NewImage(game.cellSize-1, game.cellSize-1, ebiten.FilterDefault)
	_ = cell.Fill(color.RGBA{G: 255, A: 255})

	for y, row := range game.grid {
		for x, cellValue := range row {
			if cellValue {
				lineOpts := &ebiten.DrawImageOptions{}
				lineOpts.GeoM.Translate(float64(x*game.cellSize+1), float64(y*game.cellSize+1))
				_ = screen.DrawImage(cell, lineOpts)
			}
		}
	}
}

func (game *GameOfLife) run(screen *ebiten.Image) error {
	_ = screen.Fill(color.White)
	game.drawGrid(screen)
	game.drawLines(screen)
	game.grid = game.getNextGeneration()
	return nil
}

func (game *GameOfLife) getNeighboursCount(x, y int) int {
	count := 0
	for j := -1; j <= 1; j++ {
		for i := -1; i <= 1; i++ {
			if i == 0 && j == 0 { // Не рассматриваем текущую клетку
				continue
			}
			x1, y1 := x+i, y+j
			if x1 < 0 || y1 < 0 || game.colsNumber <= x1 || game.rowsNumber <= y1 { // Проверяем границы
				continue
			}
			if game.grid[y1][x1] {
				count++
			}
		}
	}
	return count
}

func (game *GameOfLife) getNextGeneration() [][]bool {
	nextGrid := game.createGrid(false)
	for y := 0; y < game.rowsNumber; y++ {
		for x := 0; x < game.colsNumber; x++ {
			neighbourNum := game.getNeighboursCount(x, y)
			if !game.grid[y][x] && neighbourNum == 3 {
				nextGrid[y][x] = true
			} else if game.grid[y][x] && (neighbourNum == 2 || neighbourNum == 3) {
				nextGrid[y][x] = true
			}
		}
	}
	return nextGrid
}

const (
	width  = 500
	height = 300
	size   = 10
)

func main() {
	rand.Seed(time.Now().UnixNano())

	game := &GameOfLife{}
	game.init(width, height, size)

	ebiten.SetRunnableInBackground(true)
	if err := ebiten.Run(game.run, width, height, 1, "Game of Life - Komarov Georgy, K3141"); err != nil {
		log.Fatal(err)
	}
}
