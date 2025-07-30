"""
遊戲物件類別定義 - 平台、敵人、起司等
"""

import pygame
import random
import math
from config.settings import *


class Platform:
    """平台類別"""
    def __init__(self, x, y, width, height, color=BROWN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface, camera_offset_y=0):
        """繪製平台"""
        draw_rect = pygame.Rect(
            self.rect.x,
            self.rect.y + camera_offset_y,
            self.rect.width,
            self.rect.height,
        )
        if -50 <= draw_rect.y <= WINDOW_HEIGHT + 50:  # 只繪製螢幕內的物件
            pygame.draw.rect(surface, self.color, draw_rect)
            pygame.draw.rect(surface, BLACK, draw_rect, 2)


class Enemy:
    """敵人類別"""
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 30
        self.enemy_type = enemy_type
        self.health = ENEMY_BASIC_HEALTH if enemy_type == "basic" else ENEMY_BOSS_HEALTH
        self.max_health = self.health
        self.speed = ENEMY_BASIC_SPEED if enemy_type == "basic" else ENEMY_BOSS_SPEED
        self.direction = random.choice([-1, 1])
        self.attack_timer = 0
        self.patrol_range = ENEMY_PATROL_RANGE
        self.start_x = x

    def update(self, platforms, player):
        """更新敵人狀態"""
        # 簡單的巡邏AI
        self.x += self.direction * self.speed

        # 巡邏範圍限制
        if abs(self.x - self.start_x) > self.patrol_range:
            self.direction *= -1

        # 平台邊緣檢測
        on_platform = False
        for platform in platforms:
            enemy_rect = pygame.Rect(self.x, self.y + self.height, self.width, 1)
            if enemy_rect.colliderect(platform.rect):
                on_platform = True
                break

        if not on_platform:
            self.direction *= -1

        # 攻擊計時器
        if self.attack_timer > 0:
            self.attack_timer -= 1

    def take_damage(self, damage):
        """受到傷害"""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_offset_y=0):
        """繪製敵人"""
        if self.health > 0:
            draw_y = self.y + camera_offset_y
            if -50 <= draw_y <= WINDOW_HEIGHT + 50:
                # 敵人身體
                color = RED if self.enemy_type == "boss" else PURPLE
                pygame.draw.rect(surface, color, (self.x, draw_y, self.width, self.height))

                # 敵人眼睛
                pygame.draw.circle(surface, BLACK, (self.x + 6, draw_y + 8), 2)
                pygame.draw.circle(surface, BLACK, (self.x + self.width - 6, draw_y + 8), 2)

                # 血條
                if self.health < self.max_health:
                    bar_y = draw_y - 8
                    pygame.draw.rect(surface, RED, (self.x, bar_y, self.width, 4))
                    health_width = int(self.width * (self.health / self.max_health))
                    pygame.draw.rect(surface, GREEN, (self.x, bar_y, health_width, 4))


class Cheese:
    """起司類別"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 15
        self.collected = False
        self.bob_offset = 0
        self.bob_speed = 0.1

    def update(self):
        """更新起司狀態"""
        # 起司上下浮動效果
        self.bob_offset += self.bob_speed

    def collect(self):
        """收集起司"""
        self.collected = True

    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(
            self.x, self.y + math.sin(self.bob_offset) * 3, self.width, self.height
        )

    def draw(self, surface, camera_offset_y=0):
        """繪製起司"""
        if not self.collected:
            draw_y = self.y + math.sin(self.bob_offset) * 3 + camera_offset_y
            if -50 <= draw_y <= WINDOW_HEIGHT + 50:
                # 起司形狀
                pygame.draw.rect(surface, YELLOW, (self.x, draw_y, self.width, self.height))
                pygame.draw.circle(surface, YELLOW, (self.x + 5, draw_y + 3), 3)
                pygame.draw.circle(surface, YELLOW, (self.x + 15, draw_y + 8), 2)
                # 起司孔洞
                pygame.draw.circle(surface, ORANGE, (self.x + 8, draw_y + 8), 2)
                pygame.draw.circle(surface, ORANGE, (self.x + 4, draw_y + 6), 1)
