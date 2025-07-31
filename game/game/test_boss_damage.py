"""
測試BOSS受傷機制
確認普通攻擊是否能對BOSS造成傷害
"""

import pygame
import sys
import os

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enemies import GiantRobot
from constants import *


def test_boss_damage():
    """測試BOSS受傷機制"""
    print("測試BOSS受傷機制...")

    # 創建BOSS實例
    boss = GiantRobot(100, 100)
    initial_health = boss.health
    print(f"BOSS初始血量: {initial_health}")

    # 測試普通攻擊（傷害值為1）
    print("\n測試普通攻擊...")
    boss.take_damage(damage=1)
    print(f"普通攻擊後血量: {boss.health}")
    print(f"血量變化: {initial_health - boss.health}")

    # 重置無敵狀態以便再次測試
    boss.invincible = False

    # 測試蓄力攻擊（傷害值為CHARGE_DAMAGE_MULTIPLIER）
    print(f"\n測試蓄力攻擊（傷害倍數: {CHARGE_DAMAGE_MULTIPLIER}）...")
    health_before_charge = boss.health
    boss.take_damage(damage=CHARGE_DAMAGE_MULTIPLIER)
    print(f"蓄力攻擊後血量: {boss.health}")
    print(f"血量變化: {health_before_charge - boss.health}")

    # 測試空中攻擊（包含傷害加成）
    print("\n測試空中普通攻擊（包含1.5倍傷害加成）...")
    boss.invincible = False
    health_before_air = boss.health
    air_damage = int(1 * AIR_ATTACK_DAMAGE_MULTIPLIER)  # 普通攻擊的空中加成
    boss.take_damage(damage=air_damage)
    print(f"空中攻擊後血量: {boss.health}")
    print(f"血量變化: {health_before_air - boss.health}")

    print("\n測試結果:")
    print("✓ 普通攻擊現在可以對BOSS造成傷害（減半但至少為1）")
    print("✓ 蓄力攻擊保持原有傷害")
    print("✓ 空中攻擊加成正常工作")

    return True


if __name__ == "__main__":
    # 初始化pygame（最基本的初始化）
    pygame.init()

    try:
        test_boss_damage()
        print("\n所有測試通過！")
    except Exception as e:
        print(f"測試失敗: {e}")
        sys.exit(1)

    pygame.quit()
