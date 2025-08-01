"""
關卡選擇介面
"""

import pygame
import math
from constants import *
from systems.font_manager import get_font
from systems.save_system import save_system


class LevelSelectScreen:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font_large = get_font("large")
        self.font_medium = get_font("medium")
        self.font_small = get_font("small")

        # 關卡資訊
        self.level_info = {
            LEVEL_1: {
                "name": "第一關：訓練場",
                "description": "熟悉基本操作，擊敗訓練人偶",
                "difficulty": "初級",
                "color": (50, 150, 50),
            },
            LEVEL_2: {
                "name": "第二關：工廠",
                "description": "面對小型機器人的挑戰",
                "difficulty": "中級",
                "color": (150, 100, 50),
            },
            LEVEL_3: {
                "name": "第三關：實驗室",
                "description": "與巨型機器人BOSS決戰",
                "difficulty": "高級",
                "color": (150, 50, 50),
            },
        }

        self.selected_level = LEVEL_1
        self.unlocked_levels = save_system.get_unlocked_levels()
        self.completed_levels = save_system.get_completed_levels()

        # 動畫效果
        self.animation_time = 0
        self.hover_scale = 1.0
        self.target_hover_scale = 1.0

    def handle_event(self, event):
        """處理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._previous_level()
            elif event.key == pygame.K_RIGHT:
                self._next_level()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_level()
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(MENU_STATE)
            elif event.key == pygame.K_F1:
                # 重置存檔（隱藏功能）
                self._reset_save_data()

    def _previous_level(self):
        """選擇上一個關卡"""
        available_levels = sorted(self.unlocked_levels)
        current_index = (
            available_levels.index(self.selected_level)
            if self.selected_level in available_levels
            else 0
        )
        new_index = (current_index - 1) % len(available_levels)
        self.selected_level = available_levels[new_index]
        self.target_hover_scale = 1.2

    def _next_level(self):
        """選擇下一個關卡"""
        available_levels = sorted(self.unlocked_levels)
        current_index = (
            available_levels.index(self.selected_level)
            if self.selected_level in available_levels
            else 0
        )
        new_index = (current_index + 1) % len(available_levels)
        self.selected_level = available_levels[new_index]
        self.target_hover_scale = 1.2

    def _select_level(self):
        """選擇當前關卡"""
        if self.selected_level in self.unlocked_levels:
            self.state_manager.start_level(self.selected_level)

    def _reset_save_data(self):
        """重置存檔數據（隱藏功能）"""
        save_system.reset_save_data()
        self.unlocked_levels = save_system.get_unlocked_levels()
        self.completed_levels = save_system.get_completed_levels()
        self.selected_level = LEVEL_1

    def update(self):
        """更新邏輯"""
        self.animation_time += 1

        # 更新懸停動畫
        self.hover_scale += (self.target_hover_scale - self.hover_scale) * 0.1
        if abs(self.hover_scale - self.target_hover_scale) < 0.01:
            self.target_hover_scale = 1.0

    def draw(self, screen):
        """繪製關卡選擇介面"""
        # 繪製背景
        screen.fill(BLACK)

        # 繪製標題
        title = self.font_large.render("關卡選擇", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        screen.blit(title, title_rect)

        # 繪製關卡卡片
        self._draw_level_cards(screen)

        # 繪製選中關卡的詳細資訊
        self._draw_level_details(screen)

        # 繪製操作提示
        self._draw_instructions(screen)

    def _draw_level_cards(self, screen):
        """繪製關卡卡片"""
        card_width = 200
        card_height = 120
        card_spacing = 250
        start_x = WINDOW_WIDTH // 2 - (len(self.level_info) - 1) * card_spacing // 2
        card_y = 200

        for i, level_num in enumerate(sorted(self.level_info.keys())):
            level_data = self.level_info[level_num]
            is_unlocked = level_num in self.unlocked_levels
            is_completed = level_num in self.completed_levels
            is_selected = level_num == self.selected_level

            # 計算卡片位置
            card_x = start_x + i * card_spacing - card_width // 2

            # 繪製卡片陰影
            if is_selected:
                shadow_offset = 8
                shadow_rect = pygame.Rect(
                    card_x + shadow_offset,
                    card_y + shadow_offset,
                    card_width,
                    card_height,
                )
                pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=10)

            # 繪製卡片背景
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)

            if is_unlocked:
                # 已解鎖關卡
                card_color = level_data["color"]
                if is_selected:
                    # 選中時變亮
                    card_color = tuple(min(255, c + 50) for c in card_color)
            else:
                # 未解鎖關卡
                card_color = (80, 80, 80)

            pygame.draw.rect(screen, card_color, card_rect, border_radius=10)

            # 繪製邊框
            border_color = YELLOW if is_selected else WHITE
            border_width = 4 if is_selected else 2
            pygame.draw.rect(
                screen, border_color, card_rect, border_width, border_radius=10
            )

            # 繪製關卡編號
            level_text = self.font_large.render(str(level_num), True, WHITE)
            level_rect = level_text.get_rect(
                center=(card_x + card_width // 2, card_y + 40)
            )
            screen.blit(level_text, level_rect)

            # 繪製完成狀態
            if is_completed:
                # 繪製完成勾號
                check_color = GREEN
                check_size = 20
                check_x = card_x + card_width - 30
                check_y = card_y + 10
                pygame.draw.lines(
                    screen,
                    check_color,
                    False,
                    [
                        (check_x, check_y + check_size // 2),
                        (check_x + check_size // 3, check_y + check_size),
                        (check_x + check_size, check_y),
                    ],
                    4,
                )

            # 繪製鎖定狀態
            if not is_unlocked:
                # 繪製鎖定圖標
                lock_color = RED
                lock_size = 16
                lock_x = card_x + card_width // 2 - lock_size // 2
                lock_y = card_y + card_height - 35

                # 鎖身
                lock_body = pygame.Rect(lock_x, lock_y + 6, lock_size, lock_size - 6)
                pygame.draw.rect(screen, lock_color, lock_body)

                # 鎖環
                pygame.draw.arc(
                    screen,
                    lock_color,
                    (lock_x + 2, lock_y, lock_size - 4, lock_size // 2 + 4),
                    0,
                    math.pi,
                    3,
                )

            # 繪製最佳時間（已完成的關卡）
            if is_completed:
                best_time = save_system.get_best_time(level_num)
                if best_time:
                    time_text = f"{best_time:.1f}s"
                    time_surface = self.font_small.render(time_text, True, YELLOW)
                    time_rect = time_surface.get_rect(
                        center=(card_x + card_width // 2, card_y + card_height - 15)
                    )
                    screen.blit(time_surface, time_rect)

    def _draw_level_details(self, screen):
        """繪製選中關卡的詳細資訊"""
        if self.selected_level not in self.level_info:
            return

        level_data = self.level_info[self.selected_level]
        is_unlocked = self.selected_level in self.unlocked_levels
        is_completed = self.selected_level in self.completed_levels

        # 詳細資訊區域
        detail_y = 350

        # 關卡名稱
        name_color = WHITE if is_unlocked else GRAY
        name_text = self.font_medium.render(level_data["name"], True, name_color)
        name_rect = name_text.get_rect(center=(WINDOW_WIDTH // 2, detail_y))
        screen.blit(name_text, name_rect)

        # 關卡描述
        desc_text = self.font_small.render(level_data["description"], True, name_color)
        desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH // 2, detail_y + 40))
        screen.blit(desc_text, desc_rect)

        # 難度
        difficulty_text = f"難度：{level_data['difficulty']}"
        diff_color = {"初級": GREEN, "中級": YELLOW, "高級": RED}.get(
            level_data["difficulty"], WHITE
        )

        diff_surface = self.font_small.render(difficulty_text, True, diff_color)
        diff_rect = diff_surface.get_rect(center=(WINDOW_WIDTH // 2, detail_y + 80))
        screen.blit(diff_surface, diff_rect)

        # 狀態提示
        if not is_unlocked:
            lock_text = "需要完成前一關卡才能解鎖"
            lock_surface = self.font_small.render(lock_text, True, RED)
            lock_rect = lock_surface.get_rect(
                center=(WINDOW_WIDTH // 2, detail_y + 120)
            )
            screen.blit(lock_surface, lock_rect)
        elif is_completed:
            complete_text = "已完成"
            complete_surface = self.font_small.render(complete_text, True, GREEN)
            complete_rect = complete_surface.get_rect(
                center=(WINDOW_WIDTH // 2, detail_y + 120)
            )
            screen.blit(complete_surface, complete_rect)

    def _draw_instructions(self, screen):
        """繪製操作說明"""
        instructions = [
            "左右方向鍵：選擇關卡",
            "Enter/空白鍵：開始關卡",
            "ESC：返回主選單",
            "F1：重置存檔進度",
        ]

        start_y = WINDOW_HEIGHT - 140
        for i, instruction in enumerate(instructions):
            color = GRAY if i < 3 else (100, 100, 100)  # F1 指令顏色更暗
            text_surface = self.font_small.render(instruction, True, color)
            text_rect = text_surface.get_rect(
                center=(WINDOW_WIDTH // 2, start_y + i * 25)
            )
            screen.blit(text_surface, text_rect)
