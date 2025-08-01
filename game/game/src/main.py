"""
主遊戲文件 - 2D 橫向格鬥遊戲
玩家操作老鼠角色完成三個關卡
"""

import pygame
import sys
import os

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from states.game_states import GameStateManager
from constants import *


class Game:
    def __init__(self):
        pygame.init()

        # 初始化音效系統
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("音效系統初始化成功")
        except pygame.error as e:
            print(f"音效系統初始化失敗: {e}")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("老鼠格鬥遊戲")
        self.clock = pygame.time.Clock()
        self.state_manager = GameStateManager()

        # 初始化音效管理器
        from systems.sound_manager import sound_manager

        self.sound_manager = sound_manager

    def run(self):
        """主遊戲迴圈"""
        running = True
        while running:
            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.state_manager.handle_event(event)

            # 更新遊戲邏輯
            self.state_manager.update()

            # 繪製畫面
            self.screen.fill(BLACK)
            self.state_manager.draw(self.screen)

            # 更新顯示
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
