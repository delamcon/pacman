import pygame

WINDOW_SIZE = WIDTH, HEIGHT = 475, 550  # размер поля (19, 22), размер клетки 25
TICK = pygame.USEREVENT + 1  # событие, нужно для отсчета одного момента


class Board:
    def __init__(self, screen):
        self.width = 19  # ширина поля
        self.height = 22  # высота поля
        self.screen = screen  # поверхность, на которой все выводим

        self.y = 12  # координаты пакмана во вложенном списке
        self.x = 9  # нужен для метода create_pacman в классе Pacman
        self.PacmanCurrentPos = (225, 300)  # сохраняет позицию пакмана, (225, 300) - позиция в начале игры в пикселях

        self.left = 0  # отступ с левого верхнего края по оси x (пока нет счета очков, будет 0)
        self.top = 0  # отступ с левого верхнего края по оси y (пока нет счета очков, будет 0)
        self.cell_size = 25  # размер клетки в пикселях

        self.nodes_pos = set()


        self.board = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 3, 0, 0, 3, 0, 0, 0, 3, 1, 3, 0, 0, 0, 3, 0, 0, 3, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 3, 0, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 0, 3, 1],
                      [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                      [1, 3, 0, 0, 3, 1, 3, 0, 3, 1, 3, 0, 3, 1, 3, 0, 0, 3, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 3, 3, 1, 0, 1, 3, 0, 3, 0, 3, 0, 3, 1, 0, 1, 3, 3, 1],
                      [1, 1, 0, 1, 0, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 1, 0, 1, 1],
                      [1, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 1],
                      [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                      [1, 0, 1, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 1, 0, 1],
                      [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                      [1, 3, 0, 0, 3, 0, 0, 0, 3, 1, 3, 0, 0, 0, 3, 3, 0, 3, 1],
                      [1, 0, 1, 1, 0, 1, 1, 1, 3, 1, 3, 1, 1, 1, 0, 1, 1, 0, 1],
                      [1, 3, 3, 1, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 1, 3, 3, 1],
                      [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                      [1, 3, 3, 0, 3, 1, 3, 0, 3, 1, 3, 0, 3, 1, 3, 0, 3, 3, 1],
                      [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                      [1, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        # 0 - клетка, по которой можно ходить,
        # 1 - стена
        # 2 - стенка выхода привидений

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x * self.cell_size + self.left,
                                                              y * self.cell_size + self.top,
                                                              self.cell_size, self.cell_size), width=0)
                if self.board[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 128), (x * self.cell_size + self.left,
                                                                    y * self.cell_size + self.top,
                                                                    self.cell_size, self.cell_size), width=0)
                if self.board[y][x] == 2:
                    pygame.draw.rect(self.screen, (252, 15, 192), (x * self.cell_size + self.left,
                                                                   y * self.cell_size + self.top,
                                                                   self.cell_size, self.cell_size), width=0)
                if self.board[y][x] == 3:
                    pygame.draw.rect(self.screen, (26, 185, 192), (x * self.cell_size + self.left,
                                                                   y * self.cell_size + self.top,
                                                                   self.cell_size, self.cell_size), width=0)


class Pacman(Board):
    def create_pacman(self):  # создаем пакмана на поле, метод вызывается один раз
        pygame.draw.rect(self.screen, (255, 255, 0), (self.x * self.cell_size + self.left,
                                                      self.y * self.cell_size + self.top,
                                                      self.cell_size, self.cell_size), width=0)

    def pacman_movement(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 3:
                    self.nodes_pos.add(f'({[x]}, {[y]})')

        print(self.nodes_pos)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.time.set_timer(TICK, 20)
    running = True

    pacman = Pacman(screen)  # передаем только поверхность, потому что размеры известны
    pacman.render()
    pacman.create_pacman()
    pacman.pacman_movement()
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # проверка по кнопкам ASDW
                if event.key == 97:  # проверяем A
                    pass
                if event.key == 115:  # проверяем S
                    pass
                if event.key == 100:  # проверяем D
                    pass
                if event.key == 119:  # проверяем W
                    pass
            if event.type == TICK:
                pass

        pygame.display.flip()
    pygame.quit()
