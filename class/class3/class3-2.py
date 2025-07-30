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
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# 主要遊戲迴圈
clock = pygame.time.Clock()

while True:
    # 控制幀率
    clock.tick(60)
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 結束pygame
            pygame.quit()
            sys.exit()

    # 填充背景顏色
    screen.fill(WHITE)

    # 1. 繪製線條
    pygame.draw.line(screen, BLACK, (50, 50), (150, 50), 2)  # 水平線
    pygame.draw.line(screen, RED, (50, 70), (150, 120), 3)  # 斜線

    # 2. 繪製矩形
    pygame.draw.rect(screen, BLUE, (200, 50, 100, 60))  # 實心矩形
    pygame.draw.rect(screen, GREEN, (320, 50, 100, 60), 2)  # 空心矩形

    # 3. 繪製圓形
    pygame.draw.circle(screen, RED, (100, 200), 40)  # 實心圓
    pygame.draw.circle(screen, PURPLE, (200, 200), 40, 3)  # 空心圓

    # 4. 繪製橢圓
    pygame.draw.ellipse(screen, YELLOW, (300, 160, 80, 50))  # 實心橢圓
    pygame.draw.ellipse(screen, ORANGE, (400, 160, 80, 50), 2)  # 空心橢圓

    # 5. 繪製弧線
    pygame.draw.arc(screen, BLACK, (450, 50, 80, 80), 0, 3.14, 3)  # 半圓弧

    # 6. 繪製多邊形 (三角形)
    triangle_points = [(100, 300), (150, 250), (200, 300)]
    pygame.draw.polygon(screen, GREEN, triangle_points)

    # 7. 繪製多邊形 (五角形)
    pentagon_points = [(350, 280), (380, 260), (410, 280), (400, 310), (360, 310)]
    pygame.draw.polygon(screen, BLUE, pentagon_points, 2)

    # 8. 繪製多條線段
    lines_points = [(500, 250), (520, 280), (540, 260), (560, 290), (580, 270)]
    pygame.draw.lines(screen, RED, False, lines_points, 2)

    # 更新畫面
    pygame.display.flip()
