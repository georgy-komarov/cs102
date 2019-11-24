package main

import (
	"./life"
	"github.com/akamensky/argparse"
	"github.com/hajimehoshi/ebiten"
	"github.com/hajimehoshi/ebiten/inpututil"
	"image/color"
	"log"
	"math"
	"os"
)

type GUI struct {
	life     *life.GameOfLife
	width    int
	height   int
	cellSize int
	paused   bool
}

func (gui *GUI) init(life *life.GameOfLife, cellSize int) {
	gui.life = life
	gui.width = gui.life.Cols * cellSize
	gui.height = gui.life.Rows * cellSize
	gui.cellSize = cellSize
	gui.paused = false
}

func (gui *GUI) drawLines(screen *ebiten.Image) {
	verticalLine, _ := ebiten.NewImage(1, gui.height, ebiten.FilterDefault)
	_ = verticalLine.Fill(color.Black)

	horizontalLine, _ := ebiten.NewImage(gui.width, 1, ebiten.FilterDefault)
	_ = horizontalLine.Fill(color.Black)

	for x := 0; x < gui.width; x += gui.cellSize {
		lineOpts := &ebiten.DrawImageOptions{}
		lineOpts.GeoM.Translate(float64(x), 0)
		_ = screen.DrawImage(verticalLine, lineOpts)
	}
	for y := 0; y < gui.height; y += gui.cellSize {
		lineOpts := &ebiten.DrawImageOptions{}
		lineOpts.GeoM.Translate(0, float64(y))
		_ = screen.DrawImage(horizontalLine, lineOpts)
	}
}

func (gui *GUI) drawGrid(screen *ebiten.Image) {
	cell, _ := ebiten.NewImage(gui.cellSize-1, gui.cellSize-1, ebiten.FilterDefault)
	_ = cell.Fill(color.RGBA{G: 255, A: 255})

	for y, row := range gui.life.CurrentGeneration {
		for x, cellValue := range row {
			if cellValue {
				lineOpts := &ebiten.DrawImageOptions{}
				lineOpts.GeoM.Translate(float64(x*gui.cellSize+1), float64(y*gui.cellSize+1))
				_ = screen.DrawImage(cell, lineOpts)
			}
		}
	}
}

func (gui *GUI) getCell(x, y int) (int, int) {
	return x / gui.cellSize, y / gui.cellSize
}

func (gui *GUI) run(screen *ebiten.Image) error {
	if inpututil.IsKeyJustPressed(ebiten.KeySpace) {
		gui.paused = !gui.paused
	}
	if inpututil.IsMouseButtonJustPressed(ebiten.MouseButtonLeft) && gui.paused {
		xPos, yPos := ebiten.CursorPosition()
		x, y := gui.getCell(xPos, yPos)
		gui.life.CurrentGeneration[y][x] = !gui.life.CurrentGeneration[y][x]
	}

	_ = screen.Fill(color.White)
	gui.drawLines(screen)
	gui.drawGrid(screen)

	if !gui.paused {
		gui.life.Step()
	}
	return nil
}

func main() {
	parser := argparse.NewParser("Game of Life", "Game of Life, developed by Georgy Komarov, K3141")
	cols := parser.Int("c", "columns", &argparse.Options{Default: 50})
	rows := parser.Int("r", "rows", &argparse.Options{Default: 30})
	cellSize := parser.Int("s", "cell-size", &argparse.Options{Default: 10})
	maxGen := parser.Float("m", "max-generations", &argparse.Options{Default: math.Inf(0)})
	_ = parser.Parse(os.Args)

	game := &life.GameOfLife{}
	game.Init(*rows, *cols, *maxGen)

	gui := &GUI{}
	gui.init(game, *cellSize)

	ebiten.SetRunnableInBackground(true)
	if err := ebiten.Run(gui.run, gui.width, gui.height, 1, "Game of Life - Komarov Georgy, K3141"); err != nil {
		log.Fatal(err)
	}
}
