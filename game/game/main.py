"""
主遊戲文件 - 2D 橫向格鬥遊戲
玩家操作老鼠角色完成三個關卡
"""

import pygame
import sys
from game_states import GameStateManager
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("老鼠格鬥遊戲")
        self.clock = pygame.time.Clock()
        self.state_manager = GameStateManager()

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
