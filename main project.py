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
        # 3 - узел, расходжение путей

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

    def nodes(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 3:
                    self.nodes_pos.add((x, y))

    def pacman_movement(self, key, y, x):  # key - проверяемый ход WASD в виде кода кнопок, (y, x) - координата клетки
        cy = (y - self.top) // self.cell_size
        cx = (x - self.left) // self.cell_size
        print(cx, cy, x, y)
        keys = {0: 100, 1: 115, 2: 97, 3: 119}  #
        count = 0  # счетчик для оборота по круговой окружности против часовой стрелки по 90градусов, сначала 0градусов
        self.retset = set()  # множество для записи допустимых кнопок
        for i in range(1, -2, -1):
            if i != 0:
                coordcheck = self.board[cy][cx + i] == 0 or self.board[cy][cx + i] == 3
                if not ((y == cy * self.cell_size + self.top and x == cx * self.cell_size + self.left) and coordcheck):  # проверяем есть ли ход справа, при i = 1 и
                    # слева, при i = -1
                    self.retset.add(keys[count])  # добавляем код кнопки, если ход есть
                count += 1  # прибавляем 90градусов
                coordcheck = (self.board[cy + i][cx] == 0 and self.board[cy + i][cx] == 3)
                if not ((y == cy * self.cell_size + self.top and x == cx * self.cell_size + self.left) and  coordcheck):  # проверяем есть ли ход снизу, при i = 1 и
                    # сверху, при i = -1
                    self.retset.add(keys[count])  # добавляем код кнопки, если ход есть
                count += 1  # прибавляем 90градусов
        if key in self.retset:  # проверяем допустим ли наш ход WASD
            pacman.pacman_move(key)  # вызываем метод самого движения

    def pacman_move(self, key):
        if key == 97:
            x = (self.PacmanCurrentPos[0] - 1 - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] - self.left) // self.cell_size
            print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                              self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0] - 1, self.PacmanCurrentPos[1])
                pygame.draw.rect(self.screen, (255, 255, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                              self.cell_size, self.cell_size), width=0)
                pygame.display.flip()
        elif key == 115:
            x = (self.PacmanCurrentPos[0] - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] + 1 - self.left) // self.cell_size
            print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1] + 1)
                pygame.draw.rect(self.screen, (255, 255, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                              self.cell_size, self.cell_size), width=0)
                pygame.display.flip()
        elif key == 100:
            x = (self.PacmanCurrentPos[0] + 1 - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] - self.left) // self.cell_size
            print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0] + 1, self.PacmanCurrentPos[1])
                pygame.draw.rect(self.screen, (255, 255, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                              self.cell_size, self.cell_size), width=0)
                pygame.display.flip()
        elif key == 119:
            x = (self.PacmanCurrentPos[0] - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] - 1 - self.left) // self.cell_size
            print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1] - 1)
                pygame.draw.rect(self.screen, (255, 255, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                              self.cell_size, self.cell_size), width=0)
                pygame.display.flip()

    def pacman_pos(self):
        return self.PacmanCurrentPos


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.time.set_timer(TICK, 20)
    running = True

    pacman = Pacman(screen)  # передаем только поверхность, потому что размеры известны
    pacman.render()
    pacman.create_pacman()
    pacman.nodes()
    pygame.display.flip()
    PacmanCurrentKey = ''

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # проверка по кнопкам WASD
                pacman_cur_pos = pacman.pacman_pos()  # получаем координаты в реальном времени
                if event.key == 97:  # проверяем A
                    PacmanCurrentKey = 97
                    pacman.pacman_movement(97, pacman_cur_pos[1], pacman_cur_pos[0])
                if event.key == 115:  # проверяем S
                    PacmanCurrentKey = 115
                    pacman.pacman_movement(115, pacman_cur_pos[1], pacman_cur_pos[0])
                    # вызов метода проверки возможности хода
                if event.key == 100:  # проверяем D
                    PacmanCurrentKey = 100
                    pacman.pacman_movement(100, pacman_cur_pos[1], pacman_cur_pos[0])
                    # вызов метода проверки возможности хода
                if event.key == 119:  # проверяем W
                    PacmanCurrentKey = 119
                    pacman.pacman_movement(119, pacman_cur_pos[1], pacman_cur_pos[0])
                    # вызов метода проверки возможности хода
            if event.type == TICK:
                pacman_cur_pos = pacman.pacman_pos()
                pacman.pacman_movement(PacmanCurrentKey, pacman_cur_pos[1], pacman_cur_pos[0])
        pygame.display.flip()
    pygame.quit()

