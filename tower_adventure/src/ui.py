"""
遊戲UI和介面模組
"""

import pygame
from config.settings import *


class FontManager:
    """字體管理器"""

    def __init__(self):
        try:
            self.font_large = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(FONT_PATH, FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.Font(FONT_PATH, FONT_SIZE_SMALL)
        except:
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)


class GameUI:
    """遊戲UI類別"""

    def __init__(self):
        self.fonts = FontManager()

    def draw_health_bar(self, surface, player):
        """繪製生命值條"""
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 20

        # 血條背景
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))

        # 血條
        health_width = int(bar_width * (player.health / player.max_health))
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))

        # 血條邊框
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # 血量文字
        health_text = f"生命: {player.health}/{player.max_health}"
        text_surface = self.fonts.font_small.render(health_text, True, WHITE)
        surface.blit(text_surface, (bar_x, bar_y + bar_height + 5))

        return bar_x, bar_y, bar_height

    def draw_game_stats(self, surface, player, bar_x, bar_y, bar_height):
        """繪製遊戲統計資訊"""
        # 起司計數
        cheese_text = f"起司: {player.cheese_count}"
        text_surface = self.fonts.font_small.render(cheese_text, True, WHITE)
        surface.blit(text_surface, (bar_x, bar_y + bar_height + 25))

        # 進度顯示
        progress = min(int(player.y / SECTION_HEIGHT), 4)
        total_progress = TOTAL_SECTIONS
        progress_text = f"進度: {progress + 1}/{total_progress}"
        text_surface = self.fonts.font_small.render(progress_text, True, WHITE)
        surface.blit(text_surface, (bar_x, bar_y + bar_height + 45))

        # 高度顯示
        height_text = f"高度: {int(player.y)}m"
        text_surface = self.fonts.font_small.render(height_text, True, WHITE)
        surface.blit(text_surface, (bar_x, bar_y + bar_height + 65))

        # 跳躍能力顯示
        jump_text = f"跳躍: {player.max_jumps}段跳"
        text_surface = self.fonts.font_small.render(jump_text, True, WHITE)
        surface.blit(text_surface, (bar_x, bar_y + bar_height + 85))

        # 新手提示 - 只在安全區域顯示
        if player.y < 100:  # 在安全區域附近
            tutorial_text = "歡迎！這裡是安全區域，準備好開始冒險了嗎？"
            text_surface = self.fonts.font_small.render(tutorial_text, True, GREEN)
            surface.blit(text_surface, (bar_x, bar_y + bar_height + 105))

    def draw_controls(self, surface):
        """繪製操作說明"""
        controls = [
            "操作說明:",
            "A/D - 左右移動",
            "S - 滑行",
            "空白鍵 - 跳躍",
            "長按空白 - 高跳躍",
            "連續按空白 - 多段跳",
            "左鍵 - 攻擊",
            "長按左鍵 - 蓄力攻擊",
            "右鍵 - 防禦",
            "Shift - 跑步",
        ]

        for i, control in enumerate(controls):
            text_surface = self.fonts.font_small.render(control, True, WHITE)
            surface.blit(text_surface, (WINDOW_WIDTH - 200, 20 + i * 20))

    def draw_charge_indicator(self, surface, charge_time, max_charge_time):
        """繪製蓄力攻擊指示器"""
        if charge_time > 0:
            charge_width = 100
            charge_height = 10
            charge_x = WINDOW_WIDTH // 2 - charge_width // 2
            charge_y = WINDOW_HEIGHT - 50

            # 蓄力條背景
            pygame.draw.rect(
                surface, GRAY, (charge_x, charge_y, charge_width, charge_height)
            )

            # 蓄力條
            charge_progress = charge_time / max_charge_time
            charge_fill_width = int(charge_width * charge_progress)
            color = YELLOW if charge_progress < 1.0 else RED
            pygame.draw.rect(
                surface, color, (charge_x, charge_y, charge_fill_width, charge_height)
            )

            # 蓄力條邊框
            pygame.draw.rect(
                surface, WHITE, (charge_x, charge_y, charge_width, charge_height), 2
            )

    def draw_game_over(self, surface):
        """繪製遊戲結束畫面"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        # 遊戲結束文字
        game_over_text = "遊戲結束！"
        text_surface = self.fonts.font_large.render(game_over_text, True, RED)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        surface.blit(text_surface, text_rect)

        restart_text = "按 R 重新開始"
        text_surface = self.fonts.font_medium.render(restart_text, True, WHITE)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
        )
        surface.blit(text_surface, text_rect)

    def draw_victory(self, surface, cheese_count):
        """繪製勝利畫面"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        # 勝利文字
        victory_text = "恭喜！起司小子成功回到地面！"
        text_surface = self.fonts.font_large.render(victory_text, True, GREEN)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        surface.blit(text_surface, text_rect)

        score_text = f"收集起司數: {cheese_count}"
        text_surface = self.fonts.font_medium.render(score_text, True, WHITE)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        surface.blit(text_surface, text_rect)

        restart_text = "按 R 重新開始"
        text_surface = self.fonts.font_medium.render(restart_text, True, WHITE)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        )
        surface.blit(text_surface, text_rect)

    def draw_upgrade_menu(self, surface, player, upgrade_options):
        """繪製升級選單"""
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        # 升級選單標題
        progress = min(int(player.y / SECTION_HEIGHT), 4)
        title_text = f"到達區域 {progress + 1}！選擇獎勵："
        text_surface = self.fonts.font_large.render(title_text, True, GREEN)
        text_rect = text_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)
        )
        surface.blit(text_surface, text_rect)

        # 升級選項
        for i, option in enumerate(upgrade_options):
            option_text = f"{i+1}. {option['name']}"
            text_surface = self.fonts.font_medium.render(option_text, True, WHITE)
            text_rect = text_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20 + i * 40)
            )
            surface.blit(text_surface, text_rect)
