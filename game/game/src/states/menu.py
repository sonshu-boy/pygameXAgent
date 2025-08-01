"""
主選單畫面
"""

import pygame
from constants import *
from systems.font_manager import get_font


class MainMenu:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font_large = get_font("large")
        self.font_medium = get_font("medium")
        self.selected_option = 0
        self.menu_options = ["開始遊戲", "遊戲說明", "退出遊戲"]

    def handle_event(self, event):
        """處理選單事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(
                    self.menu_options
                )
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(
                    self.menu_options
                )
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()

    def _select_option(self):
        """執行選中的選項"""
        if self.selected_option == 0:  # 開始遊戲
            self._show_level_select()
        elif self.selected_option == 1:  # 遊戲說明
            self.state_manager.change_state(INSTRUCTIONS_STATE)
        elif self.selected_option == 2:  # 退出遊戲
            pygame.quit()
            exit()

    def _show_level_select(self):
        """顯示關卡選擇界面"""
        self.state_manager.change_state(LEVEL_SELECT_STATE)

    def update(self):
        """更新選單邏輯"""
        pass

    def draw(self, screen):
        """繪製選單"""
        # 繪製標題
        title = self.font_large.render("老鼠格鬥遊戲", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # 繪製選單選項
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 60))
            screen.blit(text, text_rect)

        # 繪製操作提示
        instruction = self.font_medium.render(
            "使用方向鍵選擇，按 Enter 或空白鍵確認", True, GRAY
        )
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, 550))
        screen.blit(instruction, instruction_rect)
