#!/usr/bin/env python3
"""
測試小型敵人邊界處理的腳本
"""

import pygame
import sys
from constants import *
from enemies import SmallRobot
from player import Player


def test_enemy_boundary():
    """測試小型敵人的邊界處理"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("敵人邊界測試")
        clock = pygame.time.Clock()

        # 創建玩家和敵人
        player = Player(WINDOW_WIDTH // 2, GROUND_Y - PLAYER_HEIGHT)
        enemy = SmallRobot(50, GROUND_Y - SMALL_ROBOT_HEIGHT)

        # 設定敵人初始狀態
        enemy.charging = True
        enemy.direction = -1  # 向左衝刺
        enemy.charge_speed = SMALL_ROBOT_CHARGE_SPEED

        print("=== 小型敵人邊界測試 ===")
        print(f"初始位置: x={enemy.x}")
        print(f"衝刺方向: {enemy.direction}")
        print(f"螢幕寬度: {WINDOW_WIDTH}")
        print("開始測試...按ESC退出")

        running = True
        frame_count = 0

        while running and frame_count < 600:  # 10秒測試
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("用戶關閉視窗")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        print("用戶按下ESC鍵")

            # 更新敵人
            old_x = enemy.x
            old_charging = enemy.charging
            old_direction = enemy.direction

            try:
                enemy.update(player)
            except Exception as e:
                print(f"敵人更新時發生錯誤: {e}")
                break

            # 檢查狀態變化
            if old_charging != enemy.charging:
                print(
                    f"幀 {frame_count}: 衝刺狀態改變 {old_charging} -> {enemy.charging}"
                )
                print(f"  位置: {old_x} -> {enemy.x}")
                print(f"  方向: {old_direction} -> {enemy.direction}")

            # 檢查邊界
            if enemy.x < 0:
                print(f"警告：敵人超出左邊界! x={enemy.x}")
            if enemy.x > WINDOW_WIDTH - enemy.width:
                print(
                    f"警告：敵人超出右邊界! x={enemy.x}, 最大值={WINDOW_WIDTH - enemy.width}"
                )

            # 每30幀記錄一次狀態
            if frame_count % 30 == 0:
                print(
                    f"幀 {frame_count}: x={enemy.x:.1f}, 衝刺={enemy.charging}, 方向={enemy.direction}"
                )

            # 繪製
            screen.fill(BLACK)

            # 繪製地面
            pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WINDOW_WIDTH, GROUND_Y), 2)

            # 繪製邊界線
            pygame.draw.line(screen, RED, (0, 0), (0, WINDOW_HEIGHT), 3)  # 左邊界
            pygame.draw.line(
                screen, RED, (WINDOW_WIDTH - 3, 0), (WINDOW_WIDTH - 3, WINDOW_HEIGHT), 3
            )  # 右邊界

            # 繪製實體
            try:
                player.draw(screen)
                enemy.draw(screen)
            except Exception as e:
                print(f"繪製時發生錯誤: {e}")
                break

            # 顯示資訊
            try:
                font = pygame.font.Font(None, 36)
                info_text = f"位置: {enemy.x:.1f}, 衝刺: {enemy.charging}, 方向: {enemy.direction}"
                text_surface = font.render(info_text, True, WHITE)
                screen.blit(text_surface, (10, 10))
            except Exception as e:
                print(f"字體渲染錯誤: {e}")

            pygame.display.flip()
            clock.tick(FPS)
            frame_count += 1

    except Exception as e:
        print(f"測試過程中發生錯誤: {e}")
    finally:
        pygame.quit()
        print("測試完成!")


if __name__ == "__main__":
    test_enemy_boundary()
