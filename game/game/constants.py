"""
遊戲常數定義
"""

# 視窗設定
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# 顏色定義 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)

# 玩家設定
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 0.8
GROUND_Y = WINDOW_HEIGHT - 100

# 拳頭設定
FIST_SIZE = 20
FIST_CHARGED_SIZE = 35
FIST_MAX_DISTANCE = 80
FIST_SPEED = 10
FIST_RETURN_SPEED = 8

# 蓄力攻擊設定
CHARGE_TIME = 1000  # 蓄力時間 1 秒（毫秒）
CHARGE_DAMAGE_MULTIPLIER = 2  # 蓄力攻擊傷害倍數
STUN_DURATION = 100  # 眩暈持續時間（毫秒）

# 防禦設定
DEFENSE_DURATION = 1000  # 毫秒
DEFENSE_COOLDOWN = 3000  # 毫秒

# 無敵時間
INVINCIBLE_DURATION = 500  # 毫秒

# 滑行設定
SLIDE_DISTANCE = 100
SLIDE_SPEED = 8

# 敵人設定
DUMMY_WIDTH = 40
DUMMY_HEIGHT = 70

SMALL_ROBOT_WIDTH = 45
SMALL_ROBOT_HEIGHT = 50
SMALL_ROBOT_SPEED = 3
SMALL_ROBOT_CHARGE_SPEED = 8
SMALL_ROBOT_HEALTH = 3  # 需要3次普通攻擊或1次蓄力攻擊

BOSS_WIDTH = 80
BOSS_HEIGHT = 100
BOSS_SPEED = 2
BOSS_HEALTH = 10
BOSS_SPECIAL_ATTACK_THRESHOLD = 0.5  # 血量低於50%時觸發特殊攻擊

# 遊戲狀態
MENU_STATE = "menu"
GAME_STATE = "game"
LEVEL_SELECT_STATE = "level_select"
GAME_OVER_STATE = "game_over"
INSTRUCTIONS_STATE = "instructions"

# 關卡設定
LEVEL_1 = 1  # 訓練場
LEVEL_2 = 2  # 工廠
LEVEL_3 = 3  # 實驗室（BOSS）

# 字體設定
FONT_LARGE_SIZE = 48
FONT_MEDIUM_SIZE = 32
FONT_SMALL_SIZE = 24
FONT_TINY_SIZE = 18

# 支援的中文字體路徑（Windows系統）
CHINESE_FONTS = [
    "C:/Windows/Fonts/msjh.ttc",  # 微軟正黑體
    "C:/Windows/Fonts/msyh.ttc",  # 微軟雅黑
    "C:/Windows/Fonts/mingliu.ttc",  # 細明體
    "C:/Windows/Fonts/simsun.ttc",  # 宋體
]
