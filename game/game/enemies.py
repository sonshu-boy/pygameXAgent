"""
敵人類別定義
"""

import pygame
import math
import random
from constants import *


class Enemy:
    """敵人基類"""

    def __init__(self, x, y, width, height, health=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.alive = True

        # 狀態
        self.invincible = False
        self.invincible_start_time = 0
        self.stunned = False
        self.stun_start_time = 0

    def take_damage(self, damage=1, knockback=False, stun=False):
        """受到傷害"""
        if not self.invincible and self.alive:
            self.health -= damage
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

            if knockback:
                self._apply_knockback()
            if stun:
                self.stunned = True
                self.stun_start_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.alive = False

    def _apply_knockback(self):
        """應用擊退效果（子類重寫）"""
        pass

    def update(self, player):
        """更新敵人狀態（子類重寫）"""
        current_time = pygame.time.get_ticks()

        # 更新無敵時間
        if self.invincible:
            if current_time - self.invincible_start_time > INVINCIBLE_DURATION:
                self.invincible = False

        # 更新眩暈狀態
        if self.stunned:
            if current_time - self.stun_start_time > STUN_DURATION:
                self.stunned = False

    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """繪製敵人（子類重寫）"""
        pass


class TrainingDummy(Enemy):
    """訓練用人偶 - 第一關敵人"""

    def __init__(self, x, y):
        super().__init__(x, y, DUMMY_WIDTH, DUMMY_HEIGHT, health=3)
        self.color = GRAY

    def update(self, player):
        """更新訓練人偶（不主動攻擊）"""
        super().update(player)

        # 地面碰撞
        if self.y + self.height < GROUND_Y:
            self.y = GROUND_Y - self.height

    def draw(self, screen):
        """繪製訓練人偶"""
        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製十字標記
        cross_size = 10
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        pygame.draw.line(
            screen,
            RED,
            (center_x - cross_size, center_y),
            (center_x + cross_size, center_y),
            3,
        )
        pygame.draw.line(
            screen,
            RED,
            (center_x, center_y - cross_size),
            (center_x, center_y + cross_size),
            3,
        )


class SmallRobot(Enemy):
    """小型老鼠機器人 - 第二關敵人"""

    def __init__(self, x, y):
        super().__init__(
            x, y, SMALL_ROBOT_WIDTH, SMALL_ROBOT_HEIGHT, health=SMALL_ROBOT_HEALTH
        )
        self.color = (100, 100, 150)  # 藍灰色
        self.speed = SMALL_ROBOT_SPEED
        self.charging = False
        self.charge_speed = SMALL_ROBOT_CHARGE_SPEED
        self.charge_cooldown = 0
        self.direction = 1  # 1 為右，-1 為左

    def update(self, player):
        """更新小型機器人"""
        super().update(player)
        current_time = pygame.time.get_ticks()

        if not self.stunned:
            # 計算與玩家的距離
            distance_to_player = abs(self.x - player.x)

            # 如果玩家在附近且冷卻時間結束，開始衝撞
            if distance_to_player < 200 and current_time > self.charge_cooldown:
                if not self.charging:
                    self.charging = True
                    self.direction = 1 if player.x > self.x else -1

            # 執行衝撞
            if self.charging:
                self.x += self.direction * self.charge_speed

                # 檢查是否衝撞到玩家
                if self.get_rect().colliderect(player.get_rect()):
                    player.take_damage()
                    self.charging = False
                    self.charge_cooldown = current_time + 2000  # 2秒冷卻

                # 檢查是否衝出螢幕或撞牆
                if self.x < -50 or self.x > WINDOW_WIDTH + 50:
                    self.charging = False
                    self.charge_cooldown = current_time + 2000
                    # 重新定位到螢幕內
                    self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))

            else:
                # 普通移動
                self.x += self.direction * self.speed

                # 邊界反彈
                if self.x <= 0 or self.x >= WINDOW_WIDTH - self.width:
                    self.direction *= -1

        # 地面碰撞
        if self.y + self.height < GROUND_Y:
            self.y = GROUND_Y - self.height

    def _apply_knockback(self):
        """應用擊退效果"""
        self.charging = False  # 停止衝撞
        self.charge_cooldown = pygame.time.get_ticks() + 1500

    def draw(self, screen):
        """繪製小型機器人"""
        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW  # 眩暈時變黃
        elif self.charging:
            color = RED  # 衝撞時變紅
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製機械眼睛
        eye_size = 3
        pygame.draw.circle(screen, RED, (int(self.x + 10), int(self.y + 10)), eye_size)
        pygame.draw.circle(screen, RED, (int(self.x + 30), int(self.y + 10)), eye_size)


