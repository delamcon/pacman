import pygame
import random

random.seed(33) # 23 24

WINDOW_SIZE = WIDTH, HEIGHT = 575, 550  # размер поля (19, 22), размер клетки 25
TICK = pygame.USEREVENT + 1  # событие, нужно для отсчета одного момента
PACMAN_MOTION = pygame.USEREVENT + 1  # событие для отсчета смены кадра


class Pacman(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.retset = set()  # множество для записи допустимых кнопок
        self.width = 19  # ширина поля
        self.height = 22  # высота поля
        self.screen = screen  # поверхность, на которой все выводим

        self.y = 12  # координаты пакмана во вложенном списке
        self.x = 9  # нужен для метода create_pacman в классе Pacman
        self.PacmanCurrentPos = (225, 300)
        # сохраняет позицию пакмана, (225, 300) - позиция в начале игры в пикселях

        self.all_sprites = pygame.sprite.Group()
        self.main_pacman_sprite = pygame.sprite.Sprite()
        self.main_pacman_sprite.image = pygame.image.load('data/pacmanleft.png')
        self.main_pacman_sprite.rect = self.main_pacman_sprite.image.get_rect()
        pygame.display.flip()

        self.currentkey = 0
        self.count = 0

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
                      [1, 3, 3, 1, 0, 1, 3, 0, 3, 3, 3, 0, 3, 1, 0, 1, 3, 3, 1],
                      [1, 1, 0, 1, 0, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 1, 0, 1, 1],
                      [1, 3, 3, 3, 3, 3, 3, 1, 4, 4, 4, 1, 3, 3, 3, 3, 3, 3, 1],
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
                """if self.board[y][x] == 3:
                    pygame.draw.rect(self.screen, (26, 185, 192), (x * self.cell_size + self.left,
                                                                   y * self.cell_size + self.top,
                                                                   self.cell_size, self.cell_size), width=0)"""

    def nodes(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 3:
                    self.nodes_pos.add((x, y))

    def pacman_movement(self, key, cy, cx):  # key - проверяемый ход WASD в виде кода кнопок, (y, x) - координата клетки
        y = (cy - self.top) // self.cell_size
        x = (cx - self.left) // self.cell_size
        self.retset = set()

        horkeycheck = (key == 97 or key == 100)
        verkeycheck = (key == 119 or key == 115)
        ycellcheck = (cy - self.top) % self.cell_size == 0
        xcellcheck = (cx - self.top) % self.cell_size == 0

        if (horkeycheck and ycellcheck) or (verkeycheck and xcellcheck):
            if (self.board[y][(cx - self.left + 26) // self.cell_size] != 1 and
                     self.board[y][(cx - self.left + 26) // self.cell_size] != 2):  # проверяем есть ли ход справа
                self.retset.add(100)  # добавляем код кнопки D, если ход есть
            if (self.board[(cy - self.left + 26) // self.cell_size][x] != 1 and
                     self.board[(cy - self.left + 26) // self.cell_size][x] != 2):  # проверяем есть ли ход снизу
                self.retset.add(115)  # добавляем код кнопки S, если ход есть
            if (self.board[y][(cx - self.left - 1) // self.cell_size] != 1 and
                     self.board[y][(cx - self.left - 1) // self.cell_size] != 2):  # проверяем есть ли ход слева
                self.retset.add(97)  # добавляем код кнопки A, если ход есть
            if (self.board[(cy - self.left - 1) // self.cell_size][x] != 1 and
                     self.board[(cy - self.left - 1) // self.cell_size][x] != 2):  # проверяем есть ли ход сверху
                self.retset.add(119)  # добавляем код кнопки W, если ход есть

            if key in self.retset:  # проверяем допустим ли наш ход WASD
                self.currentkey = key
                pacman.pacman_move(key)  # вызываем метод самого движения
        else:
            pacman.pacman_move(self.currentkey)

    def motion_counting(self):
        self.count += 1
        if self.count == 3:
            self.count = 0

    def pacman_move(self, key):
        if key == 97:  # A
            x = (self.PacmanCurrentPos[0] - 1 - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] - self.left) // self.cell_size
            # print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1 and self.board[y][x] != 2:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0] - 1, self.PacmanCurrentPos[1])
                self.main_pacman_sprite.rect.x = self.PacmanCurrentPos[0]
                self.main_pacman_sprite.rect.y = self.PacmanCurrentPos[1]
                if self.count % 3 == 0:
                    # картинка меняется при опредленном числе счетчика
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmcirc.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 1:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmedleft.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 2:
                    self.main_pacman_sprite.image = pygame.image.load('data/pacmanleft.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
        elif key == 115:  # S
            x = (self.PacmanCurrentPos[0] - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] + 1 - self.left) // self.cell_size
            # print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1 and self.board[y][x] != 2:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1] + 1)
                self.main_pacman_sprite.rect.x = self.PacmanCurrentPos[0]
                self.main_pacman_sprite.rect.y = self.PacmanCurrentPos[1]
                if self.count % 3 == 0:
                    # картинка меняется при опредленном числе счетчика
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmcirc.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 1:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmeddown.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 2:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmdown.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                pygame.display.flip()
        elif key == 100:  # D
            x = (self.PacmanCurrentPos[0] + 1 - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] - self.left) // self.cell_size
            # print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1 and self.board[y][x] != 2:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0] + 1, self.PacmanCurrentPos[1])
                self.main_pacman_sprite.rect.x = self.PacmanCurrentPos[0]
                self.main_pacman_sprite.rect.y = self.PacmanCurrentPos[1]
                if self.count % 3 == 0:
                    # картинка меняется при опредленном числе счетчика
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmcirc.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 1:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmedright.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 2:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmright.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
        elif key == 119:  # W
            x = (self.PacmanCurrentPos[0] - self.left) // self.cell_size
            y = (self.PacmanCurrentPos[1] - 1 - self.left) // self.cell_size
            # print(x, y, self.board[y][x], self.PacmanCurrentPos)
            if self.board[y][x] != 1 and self.board[y][x] != 2:
                pygame.draw.rect(self.screen, (0, 0, 0), (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1],
                                                          self.cell_size, self.cell_size), width=0)
                self.PacmanCurrentPos = (self.PacmanCurrentPos[0], self.PacmanCurrentPos[1] - 1)
                self.main_pacman_sprite.rect.x = self.PacmanCurrentPos[0]
                self.main_pacman_sprite.rect.y = self.PacmanCurrentPos[1]
                if self.count % 3 == 0:
                    # картинка меняется при опредленном числе счетчика
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmcirc.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 1:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmedup.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()
                elif self.count % 3 == 2:
                    self.main_pacman_sprite.image = pygame.image.load('data/pcmup.png')
                    self.all_sprites.draw(screen)
                    pygame.display.flip()

    def pacman_pos(self):
        return self.PacmanCurrentPos


class Dots(Pacman, pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.dots = pygame.sprite.Group()

        self.score = 0

    def update_dots(self):
        self.dots.draw(self.screen)
        pygame.display.flip()

    def update(self, pos):
        self.main_pacman_sprite.rect.x = pos[0]
        self.main_pacman_sprite.rect.y = pos[1]

        if pygame.sprite.spritecollideany(self.main_pacman_sprite, self.dots):
            self.score += 1
            self.score_calc()
        pygame.sprite.spritecollide(self.main_pacman_sprite, self.dots, True)

    def score_calc(self):
        font = pygame.font.Font(None, 25)
        text = font.render(f"score {self.score * 10}", True, 'yellow')
        place = text.get_rect(
            center=(525, 20))
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(screen, (0, 0, 0), (place[0], place[1],
                                             text_w, text_h), 0)
        screen.blit(text, place)

    def render_dots(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 0 or self.board[y][x] == 3:
                    self.dot = pygame.sprite.Sprite()
                    self.dot.image = pygame.image.load('data/dot.png')
                    self.dot.rect = self.dot.image.get_rect()
                    self.dot.add(self.dots)

                    self.dot.rect.x = x * self.cell_size + self.left
                    self.dot.rect.y = y * self.cell_size + self.top
                    self.dots.draw(self.screen)
                    pygame.display.flip()


class Ghosts(Pacman, pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.CianCurrentPos = (200, 250)
        self.RedCurrentPos = (225, 200)
        self.YellCurrentPos = (225, 250)
        self.PinkCurrentPos = (250, 250)
        self.ghosts = pygame.sprite.Group()
        self.dots = Dots(self.screen)

        self.pink_cell = [(250, 225), (225, 225), (200, 225)]

        self.ghostpos = []
        self.ghostsmoves = {}

    def render_ghosts(self):
        self.g_cian = pygame.sprite.Sprite()
        self.g_cian.image = pygame.image.load('data/ghostcian.png')
        self.g_cian.rect = self.g_cian.image.get_rect()
        self.g_cian.rect.x = self.CianCurrentPos[0]
        self.g_cian.rect.y = self.CianCurrentPos[1]
        self.g_cian.add(self.ghosts)

        self.ghostsmoves[self.g_cian] = ''
        self.ghostpos.append(self.g_cian)

        self.g_red = pygame.sprite.Sprite()
        self.g_red.image = pygame.image.load('data/ghostred.png')
        self.g_red.rect = self.g_red.image.get_rect()
        self.g_red.rect.x = self.RedCurrentPos[0]
        self.g_red.rect.y = self.RedCurrentPos[1]
        self.g_red.add(self.ghosts)

        self.ghostsmoves[self.g_red] = ''
        self.ghostpos.append(self.g_red)

        self.g_yell = pygame.sprite.Sprite()
        self.g_yell.image = pygame.image.load('data/ghostyellow.png')
        self.g_yell.rect = self.g_yell.image.get_rect()
        self.g_yell.rect.x = self.YellCurrentPos[0]
        self.g_yell.rect.y = self.YellCurrentPos[1]
        self.g_yell.add(self.ghosts)

        self.ghostsmoves[self.g_yell] = ''
        self.ghostpos.append(self.g_yell)

        self.g_pink = pygame.sprite.Sprite()
        self.g_pink.image = pygame.image.load('data/ghostpink.png')
        self.g_pink.rect = self.g_pink.image.get_rect()
        self.g_pink.rect.x = self.PinkCurrentPos[0]
        self.g_pink.rect.y = self.PinkCurrentPos[1]
        self.g_pink.add(self.ghosts)

        self.ghostsmoves[self.g_pink] = ''
        self.ghostpos.append(self.g_pink)

        self.ghosts.draw(self.screen)
        pygame.display.flip()

    def ghost_move(self, g):
        pygame.draw.rect(self.screen, (0, 0, 0), (g.rect.x, g.rect.y,
                                                  self.cell_size, self.cell_size), width=0)
        if self.ghostsmoves[g] == 'w':
            g.rect.y = g.rect.y - 1
        if self.ghostsmoves[g] == 'a':
            g.rect.x = g.rect.x - 1
        if self.ghostsmoves[g] == 's':
            g.rect.y = g.rect.y + 1
        if self.ghostsmoves[g] == 'd':
            g.rect.x = g.rect.x + 1
        self.ghosts.draw(self.screen)
        pygame.display.flip()

    def ghost_calc(self):
        for g in self.ghostpos:
            x = g.rect.x  # координаты призрака
            y = g.rect.y  # в пикселях по х и у
            cx = (x - self.left) // self.cell_size  # координаты призрака
            cy = (y - self.top) // self.cell_size  # в клетках по х и у

            if (x - self.left) % self.cell_size == 0 and (y - self.top) % self.cell_size == 0:
                oklist = {2, 3, 4}  # клетки по которым призрак может идти
                notokey = {1}
                goodmoves = []  # ходы, которые допустимы на той или иной клетки
                wflag = True
                aflag = True
                sflag = True
                dflag = True
                if self.board[cy][cx] == 3 or self.board[cy][cx] == 4:
                    if self.board[cy + 1][cx] == 2:
                        oklist.remove(2)
                        notokey.add(2)
                    for i in range(1, 9):  #
                        if (cx + i) <= 18 and (cx - i) >= 0:  #
                            if self.board[cy][cx + i] in oklist and dflag:
                                goodmoves.append('d')
                                dflag = False
                            elif self.board[cy][cx + i] in notokey:  #
                                dflag = False
                            if self.board[cy][cx - i] in oklist and aflag:  #
                                goodmoves.append('a')
                                aflag = False
                            elif self.board[cy][cx - i] in notokey:  #
                                aflag = False

                        if (cy + i) <= 21 and (cy - i) >= 0:
                            if self.board[cy + i][cx] in oklist and sflag:  #
                                goodmoves.append('s')
                                sflag = False
                            elif self.board[cy + i][cx] in notokey:  #
                                sflag = False
                            if self.board[cy - i][cx] in oklist and wflag:  #
                                goodmoves.append('w')
                                wflag = False
                            elif self.board[cy - i][cx] in notokey:  #
                                wflag = False

                if len(goodmoves) >= 1:  #
                    move = random.randint(0, len(goodmoves) - 1)
                    self.ghostsmoves[g] = goodmoves[move]
                self.ghost_move(g)  #
            else:  #
                self.ghost_move(g)
            self.ghosts.draw(self.screen)  #
            pygame.display.update()
        for p in self.pink_cell:
            pygame.draw.rect(self.screen, (252, 15, 192), (p[0], p[1],
                                self.cell_size, self.cell_size), width=0)

    def collide_pacman(self, pos):
        self.main_pacman_sprite.rect.x = pos[0]
        self.main_pacman_sprite.rect.y = pos[1]
        if pygame.sprite.spritecollideany(self.main_pacman_sprite, self.ghosts):
            return True
        else:
            return False


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    running = True

    pacman = Pacman(screen)  # передаем только поверхность, потому что размеры известны
    pacman.render()
    pacman.nodes()

    PacmanCurrentKey = ''
    dot = Dots(screen)
    dot.score_calc()
    dot.render_dots()
    pygame.time.set_timer(TICK, 15)
    pygame.time.set_timer(PACMAN_MOTION, 35)
    ghosts = Ghosts(screen)
    ghosts.render_ghosts()
    ghosts.ghost_calc()
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # проверка по кнопкам ASDW
                pacman_cur_pos = pacman.pacman_pos()  # получаем координаты в реальном времени
                if event.key == 97:  # проверяем A
                    PacmanCurrentKey = 97
                    pacman.pacman_movement(97, pacman_cur_pos[1], pacman_cur_pos[0])
                    # вызов метода проверки возможности хода
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

                ghosts.ghost_calc()
                dot.update(pacman_cur_pos)
                dot.update_dots()
                pacman.pacman_movement(PacmanCurrentKey, pacman_cur_pos[1], pacman_cur_pos[0])
                if ghosts.collide_pacman(pacman_cur_pos):
                    pygame.time.set_timer(TICK, 0)
                    pygame.time.set_timer(PACMAN_MOTION, 0)

                    font = pygame.font.Font(None, 50)
                    text = font.render("Game Over", True, (232, 72, 167))
                    text_x = 112
                    text_y = 150
                    place = text.get_rect(
                        center=(237, 275))
                    text_w = text.get_width()
                    text_h = text.get_height()
                    pygame.draw.rect(screen, (0, 0, 0), (place[0], place[1],
                                                           text_w, text_h), 0)
                    screen.blit(text, place)
            if event.type == PACMAN_MOTION:
                pacman.motion_counting()
        pygame.display.flip()
    pygame.quit()
