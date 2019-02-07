
from src.scene.gamescene import *
from src.scene.mapeditor import *
from src.tool.init import *
from src.tool.character import *

class GameMenu():
    def __init__(self, screen):
        self.screen = screen
        # 记录用户的选择
        # 1 为开始游戏
        # 2 为退出游戏
        self.selected = 2


    def show(self):
        pygame.mixer.music.load(music['main_theme'])
        pygame.mixer.music.play()

        while True:
            self.draw_background()

            self.check_event()

            pygame.display.update()


    def check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_DOWN:
                    if self.selected == 1:
                        # self.screen.fill((100, 150, 250), (300, 250, 40, 40))
                        # self.screen.blit(mushroom_img[0], (300, 300))
                        self.selected = 2
                elif event.key == K_UP:
                    if self.selected == 2:
                        # self.screen.fill((100, 150, 250), (300, 300, 40, 40))
                        # self.screen.blit(mushroom_img[0], (300, 250))
                        self.selected = 1
                elif event.key == K_RETURN:
                    if self.selected == 1:
                        gamescene = GameScene(self.screen)
                        gamescene.show()
                    elif self.selected == 2:
                        mapeditor = MapEditor()
                        mapeditor.show()
                        self.screen = pygame.display.set_mode((800, 600))


    def draw_background(self):
        self.screen.fill(SKYBLUE, (0, 0, 800, 600))
        for i in range(0, 800, 40):
            self.screen.blit(brick_img[0], (i, 520))
        for i in range(0, 800, 40):
            self.screen.blit(brick_img[0], (i, 560))
        self.screen.blit(cloud_img[0], (600, 100))
        self.screen.blit(brushwood_img[0], (0, 480))
        self.screen.blit(brushwood_img[0], (40, 480))
        self.screen.blit(brushwood_img[0], (200, 480))
        self.screen.blit(brushwood_img[0], (600, 480))


        # write_word(screen, '开始游戏', 36, WHITE, (350, 250))
        write_chars(screen, '开始游戏', 42, WHITE, (350, 250))
        write_chars(screen, '退出游戏', 42, WHITE, (350, 300))
        # self.screen.blit(mushroom_img[0], (300, 250))
        if self.selected == 1:
            self.screen.blit(mushroom_img[0], (300, 250))
        elif self.selected == 2:
            self.screen.blit(mushroom_img[0], (300, 300))


