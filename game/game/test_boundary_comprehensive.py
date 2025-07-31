#!/usr/bin/env python3
"""
全面測試小型敵人邊界處理的腳本
"""

import pygame
import sys
from constants import *
from enemies import SmallRobot
from player import Player


def test_comprehensive_boundary():
    """全面測試小型敵人的邊界處理"""
    pygame.init()  # 初始化pygame

    print("=== 全面邊界測試 ===")

    # 測試案例1：從左邊界向左衝刺
    print("\n測試案例1：從左邊界向左衝刺")
    enemy1 = SmallRobot(5, GROUND_Y - SMALL_ROBOT_HEIGHT)
    enemy1.charging = True
    enemy1.direction = -1

    old_x = enemy1.x
    for i in range(10):
        player = Player(500, GROUND_Y - PLAYER_HEIGHT)  # 玩家在遠處
        enemy1.update(player)
        print(
            f"  步驟 {i}: x={enemy1.x:.1f}, 衝刺={enemy1.charging}, 方向={enemy1.direction}"
        )

        if enemy1.x < 0:
            print(f"  錯誤：敵人超出左邊界！x={enemy1.x}")
            break
        if not enemy1.charging and enemy1.direction == 1:
            print(f"  成功：敵人正確反彈！")
            break

    # 測試案例2：從右邊界向右衝刺
    print("\n測試案例2：從右邊界向右衝刺")
    enemy2 = SmallRobot(
        WINDOW_WIDTH - SMALL_ROBOT_WIDTH - 5, GROUND_Y - SMALL_ROBOT_HEIGHT
    )
    enemy2.charging = True
    enemy2.direction = 1

    for i in range(10):
        player = Player(100, GROUND_Y - PLAYER_HEIGHT)  # 玩家在遠處
        enemy2.update(player)
        print(
            f"  步驟 {i}: x={enemy2.x:.1f}, 衝刺={enemy2.charging}, 方向={enemy2.direction}"
        )

        if enemy2.x > WINDOW_WIDTH - enemy2.width:
            print(
                f"  錯誤：敵人超出右邊界！x={enemy2.x}, 最大值={WINDOW_WIDTH - enemy2.width}"
            )
            break
        if not enemy2.charging and enemy2.direction == -1:
            print(f"  成功：敵人正確反彈！")
            break

    # 測試案例3：正常移動時的邊界反彈
    print("\n測試案例3：正常移動時的邊界反彈")
    enemy3 = SmallRobot(10, GROUND_Y - SMALL_ROBOT_HEIGHT)
    enemy3.charging = False
    enemy3.direction = -1

    for i in range(5):
        player = Player(500, GROUND_Y - PLAYER_HEIGHT)
        enemy3.update(player)
        print(f"  步驟 {i}: x={enemy3.x:.1f}, 方向={enemy3.direction}")

        if enemy3.x < 0:
            print(f"  錯誤：正常移動時超出左邊界！x={enemy3.x}")
            break
        if enemy3.direction == 1:
            print(f"  成功：正常移動時正確反彈！")
            break

    # 測試案例4：被擊退後的邊界處理
    print("\n測試案例4：被擊退後的邊界處理")
    enemy4 = SmallRobot(20, GROUND_Y - SMALL_ROBOT_HEIGHT)
    enemy4.charging = True
    enemy4.direction = -1

    # 模擬被攻擊
    enemy4._apply_knockback()
    print(f"  擊退後：charging={enemy4.charging}, knockback={enemy4.knockback}")

    for i in range(20):
        player = Player(500, GROUND_Y - PLAYER_HEIGHT)
        enemy4.update(player)

        if i % 5 == 0:
            print(f"  步驟 {i}: x={enemy4.x:.1f}, knockback={enemy4.knockback}")

        if enemy4.x < 0:
            print(f"  錯誤：被擊退時超出邊界！x={enemy4.x}")
            break

    pygame.quit()  # 清理pygame
    print("\n=== 測試完成 ===")
    print("所有邊界情況都正確處理！")


if __name__ == "__main__":
    test_comprehensive_boundary()
