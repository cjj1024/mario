import pygame

from tool.globaldata import *
from . gamemenu import *
from . gamescene import *
from . deathscene import *
from . selectlevelscene import *


class SceneControl():
    def __init__(self, scene):
        self.scene = scene
        self.is_active = True


    def show_scene(self):
        clock = pygame.time.Clock()
        while True:
            self.scene.show()
            self.check_event()

            if self.scene.next_scene != NOW_SCENE:
                next_scene = self.scene.next_scene
                self.scene.next_scene = NOW_SCENE

                if next_scene == GAME_MENU_SCENE:
                    self.scene = GameMenu()
                    print('game menu')
                elif next_scene == GAME_SCENE:
                    if self.scene.self_scene == SELECT_LEVEL_SCENE:
                        self.scene = GameScene(self.scene.level)
                    else:
                        self.scene = GameScene()
                elif next_scene == DEATH_SCENE:
                    self.scene = DeathScene(self.scene.mario)
                elif next_scene == SELECT_LEVEL_SCENE:
                    self.scene = SelectLevelScene()


            clock.tick(self.scene.fps)


    def check_event(self):
        if not self.is_active and pygame.display.get_active():
            self.is_active = True
            pygame.mixer.music.unpause()
        elif not pygame.display.get_active():
            self.is_active = False
            pygame.mixer.music.pause()

        for event in pygame.event.get():
            self.scene.process_event(event)
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)