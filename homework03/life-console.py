import argparse
import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row_ind, row in enumerate(self.life.curr_generation, start=1):
            for col_ind, cell in enumerate(row, start=1):
                if cell:
                    try:
                        screen.addstr(row_ind, col_ind, '*')
                    except curses.error:  # Если терминал меньше поля
                        pass

    def run(self) -> None:
        screen = curses.initscr()

        running = True
        while running:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)

            self.life.step()
            if self.life.is_max_generations_exceed:
                running = False

            screen.refresh()
            time.sleep(1 / 60)

        screen.getch()
        curses.endwin()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=80)
    parser.add_argument('--cols', type=int, default=30)
    parser.add_argument('--max-generations', default=float('inf'), type=int)
    args = parser.parse_args()

    game = GameOfLife((args.cols, args.rows), max_generations=args.max_generations)
    console = Console(game)
    console.run()
