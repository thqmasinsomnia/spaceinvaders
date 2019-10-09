import pygame.font
import operator
from pygame.sprite import Group


class Highscore:
    def __init__(self, screen):
        self.screen = screen
        self.text_color = (255, 255, 255)
        self.black = (0, 0, 0)
        self.highscores = {}
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.x = 200
        self.y = 100

        with open("scores.txt") as file:
            for line in file:
                (key, val, val2) = line.split()
                self.highscores[int(key)] = int(val), val2

    def show_scores(self):
        test = pygame.image.load("images/spacebg.png")
        self.screen.blit(test, [0, 0])
        self.screen.blit(self.font.render('HIGH SCORES:', True, self.text_color), [self.x - 10, self.y - 50])
        self.screen.blit(self.font.render(str(self.highscores[0]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y])
        self.screen.blit(self.font.render(str(self.highscores[1]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 50])
        self.screen.blit(self.font.render(str(self.highscores[2]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 100])
        self.screen.blit(self.font.render(str(self.highscores[3]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 150])
        self.screen.blit(self.font.render(str(self.highscores[4]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 200])
        self.screen.blit(self.font.render(str(self.highscores[5]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 250])
        self.screen.blit(self.font.render(str(self.highscores[6]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 300])
        self.screen.blit(self.font.render(str(self.highscores[7]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 350])
        self.screen.blit(self.font.render(str(self.highscores[8]).strip('()').replace(',', ' -').replace("'", ''), True,
                                          self.text_color), [self.x, self.y + 400])
        self.screen.blit(self.font.render(str(self.highscores[9]).strip('()').replace(',', ' -').replace("'", ''), True,
                             self.text_color), [self.x, self.y + 450])
        self.screen.blit(self.font.render('PRESS "SPACE" TO PLAY', True, self.text_color), [self.x - 70, self.y + 500])

    def get_lowest_score(self):
        return int(self.highscores[9].__getitem__(0))

    def get_intials(self):
        test = pygame.image.load("images/spacebg.png")
        self.screen.blit(test, [0, 0])
        self.screen.blit(self.font.render('TYPE IN INITIALS', True, self.text_color), [self.x, self.y])
        pygame.display.flip()


        cnt = 0
        intials = ''
        done = False
        while cnt < 3:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        intials += 'A'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_b:
                        intials += 'B'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_c:
                        intials += 'C'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_d:
                        intials += 'D'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_e:
                        intials += 'E'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_f:
                        intials += 'F'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_g:
                        intials += 'G'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_h:
                        intials += 'H'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_i:
                        intials += 'I'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_j:
                        intials += 'J'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_k:
                        intials += 'K'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_l:
                        intials += 'L'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_m:
                        intials += 'M'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_n:
                        intials += 'N'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_o:
                        intials += 'O'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_p:
                        intials += 'P'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_q:
                        intials += 'Q'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_r:
                        intials += 'R'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_s:
                        intials += 'S'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_t:
                        intials += 'T'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_u:
                        intials += 'U'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_v:
                        intials += 'V'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_w:
                        intials += 'W'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_x:
                        intials += 'X'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_y:
                        intials += 'Y'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_z:
                        intials += 'Z'
                        self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                        pygame.display.flip()
                        cnt += 1
                    elif event.key == pygame.K_BACKSPACE:
                        if cnt > 0:
                            intials = intials[:-1]
                            self.screen.blit(test, [0, 0])
                            self.screen.blit(self.font.render('TYPE IN INITIALS', True, self.text_color),
                                             [self.x, self.y])
                            self.screen.blit(self.font.render(intials, True, self.text_color), [self.x, self.y + 50])
                            pygame.display.flip()
                            cnt -= 1


        return intials


    def add_score(self, name, score):


        self.highscores[10] = score, name
        d = sorted(self.highscores.values(), reverse=True)
        self.highscores = d
        print(self.highscores)

        f = open("scores.txt", "w+")

        for i in range(9):
            f.write(str(i) + " " + str(self.highscores[i]).strip('()').replace(',', '').replace("'", '') + '\n')

        f.write("9 " + str(self.highscores[9]).strip('()').replace(',', '').replace("'", ''))





