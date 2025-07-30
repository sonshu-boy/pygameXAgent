"""
起司小子的塔樓冒險 - 主程式入口
Tower Adventure Game - Main Entry Point

這是一個2D平台跳躍遊戲，玩家控制一隻可愛的老鼠從高塔上往下爬，
收集起司並避開敵人，最終安全到達地面。

操作說明：
- A/D 鍵：左右移動
- 空白鍵：跳躍（支援多段跳）
- S 鍵：滑行
- 滑鼠左鍵：攻擊
- 滑鼠右鍵：防禦
- Shift 鍵：跑步
"""

import pygame
import sys
from config.settings import *
from src.game import Game


def main():
    """主程式函數"""
    # 初始化pygame
    pygame.init()

    # 創建遊戲視窗
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # 創建時鐘物件
    clock = pygame.time.Clock()

    # 創建遊戲實例
    game = Game()

    # 輸入狀態追蹤
    keys_pressed = set()
    mouse_pressed = set()
    attack_charge_time = 0

    # 主遊戲迴圈
    while True:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                keys_pressed.add(event.key)

                # 跳躍處理 - 在事件處理中避免重複跳躍
                if event.key == pygame.K_SPACE and game.game_state == "playing":
                    game.player.jump()

                # 滑行處理 - 在事件處理中避免重複滑行
                if event.key == pygame.K_s and game.game_state == "playing":
                    game.player.slide()

                # 重新開始遊戲
                if event.key == pygame.K_r and game.game_state in [
                    "game_over",
                    "victory",
                ]:
                    game.reset_game()

                # 升級選單選擇
                if game.game_state == "upgrade":
                    if event.key == pygame.K_1 and len(game.upgrade_options) > 0:
                        game.apply_upgrade(game.upgrade_options[0]["type"])
                    elif event.key == pygame.K_2 and len(game.upgrade_options) > 1:
                        game.apply_upgrade(game.upgrade_options[1]["type"])
                    elif event.key == pygame.K_3 and len(game.upgrade_options) > 2:
                        game.apply_upgrade(game.upgrade_options[2]["type"])

            elif event.type == pygame.KEYUP:
                keys_pressed.discard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed.add(event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and 1 in mouse_pressed:  # 左鍵釋放
                    if game.game_state == "playing":
                        game.player.attack(game.enemies, attack_charge_time)
                    attack_charge_time = 0
                mouse_pressed.discard(event.button)

        # 處理遊戲中的持續輸入
        if game.game_state == "playing":
            # 處理持續按鍵
            running = pygame.K_LSHIFT in keys_pressed or pygame.K_RSHIFT in keys_pressed

            # 左右移動
            if pygame.K_a in keys_pressed:
                game.player.move_left(running)
            elif pygame.K_d in keys_pressed:
                game.player.move_right(running)
            else:
                game.player.stop_moving()

            # 變長跳躍 - 按住空白鍵持續施加上升力
            if pygame.K_SPACE in keys_pressed:
                game.player.continue_jump()

            # 防禦
            game.player.is_defending = 3 in mouse_pressed  # 右鍵

            # 蓄力攻擊
            if 1 in mouse_pressed:  # 左鍵按住
                attack_charge_time += 1
                if attack_charge_time > game.player.max_attack_charge:
                    attack_charge_time = game.player.max_attack_charge

        # 更新遊戲狀態
        game.update()

        # 繪製遊戲
        game.draw(screen)

        # 繪製蓄力攻擊指示器
        if attack_charge_time > 0 and game.game_state == "playing":
            game.ui.draw_charge_indicator(
                screen, attack_charge_time, game.player.max_attack_charge
            )

        # 更新顯示
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
