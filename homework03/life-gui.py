import argparse

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.cell_size = cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(len(self.life.curr_generation)):
            for x in range(len(self.life.curr_generation[0])):
                if self.life.curr_generation[y][x]:
                    pygame.draw.rect(self.screen,
                                     pygame.Color('green'),
                                     (x * self.cell_size + 1,
                                      y * self.cell_size + 1,
                                      self.cell_size - 1,
                                      self.cell_size - 1)
                                     )

    def get_cell(self, x: int, y: int):
        return x // self.cell_size, y // self.cell_size

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        paused = False
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                if event.type == MOUSEBUTTONDOWN:
                    if paused:
                        x, y = self.get_cell(*pygame.mouse.get_pos())
                        self.life.curr_generation[y][x] = not self.life.curr_generation[y][x]

            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            if paused:
                pass
            elif not self.life.is_max_generations_exceed:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=640)
    parser.add_argument('--height', type=int, default=480)
    parser.add_argument('--cell-size', type=int, default=10)
    parser.add_argument('--max-generations', default=float('inf'), type=int)
    args = parser.parse_args()

    rows, cols = args.height // args.cell_size, args.width // args.cell_size
    game = GameOfLife((rows, cols), max_generations=args.max_generations)
    gui = GUI(game, args.cell_size)
    gui.run()
