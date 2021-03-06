from . singleton import *


# 游戏难度
# 当碰到敌人时， 以一定概率触发不死
# 困难
HARD =                  0.1
# 普通
NORMAL =                0.3
# 简单
EASY =                  0.5



# 场景
# NOWSCENE 当前场景
NOW_SCENE =                 0
GAME_MENU_SCENE =           1
GAME_SCENE =                2
DEATH_SCENE =               3
WIN_SCENE =                 4
SELECT_LEVEL_SCENE =        5
SELECT_DIFFICULTY_SCENE =   6


# 场景宽高
SCREEN_SIZE =       (800, 600)


# 按钮状态
BUTTON_NORMAL =     1
BUTTON_HOVER =      2
BUTTON_ACTIVE =     3


# 剪刀花的状态
PIRANHA_CLOSE =     1
PIRANHA_OPEN =      2


# 死亡场景时间
DEATH_SCENE_TIME =    180


# 标记Mario的方向
NODIRECTION =   0
LEFT =          1
RIGHT =         2
TOP =           3
BOTTOM =        4


# 标记Mario的状态
STAND =     1
WALK =      2
RUN =       3
JUMP =      4
FALL =      5
DEATH =     6


# 标记Mario的形态
SMALL =     1
BIG =       2


# 加速度
GRAVITY_X =         0.5
GRAVITY_Y =         0.9


# 最大速度
MAX_SPEED_X =   9
MAX_SPEED_Y =   20


MAX_JUMP_HEIGHT = 120


# 初始跳跃速度
SMALL_JUMP_SPEED_Y =    -13
BIG_JUMP_SPEED_Y =      -18


# 蘑菇的类型
GROW_BIGGER =   1
PLUS_LIFE =     2


# 字符初始大小
FONT_SIZE =     48


# 颜色
RED =       (255, 0, 0)
YELLOW =    (0, 255, 0)
BLUE =      (0, 0, 255)
WHITE =     (255, 255, 255)
BLACK =     (0, 0, 0)
SKYBLUE =   (135, 206, 235)
MAGENTA =   (255, 0, 255)
LIGHTBLUE = (173, 216, 230)


@Singleton
class GlobalData(object):
    def __init__(self):
        self.game_probability = EASY
        self.scene = NOW_SCENE