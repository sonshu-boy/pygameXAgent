"""
平台系統 - 處理可跳躍的平台
"""

import pygame
from constants import *


class Platform:
    """可跳躍的平台"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def get_rect(self):
        """獲取平台碰撞矩形"""
        return self.rect

    def draw(self, screen):
        """繪製平台"""
        # 繪製平台主體
        pygame.draw.rect(screen, PLATFORM_COLOR, self.rect)
        # 繪製平台邊框
        pygame.draw.rect(screen, PLATFORM_BORDER_COLOR, self.rect, 3)


class PlatformSystem:
    """平台系統管理器"""

    def __init__(self):
        self.platforms = []

    def add_platform(self, x, y, width, height):
        """添加新平台"""
        platform = Platform(x, y, width, height)
        self.platforms.append(platform)
        return platform

    def clear_platforms(self):
        """清除所有平台"""
        self.platforms.clear()

    def check_collision(self, entity_rect, vel_y):
        """
        檢查實體與平台的碰撞
        返回 (碰撞的平台, 新的y位置) 或 (None, None)
        """
        for platform in self.platforms:
            platform_rect = platform.get_rect()

            # 只在實體向下移動且從上方接觸平台時才處理碰撞
            if (
                vel_y >= 0
                and entity_rect.colliderect(platform_rect)
                and entity_rect.bottom - vel_y <= platform_rect.top + 5
            ):  # 5像素容差

                # 將實體放置在平台上方
                new_y = platform_rect.top - entity_rect.height
                return platform, new_y

        return None, None

    def is_on_platform(self, entity_rect):
        """檢查實體是否站在平台上"""
        # 向下延伸一點檢查是否觸碰平台
        check_rect = pygame.Rect(
            entity_rect.x, entity_rect.bottom, entity_rect.width, 5
        )

        for platform in self.platforms:
            if check_rect.colliderect(platform.get_rect()):
                return True
        return False

    def get_nearest_platform_above(self, x, y, max_distance=200):
        """
        獲取指定位置上方最近的平台
        用於敵人AI決定跳躍目標
        """
        nearest_platform = None
        min_distance = float("inf")

        for platform in self.platforms:
            platform_rect = platform.get_rect()

            # 檢查平台是否在上方且在合理的水平範圍內
            if (
                platform_rect.bottom < y  # 平台在上方
                and abs(platform_rect.centerx - x) < max_distance  # 水平距離合理
                and y - platform_rect.bottom < max_distance
            ):  # 垂直距離合理

                distance = (
                    (platform_rect.centerx - x) ** 2 + (platform_rect.centery - y) ** 2
                ) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    nearest_platform = platform

        return nearest_platform

    def draw(self, screen):
        """繪製所有平台"""
        for platform in self.platforms:
            platform.draw(screen)
