"""
主選單畫面
"""

import pygame
from constants import *
from systems.font_manager import get_font
from systems.sound_manager import sound_manager


class MainMenu:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font_large = get_font("large")
        self.font_medium = get_font("medium")
        self.font_small = get_font("small")
        self.selected_option = 0
        self.menu_options = ["開始遊戲", "遊戲說明", "音樂設定", "退出遊戲"]
        self.music_volume = sound_manager.bgm_volume
        self.showing_music_menu = False

    def handle_event(self, event):
        """處理選單事件"""
        if event.type == pygame.KEYDOWN:
            if self.showing_music_menu:
                self._handle_music_menu_event(event)
            else:
                self._handle_main_menu_event(event)

    def _handle_main_menu_event(self, event):
        """處理主選單事件"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self._select_option()

    def _handle_music_menu_event(self, event):
        """處理音樂設定選單事件"""
        if event.key == pygame.K_ESCAPE:
            self.showing_music_menu = False
        elif event.key == pygame.K_LEFT:
            self.music_volume = max(0.0, self.music_volume - 0.1)
            sound_manager.set_bgm_volume(self.music_volume)
            # 更新原始音量，以便關卡中的50%計算基於新音量
            sound_manager.original_bgm_volume = self.music_volume
        elif event.key == pygame.K_RIGHT:
            self.music_volume = min(1.0, self.music_volume + 0.1)
            sound_manager.set_bgm_volume(self.music_volume)
            # 更新原始音量，以便關卡中的50%計算基於新音量
            sound_manager.original_bgm_volume = self.music_volume
        elif event.key == pygame.K_m:
            # 切換背景音樂開關
            if sound_manager.is_bgm_playing():
                sound_manager.stop_background_music()
            else:
                sound_manager.play_background_music()

    def _select_option(self):
        """執行選中的選項"""
        if self.selected_option == 0:  # 開始遊戲
            self._show_level_select()
        elif self.selected_option == 1:  # 遊戲說明
            self.state_manager.change_state(INSTRUCTIONS_STATE)
        elif self.selected_option == 2:  # 音樂設定
            self.showing_music_menu = True
        elif self.selected_option == 3:  # 退出遊戲
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
        if self.showing_music_menu:
            self._draw_music_menu(screen)
        else:
            self._draw_main_menu(screen)

    def _draw_main_menu(self, screen):
        """繪製主選單"""
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

        # 顯示背景音樂狀態
        music_status = (
            "背景音樂: 播放中" if sound_manager.is_bgm_playing() else "背景音樂: 已停止"
        )
        status_text = self.font_small.render(
            music_status, True, GREEN if sound_manager.is_bgm_playing() else RED
        )
        status_rect = status_text.get_rect(center=(WINDOW_WIDTH // 2, 600))
        screen.blit(status_text, status_rect)

    def _draw_music_menu(self, screen):
        """繪製音樂設定選單"""
        # 繪製標題
        title = self.font_large.render("音樂設定", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # 繪製音量控制
        volume_text = self.font_medium.render(
            f"音量: {int(self.music_volume * 100)}%", True, WHITE
        )
        volume_rect = volume_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        screen.blit(volume_text, volume_rect)

        # 繪製音量調整提示
        volume_hint = self.font_small.render("使用左右方向鍵調整音量", True, GRAY)
        volume_hint_rect = volume_hint.get_rect(center=(WINDOW_WIDTH // 2, 300))
        screen.blit(volume_hint, volume_hint_rect)

        # 繪製音樂控制提示
        music_status = (
            "背景音樂: 播放中" if sound_manager.is_bgm_playing() else "背景音樂: 已停止"
        )
        status_color = GREEN if sound_manager.is_bgm_playing() else RED
        status_text = self.font_medium.render(music_status, True, status_color)
        status_rect = status_text.get_rect(center=(WINDOW_WIDTH // 2, 350))
        screen.blit(status_text, status_rect)

        music_hint = self.font_small.render("按 M 鍵開關背景音樂", True, GRAY)
        music_hint_rect = music_hint.get_rect(center=(WINDOW_WIDTH // 2, 400))
        screen.blit(music_hint, music_hint_rect)

        # 繪製返回提示
        back_hint = self.font_medium.render("按 ESC 鍵返回主選單", True, YELLOW)
        back_hint_rect = back_hint.get_rect(center=(WINDOW_WIDTH // 2, 500))
        screen.blit(back_hint, back_hint_rect)
