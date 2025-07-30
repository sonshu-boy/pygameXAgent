import pygame
import sys

# 初始化pygame
pygame.init()

# 設定視窗大小
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 設定視窗標題
pygame.display.set_caption("pygame圖案繪製範例")

# 定義顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# 顏色列表用於循環變換
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]

# 初始化字體 - 使用支援繁體中文的系統字體
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 24)

# 方塊設定
square_size = 50
square_x = WINDOW_WIDTH // 2 - square_size // 2
square_y = WINDOW_HEIGHT // 2 - square_size // 2
move_speed = 5

# 顏色變換設定
current_color_index = 0
total_distance = 0
COLOR_CHANGE_DISTANCE = 50

# 主要遊戲迴圈
clock = pygame.time.Clock()

while True:
    # 控制幀率
    clock.tick(60)

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 偵測按鍵狀態
    keys = pygame.key.get_pressed()

    # WASD控制移動
    moved = False
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        square_y -= move_speed
        moved = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        square_y += move_speed
        moved = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        square_x -= move_speed
        moved = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        square_x += move_speed
        moved = True

    # 追蹤移動距離並變換顏色
    if moved:
        total_distance += move_speed
        if total_distance >= COLOR_CHANGE_DISTANCE:
            current_color_index = (current_color_index + 1) % len(COLORS)
            total_distance = 0

    # 邊界檢查
    if square_x < 0:
        square_x = 0
    elif square_x > WINDOW_WIDTH - square_size:
        square_x = WINDOW_WIDTH - square_size
    if square_y < 0:
        square_y = 0
    elif square_y > WINDOW_HEIGHT - square_size:
        square_y = WINDOW_HEIGHT - square_size

    # 計算方塊中心座標
    center_x = square_x + square_size // 2
    center_y = square_y + square_size // 2

    # 填充背景顏色
    screen.fill(WHITE)

    # 繪製紅色方塊
    current_color = COLORS[current_color_index]
    pygame.draw.rect(
        screen, current_color, (square_x, square_y, square_size, square_size)
    )

    # 顯示方塊中心座標
    coord_text = f"中心座標: ({center_x}, {center_y})"
    text_surface = font.render(coord_text, True, BLACK)
    screen.blit(text_surface, (10, 10))

    # 更新畫面
    pygame.display.flip()
