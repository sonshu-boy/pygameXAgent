"""
遊戲說明畫面
"""

import pygame
from constants import *
from systems.font_manager import get_font


class InstructionsScreen:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font_large = get_font("large")
        self.font_medium = get_font("small")

        # 遊戲說明文字
        self.instructions = [
            "遊戲操作說明",
            "",
            "移動：方向鍵或 WASD",
            "跳躍：W 鍵或上方向鍵",
            "左移：A 鍵或左方向鍵",
            "右移：D 鍵或右方向鍵",
            "下平台：S 鍵或下方向鍵（在平台上時）",
            "",
            "攻擊：左鍵（左拳）/ 右鍵（右拳）",
            "蓄力攻擊：長按攻擊鍵可增加傷害和距離",
            "",
            "防禦：空白鍵（短暫無敵，有冷卻時間）",
            "",
            "閃避：",
            "蹲下：靜止時按 Shift",
            "滑行：移動時按 Shift",
            "",
            "互動：E 鍵",
            "",
            "遊戲目標：",
            "控制老鼠角色完成三個關卡",
            "第一關：訓練場（對抗訓練人偶）",
            "第二關：工廠（對抗小型機器人）",
            "第三關：實驗室（對抗巨型機器人 BOSS）",
            "",
            "注意：玩家只有三顆愛心，要小心保護！",
        ]

    def handle_event(self, event):
        """處理說明畫面事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.state_manager.change_state(MENU_STATE)

    def update(self):
        """更新說明畫面邏輯"""
        pass

    def draw(self, screen):
        """繪製說明畫面"""
        y_offset = 50

        for i, line in enumerate(self.instructions):
            if i == 0:  # 標題
                text = self.font_large.render(line, True, YELLOW)
            elif line == "":  # 空行
                y_offset += 10
                continue
            else:
                text = self.font_medium.render(line, True, WHITE)

            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30

        # 繪製返回提示
        back_text = self.font_medium.render("按 ESC 或 Enter 返回主選單", True, GRAY)
        back_rect = back_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        screen.blit(back_text, back_rect)
