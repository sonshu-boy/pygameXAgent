import pygame
import sys

# 初始化pygame
pygame.init()

# 設定視窗大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 設定視窗標題
pygame.display.set_caption("敲磚塊遊戲")

# 定義顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# 初始化字體 - 使用支援繁體中文的系統字體
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 24)


# Brick 類別定義
class Brick:
    def __init__(self, x, y, width=80, height=30, color=RED):
        """
        初始化磚塊物件
        x, y: 磚塊左上角座標
        width, height: 磚塊大小
        color: 磚塊顏色
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True  # 磚塊是否可見
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        """繪製磚塊"""
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)
            # 繪製邊框讓磚塊更明顯
            pygame.draw.rect(surface, BLACK, self.rect, 2)

    def get_rect(self):
        """取得磚塊的矩形區域"""
        return self.rect

    def hit(self):
        """磚塊被擊中時調用"""
        self.visible = False


# Paddle 類別定義 - 繼承 Brick 類別
class Paddle(Brick):
    def __init__(self, x, y, width=120, height=20, color=BLUE):
        """
        初始化擋板物件
        繼承 Brick 的屬性和方法
        """
        super().__init__(x, y, width, height, color)
        self.speed = 8  # 擋板移動速度

    def update_position(self, mouse_x):
        """
        根據滑鼠 x 位置更新擋板位置
        mouse_x: 滑鼠的 x 座標
        """
        # 將擋板中心對齊滑鼠位置
        self.x = mouse_x - self.width // 2

        # 邊界檢查，確保擋板不會移出視窗
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width

        # 更新矩形位置
        self.rect.x = self.x

    def draw(self, surface):
        """繪製擋板 - 覆寫父類別方法"""
        pygame.draw.rect(surface, self.color, self.rect)
        # 擋板使用白色邊框
        pygame.draw.rect(surface, WHITE, self.rect, 2)


# Ball 類別定義
class Ball:
    def __init__(self, x, y, radius=10, color=WHITE):
        """初始化球物件"""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 5
        self.speed_y = -5
        self.launched = False  # 球是否已發射

    def update(self, paddle=None):
        """更新球的位置"""
        if not self.launched and paddle:
            # 球尚未發射，固定在擋板上方
            self.x = paddle.x + paddle.width // 2
            self.y = paddle.y - self.radius
        else:
            # 球已發射，正常移動
            self.x += self.speed_x
            self.y += self.speed_y

            # 左右邊界反彈
            if self.x <= self.radius or self.x >= WINDOW_WIDTH - self.radius:
                self.speed_x = -self.speed_x

            # 上邊界反彈
            if self.y <= self.radius:
                self.speed_y = -self.speed_y

    def launch(self):
        """發射球"""
        self.launched = True

    def reset(self, x, y):
        """重置球的位置和狀態"""
        self.x = x
        self.y = y
        self.launched = False
        self.speed_x = 5
        self.speed_y = -5

    def draw(self, surface):
        """繪製球"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        """取得球的矩形區域"""
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def bounce_y(self):
        """Y軸反彈"""
        self.speed_y = -self.speed_y

    def bounce_x(self):
        """X軸反彈"""
        self.speed_x = -self.speed_x


# 遊戲狀態變數
game_over = False
game_won = False
score = 0

# 創建磚塊群組
bricks = []
brick_rows = 5
brick_cols = 8
brick_colors = [RED, ORANGE, YELLOW, GREEN, BLUE]

for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * 90 + 50
        brick_y = row * 40 + 50
        color = brick_colors[row % len(brick_colors)]
        brick = Brick(brick_x, brick_y, color=color)
        bricks.append(brick)

# 創建擋板
paddle = Paddle(WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT - 40)

# 創建球
ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (
                event.button == 1
                and not ball.launched
                and not game_over
                and not game_won
            ):
                # 滑鼠左鍵發射球
                ball.launch()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or game_won):
                # 重新開始遊戲
                game_over = False
                game_won = False
                score = 0
                ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                bricks = []
                for row in range(brick_rows):
                    for col in range(brick_cols):
                        brick_x = col * 90 + 50
                        brick_y = row * 40 + 50
                        color = brick_colors[row % len(brick_colors)]
                        brick = Brick(brick_x, brick_y, color=color)
                        bricks.append(brick)

    if not game_over and not game_won:
        # 取得滑鼠位置並更新擋板
        mouse_x, mouse_y = pygame.mouse.get_pos()
        paddle.update_position(mouse_x)

        # 更新球的位置
        ball.update(paddle)

        # 檢查球與擋板的碰撞（只有在球已發射時才檢查）
        if (
            ball.launched
            and ball.get_rect().colliderect(paddle.get_rect())
            and ball.speed_y > 0
        ):
            ball.bounce_y()
            # 根據擊中擋板的位置調整球的水平速度
            hit_pos = (ball.x - paddle.x) / paddle.width
            ball.speed_x = (hit_pos - 0.5) * 10

        # 檢查球與磚塊的碰撞（只有在球已發射時才檢查）
        if ball.launched:
            for brick in bricks[:]:  # 使用切片複製避免迭代時修改列表
                if brick.visible and ball.get_rect().colliderect(brick.get_rect()):
                    brick.hit()
                    ball.bounce_y()
                    score += 10
                    bricks.remove(brick)
                    break

        # 檢查遊戲結束條件（只有在球已發射時才檢查）
        if ball.launched and ball.y > WINDOW_HEIGHT:
            game_over = True

        # 檢查勝利條件
        if not any(brick.visible for brick in bricks):
            game_won = True

    # 填充背景顏色
    screen.fill(BLACK)

    # 繪製所有磚塊
    for brick in bricks:
        brick.draw(screen)

    # 繪製擋板
    paddle.draw(screen)

    # 繪製球
    if not game_over:
        ball.draw(screen)

    # 顯示分數
    score_text = f"分數: {score}"
    text_surface = font.render(score_text, True, WHITE)
    screen.blit(text_surface, (10, 10))

    # 顯示遊戲狀態
    if game_over:
        game_over_text = "遊戲結束！按 R 重新開始"
        text_surface = font.render(game_over_text, True, RED)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        screen.blit(text_surface, text_rect)
    elif game_won:
        win_text = "恭喜過關！按 R 重新開始"
        text_surface = font.render(win_text, True, GREEN)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        screen.blit(text_surface, text_rect)

    # 顯示操作說明
    if not game_over and not game_won:
        if not ball.launched:
            instruction_text = "移動滑鼠控制擋板，點擊左鍵發射球"
        else:
            instruction_text = "移動滑鼠控制擋板"
        text_surface = font.render(instruction_text, True, GRAY)
        screen.blit(text_surface, (10, WINDOW_HEIGHT - 30))

    # 更新畫面
    pygame.display.flip()
