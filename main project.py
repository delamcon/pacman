import pygame

WINDOW_SIZE = WIDTH, HEIGHT = 475, 550  # размер поля (19, 22), размер клетки 25


class Board:
    def __init__(self, screen):
        self.width = 19  # ширина поля
        self.height = 21  # высота поля
        self.screen = screen  # поверхность, на которой все выводим

        self.left = 0  # отступ с левого верхнего края по оси x (пока нет счета очков, будет 0)
        self.top = 0  # отступ с левого верхнего края по оси y (пока нет счета очков, будет 0)
        self.cell_size = 25  # размер клетки в пикселях

        self.board = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                      [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                      [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                      [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                      [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                      [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                      [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                      [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                      [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        # 0 - клетка, по которой можно ходить,
        # 1 - стена

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 0:
                    pygame.draw.rect(self.screen, (125, 125, 125), (x * self.cell_size + self.left,
                                                                    y * self.cell_size + self.top,
                                                                    self.cell_size, self.cell_size), width=1)
                if self.board[y][x] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.cell_size + self.left,
                                                                    y * self.cell_size + self.top,
                                                                    self.cell_size, self.cell_size), width=0)


class Pacman(Board):
    pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    running = True

    pacman = Pacman(screen)  # передаем только поверхность, потому что размеры известны
    pacman.render()
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
