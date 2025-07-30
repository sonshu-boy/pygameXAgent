"""
主要遊戲邏輯模組
"""

import pygame
from config.settings import *
from src.player import Player
from src.ui import GameUI
from levels.level_generator import LevelGenerator


class Game:
    """遊戲主類別"""

    def __init__(self):
        # 先生成關卡，然後將玩家放在安全位置
        self.platforms, self.enemies, self.cheeses = (
            LevelGenerator.generate_complete_tower()
        )

        # 將玩家放在安全起始平台上（區域1的安全平台）
        safe_platform_x = 500  # 安全平台中心
        safe_platform_y = 20  # 安全平台Y位置
        self.player = Player(
            safe_platform_x - 15, safe_platform_y - 40
        )  # 玩家在平台上方

        self.camera_y = 0
        self.game_state = "playing"  # playing, game_over, victory, upgrade
        self.upgrade_options = []
        self.ui = GameUI()
        self.safe_platform_heal_timer = 0  # 安全平台治療計時器

    def update(self):
        """更新遊戲狀態"""
        if self.game_state == "playing":
            # 更新玩家
            self.player.update(self.platforms, self.enemies)

            # 檢查玩家是否在安全平台上並提供治療
            self.check_safe_platform_healing()

            # 更新敵人
            for enemy in self.enemies:
                enemy.update(self.platforms, self.player)

            # 更新起司
            for cheese in self.cheeses:
                cheese.update()
                if not cheese.collected and self.player.get_rect().colliderect(
                    cheese.get_rect()
                ):
                    cheese.collect()
                    self.player.collect_cheese()

            # 更新攝影機
            target_camera_y = self.player.y - WINDOW_HEIGHT // 2
            self.camera_y += (target_camera_y - self.camera_y) * 0.1

            # 檢查玩家是否死亡
            if self.player.health <= 0:
                self.game_state = "game_over"

            # 檢查是否到達終點（連續關卡系統）
            if self.player.y >= TOTAL_TOWER_HEIGHT - 200:
                self.game_state = "victory"

            # 基於高度的進度系統，每下降一定距離給予獎勵
            current_progress = int(self.player.y / SECTION_HEIGHT)
            if current_progress > 0 and current_progress < TOTAL_SECTIONS:
                # 檢查是否需要顯示獎勵（可以添加標記避免重複觸發）
                if not hasattr(self, "last_progress"):
                    self.last_progress = 0
                if current_progress > self.last_progress:
                    self.last_progress = current_progress
                    self.show_progress_reward()

    def check_safe_platform_healing(self):
        """檢查玩家是否在安全平台上並提供治療"""
        player_rect = self.player.get_rect()
        is_on_safe_platform = False

        # 檢查是否站在綠色（安全）平台上
        for platform in self.platforms:
            if (
                platform.color == GREEN
                and player_rect.colliderect(platform.rect)
                and self.player.vel_y >= 0
                and player_rect.bottom <= platform.rect.top + 10
            ):
                is_on_safe_platform = True
                break

        if is_on_safe_platform:
            self.safe_platform_heal_timer += 1
            # 每2秒（120幀）恢復5點生命值
            if self.safe_platform_heal_timer >= 120:
                if self.player.health < self.player.max_health:
                    self.player.health = min(
                        self.player.health + 5, self.player.max_health
                    )
                self.safe_platform_heal_timer = 0
        else:
            self.safe_platform_heal_timer = 0

    def show_progress_reward(self):
        """顯示進度獎勵選單"""
        self.game_state = "upgrade"
        self.upgrade_options = [
            {"name": "恢復生命值 +30", "type": "health"},
            {"name": "增加攻擊力 +5", "type": "attack"},
            {"name": "獲得額外跳躍 (三段跳)", "type": "extra_jump"},
        ]

    def apply_upgrade(self, upgrade_type):
        """應用升級"""
        if upgrade_type == "health":
            self.player.max_health += 20
            self.player.health = min(self.player.health + 30, self.player.max_health)
        elif upgrade_type == "attack":
            self.player.attack_power += 5
        elif upgrade_type == "extra_jump":
            self.player.max_jumps = min(self.player.max_jumps + 1, 3)  # 最多三段跳

        self.game_state = "playing"

    def reset_game(self):
        """重置遊戲"""
        # 重新生成塔樓
        self.platforms, self.enemies, self.cheeses = (
            LevelGenerator.generate_complete_tower()
        )

        # 將玩家重新放在安全起始平台上
        safe_platform_x = 500  # 安全平台中心
        safe_platform_y = 20  # 安全平台Y位置
        self.player = Player(
            safe_platform_x - 15, safe_platform_y - 40
        )  # 玩家在平台上方

        self.camera_y = 0
        self.game_state = "playing"
        self.last_progress = 0
        self.safe_platform_heal_timer = 0

    def draw(self, surface):
        """繪製遊戲"""
        # 清除螢幕
        surface.fill(BLACK)

        # 計算攝影機偏移量
        camera_offset_y = -self.camera_y

        # 繪製平台
        for platform in self.platforms:
            platform.draw(surface, camera_offset_y)

        # 繪製起司
        for cheese in self.cheeses:
            cheese.draw(surface, camera_offset_y)

        # 繪製敵人
        for enemy in self.enemies:
            enemy.draw(surface, camera_offset_y)

        # 繪製玩家
        self.player.draw(surface, camera_offset_y)

        # 繪製UI
        self.draw_ui(surface)

    def draw_ui(self, surface):
        """繪製UI元素"""
        # 基本UI
        bar_x, bar_y, bar_height = self.ui.draw_health_bar(surface, self.player)
        self.ui.draw_game_stats(surface, self.player, bar_x, bar_y, bar_height)
        self.ui.draw_controls(surface)

        # 安全平台提示
        self.draw_safe_platform_status(surface)

        # 遊戲狀態相關UI
        if self.game_state == "game_over":
            self.ui.draw_game_over(surface)
        elif self.game_state == "victory":
            self.ui.draw_victory(surface, self.player.cheese_count)
        elif self.game_state == "upgrade":
            self.ui.draw_upgrade_menu(surface, self.player, self.upgrade_options)

    def draw_safe_platform_status(self, surface):
        """繪製安全平台狀態提示"""
        player_rect = self.player.get_rect()
        is_on_safe_platform = False

        # 檢查是否站在綠色（安全）平台上
        for platform in self.platforms:
            if (
                platform.color == GREEN
                and player_rect.colliderect(platform.rect)
                and self.player.vel_y >= 0
                and player_rect.bottom <= platform.rect.top + 10
            ):
                is_on_safe_platform = True
                break

        if is_on_safe_platform:
            # 顯示安全平台提示
            safe_text = "安全區域 - 正在治療中..."
            text_surface = self.ui.fonts.font_medium.render(safe_text, True, GREEN)
            text_rect = text_surface.get_rect()
            text_rect.centerx = WINDOW_WIDTH // 2
            text_rect.y = 100

            # 背景框
            bg_rect = text_rect.copy()
            bg_rect.inflate(20, 10)
            pygame.draw.rect(surface, BLACK, bg_rect)
            pygame.draw.rect(surface, GREEN, bg_rect, 2)

            surface.blit(text_surface, text_rect)

            # 治療進度條
            if self.safe_platform_heal_timer > 0:
                progress_width = 200
                progress_height = 8
                progress_x = (WINDOW_WIDTH - progress_width) // 2
                progress_y = text_rect.bottom + 10

                # 進度條背景
                pygame.draw.rect(
                    surface,
                    DARK_GRAY,
                    (progress_x, progress_y, progress_width, progress_height),
                )

                # 進度條
                progress = min(self.safe_platform_heal_timer / 120, 1.0)
                filled_width = int(progress_width * progress)
                pygame.draw.rect(
                    surface,
                    GREEN,
                    (progress_x, progress_y, filled_width, progress_height),
                )

                # 進度條邊框
                pygame.draw.rect(
                    surface,
                    WHITE,
                    (progress_x, progress_y, progress_width, progress_height),
                    1,
                )
