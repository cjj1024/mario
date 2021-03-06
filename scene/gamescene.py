import sys
import random

from sprite.mario import *
from level.level import *
from tool.character import *
from . scene import *
from gui.gui import *
from gui.menuitem import *
from gui.menu import *
from gui.menubar import *
from gui.slider import *
from gui.widget import *
from gui.label import *


@Singleton
class GameScene(Scene):
    def __init__(self):
        print("init game scene")
        Scene.__init__(self)

        self.self_scene = GAME_SCENE

        self.sound_volume = 0

        self.player_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.mushroom_group = pygame.sprite.Group()

        self.mario = Mario()
        self.player_group.add(self.mario)

        self.init_gui()

        self.globalData = GlobalData()


    def set_level(self, level):
        self.level = Level(level)


    def init_gui(self):
        self.gui = GUI()

        menubar = MenuBar()

        setting_menu = Menu(text="设置")
        menubar.add_menu(setting_menu)
        sound_menuitem = MenuItem(text="声音")
        sound_menuitem.bind_active(self.set_volumn, sound_menuitem)
        setting_menu.add_menuitem(sound_menuitem)

        system_menu = Menu(text="系统")

        menubar.add_menu(system_menu)
        return_menu_menuitem = MenuItem(text='返回菜单')
        return_menu_menuitem.bind_active(self.enter_gamemenu_sceen)
        system_menu.add_menuitem(return_menu_menuitem)
        exit_menuitem = MenuItem(text="退出")
        exit_menuitem.bind_active(
            lambda: sys.exit(0))
        system_menu.add_menuitem(exit_menuitem)

        self.gui.add_menubar(menubar, pos=(0, 0))


    def set_volumn(self, button):
        button.status = HOVER

        widget = Widget()
        music_label = Label(text='声音', text_size=48)
        music_slider = Slider(value=pygame.mixer.music.get_volume())
        widget.add_label(music_label, pos=(0, 100))
        widget.add_slider(music_slider, pos=(music_label.rect.width, 100))
        sound_label = Label(text='音效', text_size=48)
        sound_slider = Slider(value=pygame.mixer.music.get_volume())
        widget.add_label(sound_label, pos=(0, 200))
        widget.add_slider(sound_slider, pos=(sound_label.rect.width, 200))
        self.gui.add_widget(widget, pos=(100, 200))

        clock = pygame.time.Clock()
        while widget.alive():
            for event in pygame.event.get():
                self.gui.process_event(event)
            self.update()
            self.gui.update(self.screen)
            pygame.display.update()
            pygame.mixer.music.set_volume(music_slider.value)
            self.sound_volume = sound_slider.value
            clock.tick(60)


    def enter_gamemenu_sceen(self):
        self.globalData.scene = GAME_MENU_SCENE


    def update(self):
        self.screen.fill(SKYBLUE, (0, 0, 800, 600))
        self.level.update(self.screen)
        self.coin_group.update()
        self.coin_group.draw(self.screen)
        self.mushroom_group.update()
        self.mushroom_group.draw(self.screen)
        self.player_group.update()
        self.player_group.draw(self.screen)


    def show(self):
        self.update()

        self.move_mario()
        self.move_item(self.level.enemy_group)
        self.move_item(self.mushroom_group)

        self.show_info()
        self.gui.update(self.screen)
        pygame.display.update()

        if not self.player_group.has(self.mario):
            self.globalData.scene = DEATH_SCENE
            self.player_group.add(self.mario)


    # 根据mario的x, y轴的速度移动mario
    # 在x轴, y轴移动后, 检测碰撞, 处理碰撞
    def move_mario(self):

        self.mario.rect.x += self.mario.speed_x
        self.check_move_scene()
        self.check_mario_border()
        self.check_mario_collision_x()

        if self.mario.speed_y != 0:
            self.mario.rect.y += self.mario.speed_y
            self.check_mario_border()
            self.check_mario_collision_y()


    # 检测是否移动场景
    # 当mairo走过屏幕的一半时, 移动场景
    def check_move_scene(self):
        if self.mario.rect.x > 400 and self.mario.speed_x > 0 \
           and self.level.start_x + self.mario.speed_x + 800 < self.level.length:
            self.level.start_x += self.mario.speed_x

            self.mario.rect.x -= self.mario.speed_x

            for enemy in self.level.enemy_group:
                enemy.rect.x -= self.mario.speed_x

            for coin in self.coin_group:
                coin.rect.x -= self.mario.speed_x

            for mushroom in self.mushroom_group:
                mushroom.rect.x -= self.mario.speed_x


    # 检测mario在x轴上的碰撞
    def check_mario_collision_x(self):
        if not self.mario.is_collider:
            return
        brick = pygame.sprite.spritecollideany(self.mario, self.level.brick_group)
        pipe = pygame.sprite.spritecollideany(self.mario, self.level.pipe_group)
        mushroom = pygame.sprite.spritecollideany(self.mario, self.mushroom_group)
        enemy = pygame.sprite.spritecollideany(self.mario, self.level.enemy_group)
        piranha = pygame.sprite.spritecollideany(self.mario, self.level.plant_enemy)
        checkpoint = pygame.sprite.spritecollideany(self.mario, self.level.checkpoint_group)
        win = pygame.sprite.spritecollideany(self.mario, self.level.castle_group)

        if brick:
            self.process_mario_collision_x(brick)

        if pipe:
            self.process_mario_collision_x(pipe)

        if win:
            self.process_win()

        if mushroom:
            self.process_mario_mushroom_collision(mushroom)

        if enemy:
            if self.mario.rect.x > enemy.rect.x and self.mario.rect.left + 10 < enemy.rect.right or \
                self.mario.rect.x < enemy.rect.x and self.mario.rect.right - 10 > enemy.rect.left:
                self.process_mario_enemy_collision_x()

        if checkpoint:
            self.process_mario_checkpoint_collision(checkpoint)

        if piranha:
            self.process_mario_piranha_collision()

    def process_win(self):
        self.globalData.scene = WIN_SCENE


    def process_mario_piranha_collision(self):
        self.mario.set_status(DEATH)


    def process_mario_checkpoint_collision(self, checkpoint):
        self.mario.save_data()
        checkpoint.kill()


    def process_mario_enemy_collision_x(self):
        self.mario.set_status(DEATH)


    def process_mario_mushroom_collision(self, mushroom):
        mushroom.bump(self.mario)


    # 处理Mario在x轴上的碰撞
    def process_mario_collision_x(self, collider):
        if self.mario.rect.x < collider.rect.x:
            self.mario.rect.right = collider.rect.left
        else:
            self.mario.rect.left = collider.rect.right

        # mario在x轴上遇到碰撞, 则x水平速度置为0
        self.mario.speed_x = 0


    # 检测mario在y轴上的碰撞
    def check_mario_collision_y(self):
        if not self.mario.is_collider:
            return
        brick = pygame.sprite.spritecollideany(self.mario, self.level.brick_group)
        pipe = pygame.sprite.spritecollideany(self.mario, self.level.pipe_group)
        mushroom = pygame.sprite.spritecollideany(self.mario, self.mushroom_group)

        checkpoint = pygame.sprite.spritecollideany(self.mario, self.level.checkpoint_group)

        if brick:
            self.process_mario_collision_y(brick)

        if pipe:
            self.process_mario_collision_y(pipe)

        if mushroom:
            self.process_mario_mushroom_collision(mushroom)

        enemy = pygame.sprite.spritecollideany(self.mario, self.level.enemy_group)
        if enemy:
            self.process_mario_enemy_collision_y(enemy)

        if checkpoint:
            self.process_mario_checkpoint_collision(checkpoint)

        piranha = pygame.sprite.spritecollideany(self.mario, self.level.plant_enemy)
        if piranha:
            self.process_mario_piranha_collision()


    def process_mario_enemy_collision_y(self, enemy):
        if self.mario.rect.y + self.mario.rect.height * 0.5 < enemy.rect.y:
            enemy.set_status(DEATH)
            self.level.death_enemy_group.add(enemy)
            self.level.enemy_group.remove(enemy)


    # 处理mario在y轴上的碰撞
    def process_mario_collision_y(self, collider):
        if self.mario.rect.y < collider.rect.y:
            self.mario.rect.bottom = collider.rect.top
        elif self.mario.rect.y > collider.rect.y:
            self.mario.rect.top = collider.rect.bottom
            # 当mario用头撞击物体时, 处理奖励
            if collider.type == 2100:
                collider.bump(self.coin_group, self.mario)
            else:
                collider.bump(self.mushroom_group, self.mario)

        # mairo在y轴方向遇到碰撞, 垂直速度置为0
        self.mario.speed_y = 0

        # 如果mario在跳跃中遇到y轴方向的碰撞
        # 水平速度置为0
        if self.mario.status == JUMP:
            self.mario.speed_x = 0
            self.mario.status = STAND


    # 移动物体
    # 移动后检测碰撞并处理碰撞
    def move_item(self, item_group):
        for item in item_group:
            item.rect.x += item.speed_x
            self.check_item_collision_x(item)

            if item.speed_y != 0:
                item.rect.y += item.speed_y
                self.check_item_collision_y(item)


    # 检测物体在x轴方向的碰撞
    # 碰到砖块, 水管则调转方向
    def check_item_collision_x(self, item):
        brick = pygame.sprite.spritecollideany(item, self.level.brick_group)
        pipe = pygame.sprite.spritecollideany(item, self.level.pipe_group)

        if brick:
            item.rotate_direction()

        if pipe:
            item.rotate_direction()


    # 检测物体在y轴方向的碰撞
    def check_item_collision_y(self, item):
        brick = pygame.sprite.spritecollideany(item, self.level.brick_group)
        pipe = pygame.sprite.spritecollideany(item, self.level.pipe_group)

        if brick:
            if item.rect.y < brick.rect.y:
                item.rect.bottom = brick.rect.top
            item.speed_y = 0

        if pipe:
            if item.rect.y < pipe.rect.y:
                item.rect.bottom = pipe.rect.top
            item.speed_y = 0


    def check_mario_border(self):
        if self.mario.rect.left < 0:
            self.mario.rect.left = 0

        if self.mario.rect.right > 800:
            self.mario.rect.right = 800

        if self.mario.rect.top < 0:
            self.mario.rect.top = 0

        if self.mario.rect.bottom > 600:
            self.mario.rect.bottom = 600


    # 展示信息
    def show_info(self):
        write_chars(self.screen, "分数: " + str(self.mario.score), 32, WHITE, (650, 0))
        write_chars(self.screen, "硬币: " + str(self.mario.coin_num), 32, WHITE, (650, 32))
        write_chars(self.screen, "生命: " + str(self.mario.life), 32, WHITE, (650, 64))


    def process_event(self, event):
        self.gui.process_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.mario.set_status(WALK)
                self.mario.set_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.mario.set_status(WALK)
                self.mario.set_direction(RIGHT)
            elif event.key == pygame.K_a:
                self.mario.set_status(JUMP)


