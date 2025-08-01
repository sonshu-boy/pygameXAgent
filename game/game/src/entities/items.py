"""
遊戲道具類別定義
"""

import pygame
import math
from constants import *


class HealthItem:
    """血量道具"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = HEALTH_ITEM_SIZE
        self.alive = True
        self.spawn_time = pygame.time.get_ticks()
        self.float_offset = 0  # 浮動動畫偏移
        self.collected = False

        # 道具會在地面上方稍微浮動
        self.base_y = y - self.size - 10  # 在地面上方

    def update(self):
        """更新血量道具"""
        current_time = pygame.time.get_ticks()

        # 浮動動畫
        self.float_offset = math.sin((current_time - self.spawn_time) / 300.0) * 5

        # 檢查是否超時（30秒後消失）
        if current_time - self.spawn_time > 30000:
            self.alive = False

    def get_rect(self):
        """獲取道具碰撞矩形"""
        actual_y = self.base_y + self.float_offset
        return pygame.Rect(
            self.x - self.size // 2, actual_y - self.size // 2, self.size, self.size
        )

    def collect(self, player):
        """玩家拾取道具"""
        if not self.collected and self.alive:
            if self.get_rect().colliderect(player.get_rect()):
                if player.health < 3:  # 只有未滿血時才能拾取
                    player.health = min(player.health + HEALTH_ITEM_RESTORE, 3)
                    self.collected = True
                    self.alive = False

                    # 添加治療特效
                    try:
                        from ..systems.particle_system import particle_system

                        heal_x = self.x
                        heal_y = self.base_y + self.float_offset
                        particle_system.create_heal_effect(
                            heal_x, heal_y, HEALTH_ITEM_RESTORE
                        )
                    except ImportError:
                        pass  # 如果粒子系統不可用就跳過特效

                    return True
        return False

    def draw(self, screen):
        """繪製血量道具"""
        if not self.alive:
            return

        actual_y = self.base_y + self.float_offset

        # 繪製愛心形狀的血量道具
        # 使用多個圓形組成愛心
        heart_color = (255, 100, 100)  # 淺紅色
        glow_color = (255, 150, 150)  # 發光效果

        # 發光效果
        for i in range(3):
            glow_size = self.size // 2 + i * 2
            alpha = 50 - i * 15
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
            glow_surface.set_alpha(alpha)
            glow_surface.set_colorkey(BLACK)
            pygame.draw.circle(
                glow_surface, glow_color, (glow_size, glow_size), glow_size
            )
            screen.blit(glow_surface, (self.x - glow_size, actual_y - glow_size))

        # 主體愛心
        heart_size = self.size // 2
        # 愛心由三個圓形組成
        pygame.draw.circle(
            screen,
            heart_color,
            (int(self.x - heart_size // 2), int(actual_y - heart_size // 3)),
            heart_size // 2,
        )
        pygame.draw.circle(
            screen,
            heart_color,
            (int(self.x + heart_size // 2), int(actual_y - heart_size // 3)),
            heart_size // 2,
        )
        pygame.draw.circle(
            screen,
            heart_color,
            (int(self.x), int(actual_y + heart_size // 3)),
            heart_size // 2,
        )

        # 十字標記表示醫療
        cross_size = 6
        pygame.draw.line(
            screen,
            WHITE,
            (self.x - cross_size, actual_y),
            (self.x + cross_size, actual_y),
            2,
        )
        pygame.draw.line(
            screen,
            WHITE,
            (self.x, actual_y - cross_size),
            (self.x, actual_y + cross_size),
            2,
        )


class HealthItemSpawner:
    """血量道具生成器"""

    def __init__(self):
        self.last_spawn_time = pygame.time.get_ticks()
        self.items = []

    def update(self, platform_system=None):
        """更新道具生成器"""
        current_time = pygame.time.get_ticks()

        # 檢查是否需要生成新道具
        if current_time - self.last_spawn_time > HEALTH_ITEM_SPAWN_INTERVAL:
            self.spawn_health_item(platform_system)
            self.last_spawn_time = current_time

        # 更新現有道具
        for item in self.items[:]:
            item.update()
            if not item.alive:
                self.items.remove(item)

    def spawn_health_item(self, platform_system=None):
        """生成血量道具"""
        import random

        # 隨機選擇生成位置
        possible_positions = []

        # 地面位置
        for i in range(5):
            x = random.randint(50, WINDOW_WIDTH - 50)
            possible_positions.append((x, GROUND_Y))

        # 平台位置
        if platform_system:
            for platform in platform_system.platforms:
                # 在平台上隨機生成
                x = random.randint(
                    int(platform.x + 20), int(platform.x + platform.width - 20)
                )
                possible_positions.append((x, platform.y))

        if possible_positions:
            x, y = random.choice(possible_positions)
            item = HealthItem(x, y)
            self.items.append(item)

    def check_collection(self, player):
        """檢查玩家是否拾取道具"""
        for item in self.items[:]:
            if item.collect(player):
                return True
        return False

    def draw(self, screen):
        """繪製所有道具"""
        for item in self.items:
            item.draw(screen)

    def clear_all(self):
        """清空所有道具"""
        self.items.clear()
