package main

import (
	"./life"
	"fmt"
	"github.com/akamensky/argparse"
	"github.com/gdamore/tcell"
	"github.com/gdamore/tcell/encoding"
	"math"
	"os"
	"time"
)

type Console struct {
	life     *life.GameOfLife
	width    int
	height   int
	cellSize int
	paused   bool
}

func (ui *Console) init(life *life.GameOfLife) {
	ui.life = life
	ui.width = ui.life.Cols
	ui.height = ui.life.Rows
	ui.paused = false
}

func (ui *Console) drawGrid(screen tcell.Screen) {
	for i, row := range ui.life.CurrentGeneration {
		for j, cell := range row {
			if cell {
				screen.SetContent(j, i, '*', nil, tcell.StyleDefault.
					Background(tcell.ColorBlack).
					Foreground(tcell.ColorWhite))
			}
		}
	}
}

func (ui *Console) drawBorder(screen tcell.Screen) {
	for y := 0; y <= ui.height; y++ {
		screen.SetContent(0, y, '+', nil, tcell.StyleDefault.
			Background(tcell.ColorBlack).
			Foreground(tcell.ColorWhite))
		screen.SetContent(ui.width+1, y, '+', nil, tcell.StyleDefault.
			Background(tcell.ColorBlack).
			Foreground(tcell.ColorWhite))
	}
	for x := 0; x <= ui.width; x++ {
		screen.SetContent(x, 0, '+', nil, tcell.StyleDefault.
			Background(tcell.ColorBlack).
			Foreground(tcell.ColorWhite))
		screen.SetContent(x, ui.height+1, '+', nil, tcell.StyleDefault.
			Background(tcell.ColorBlack).
			Foreground(tcell.ColorWhite))
	}
}

func (ui *Console) getCell(x, y int) (int, int) {
	return x / ui.cellSize, y / ui.cellSize
}

func (ui *Console) run() {
	// Init screen
	encoding.Register()
	screen, err := tcell.NewScreen()
	if err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}
	if err := screen.Init(); err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}
	screen.EnableMouse()
	screen.SetStyle(tcell.StyleDefault.
		Foreground(tcell.ColorWhite).
		Background(tcell.ColorBlack))
	defer screen.Fini()

	quit := make(chan struct{})
	go func() {
		for {
			ev := screen.PollEvent()
			switch ev := ev.(type) {
			case *tcell.EventKey:
				switch ev.Key() {
				case tcell.KeyEscape, tcell.KeyEnter, tcell.KeyCtrlC:
					close(quit)
					return
				case tcell.KeyCtrlL:
					screen.Sync()
				}
			case *tcell.EventResize:
				screen.Sync()
			}
		}
	}()

loop:
	for {
		select {
		case <-quit:
			break loop
		default:
			time.Sleep(time.Second / 30)

			screen.Clear()
			ui.drawGrid(screen)
			ui.drawBorder(screen)
			screen.Show()

			ui.life.Step()
		}
	}
}

func main() {
	parser := argparse.NewParser("Game of Life", "Game of Life, developed by Georgy Komarov, K3141")
	cols := parser.Int("c", "columns", &argparse.Options{Default: 50})
	rows := parser.Int("r", "rows", &argparse.Options{Default: 20})
	maxGen := parser.Float("m", "max-generations", &argparse.Options{Default: math.Inf(0)})
	_ = parser.Parse(os.Args)

	game := &life.GameOfLife{}
	game.Init(*rows, *cols, *maxGen)

	gui := &Console{}
	gui.init(game)
	gui.run()
}