class GiantRobot(Enemy):
    """巨型老鼠機器人 - 第三關BOSS"""

    def __init__(self, x, y):
        super().__init__(x, y, BOSS_WIDTH, BOSS_HEIGHT, health=BOSS_HEALTH)
        self.color = (150, 50, 50)  # 深紅色
        self.speed = BOSS_SPEED
        self.direction = 1
        self.attack_cooldown = 0
        self.special_attack_cooldown = 0
        self.attack_pattern = 0  # 攻擊模式

    def update(self, player):
        """更新巨型機器人BOSS"""
        super().update(player)
        current_time = pygame.time.get_ticks()

        if not self.stunned:
            # 移動朝向玩家
            if abs(self.x - player.x) > 50:
                if player.x > self.x:
                    self.x += self.speed
                    self.direction = 1
                else:
                    self.x -= self.speed
                    self.direction = -1

            # 普通攻擊
            if current_time > self.attack_cooldown:
                distance_to_player = abs(self.x - player.x)
                if distance_to_player < 100:
                    # 近距離攻擊
                    if self.get_rect().colliderect(player.get_rect()):
                        player.take_damage()
                        self.attack_cooldown = current_time + 1500

            # 特殊攻擊 - 當血量低於50%時觸發
            if (self.health / self.max_health) <= BOSS_SPECIAL_ATTACK_THRESHOLD:
                if current_time > self.special_attack_cooldown:
                    self._special_attack(player)
                    self.special_attack_cooldown = current_time + 5000  # 5秒冷卻

        # 地面碰撞
        if self.y + self.height < GROUND_Y:
            self.y = GROUND_Y - self.height

        # 邊界限制
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))

    def _special_attack(self, player):
        """特殊攻擊技能 - 範圍攻擊"""
        # 強力範圍攻擊，只能通過防禦抵擋
        distance_to_player = abs(self.x - player.x)
        if distance_to_player < 200:  # 更大的攻擊範圍
            if not player.is_defending:
                player.take_damage()
                # 可以在這裡添加視覺效果表示範圍攻擊

    def _apply_knockback(self):
        """BOSS受到擊退效果較小"""
        # BOSS較重，擊退效果減弱
        pass

    def take_damage(self, damage=1, knockback=False, stun=False):
        """BOSS受傷處理 - 只有蓄力攻擊才能造成傷害"""
        # BOSS只會受到蓄力攻擊的傷害
        if damage >= CHARGE_DAMAGE_MULTIPLIER and not self.invincible and self.alive:
            self.health -= damage
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

            if knockback:
                self._apply_knockback()
            if stun:
                self.stunned = True
                self.stun_start_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.alive = False

    def draw(self, screen):
        """繪製巨型機器人BOSS"""
        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製威脅性的紅眼
        eye_size = 6
        pygame.draw.circle(screen, RED, (int(self.x + 20), int(self.y + 20)), eye_size)
        pygame.draw.circle(screen, RED, (int(self.x + 60), int(self.y + 20)), eye_size)

        # 繪製血量條
        self._draw_health_bar(screen)

    def _draw_health_bar(self, screen):
        """繪製BOSS血量條"""
        bar_width = 200
        bar_height = 10
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = 30

        # 背景
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

        # 血量
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        color = GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.2 else RED)
        pygame.draw.rect(screen, color, (bar_x, bar_y, health_width, bar_height))

        # 邊框
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
