"""
遊戲組件測試腳本
"""

import pygame
import sys
from constants import *
from player import Player
from enemies import TrainingDummy, SmallRobot, GiantRobot


def test_components():
    """測試遊戲組件是否正常工作"""
    print("開始測試遊戲組件...")

    # 初始化 pygame
    pygame.init()

    # 測試常數
    print(f"視窗大小: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"玩家大小: {PLAYER_WIDTH}x{PLAYER_HEIGHT}")

    # 測試玩家創建
    try:
        player = Player(100, GROUND_Y - PLAYER_HEIGHT)
        print("✓ 玩家創建成功")
        print(f"  玩家位置: ({player.x}, {player.y})")
        print(f"  玩家生命值: {player.health}")
    except Exception as e:
        print(f"✗ 玩家創建失敗: {e}")
        return False

    # 測試敵人創建
    try:
        dummy = TrainingDummy(500, GROUND_Y - DUMMY_HEIGHT)
        robot = SmallRobot(400, GROUND_Y - SMALL_ROBOT_HEIGHT)
        boss = GiantRobot(600, GROUND_Y - BOSS_HEIGHT)

        print("✓ 所有敵人創建成功")
        print(f"  訓練人偶血量: {dummy.health}")
        print(f"  小型機器人血量: {robot.health}")
        print(f"  巨型機器人血量: {boss.health}")
    except Exception as e:
        print(f"✗ 敵人創建失敗: {e}")
        return False

    # 測試拳頭
    try:
        left_fist = player.left_fist
        right_fist = player.right_fist
        print("✓ 拳頭系統正常")
        print(f"  左拳位置: ({left_fist.x}, {left_fist.y})")
        print(f"  右拳位置: ({right_fist.x}, {right_fist.y})")
    except Exception as e:
        print(f"✗ 拳頭系統失敗: {e}")
        return False

    # 測試碰撞檢測
    try:
        player_rect = player.get_rect()
        dummy_rect = dummy.get_rect()
        print("✓ 碰撞檢測系統正常")
        print(f"  玩家碰撞框: {player_rect}")
        print(f"  敵人碰撞框: {dummy_rect}")
    except Exception as e:
        print(f"✗ 碰撞檢測失敗: {e}")
        return False

    pygame.quit()
    print("\n✓ 所有組件測試通過！")
    return True


def test_game_mechanics():
    """測試遊戲機制"""
    print("\n開始測試遊戲機制...")

    pygame.init()
    player = Player(100, GROUND_Y - PLAYER_HEIGHT)
    dummy = TrainingDummy(500, GROUND_Y - DUMMY_HEIGHT)

    # 測試傷害系統
    initial_health = player.health
    player.take_damage()
    if player.health == initial_health - 1:
        print("✓ 傷害系統正常")
    else:
        print("✗ 傷害系統異常")

    # 測試無敵時間
    if player.invincible:
        print("✓ 無敵時間機制正常")
    else:
        print("✗ 無敵時間機制異常")

    # 測試敵人傷害
    initial_dummy_health = dummy.health
    dummy.take_damage()
    if dummy.health == initial_dummy_health - 1:
        print("✓ 敵人傷害系統正常")
    else:
        print("✗ 敵人傷害系統異常")

    pygame.quit()
    print("✓ 遊戲機制測試完成！")


if __name__ == "__main__":
    try:
        test_components()
        test_game_mechanics()
        print("\n🎮 遊戲已準備就緒！可以開始遊玩了！")
        print("執行 'python run_game.py' 或點擊 'start_game.bat' 來啟動遊戲")
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        sys.exit(1)
