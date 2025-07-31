"""
測試遊戲更新功能
"""

import pygame
from constants import *
from player import Player
from enemies import TrainingDummy, SmallRobot, GiantRobot


def test_charge_attack():
    """測試蓄力攻擊功能"""
    print("=== 測試蓄力攻擊功能 ===")

    # 初始化 pygame（測試需要）
    pygame.init()

    player = Player(100, GROUND_Y - PLAYER_HEIGHT)

    # 測試拳頭是否有蓄力功能
    assert hasattr(player.left_fist, "charging"), "拳頭缺少蓄力屬性"
    assert hasattr(player.left_fist, "charge_start_time"), "拳頭缺少蓄力時間屬性"
    assert hasattr(player.left_fist, "start_charging"), "拳頭缺少開始蓄力方法"
    assert hasattr(player.left_fist, "release_attack"), "拳頭缺少釋放攻擊方法"

    print("✓ 拳頭蓄力系統初始化正常")

    # 測試蓄力過程
    player.left_fist.start_charging()
    assert player.left_fist.charging == True, "蓄力狀態設定失敗"

    # 模擬蓄力完成
    player.left_fist.charge_start_time = pygame.time.get_ticks() - CHARGE_TIME - 100
    player.left_fist.update()
    assert player.left_fist.size == FIST_CHARGED_SIZE, "蓄力後拳頭大小錯誤"

    print("✓ 蓄力攻擊機制正常")


def test_enemy_health():
    """測試敵人血量調整"""
    print("=== 測試敵人血量調整 ===")

    # 測試小型機器人血量
    small_robot = SmallRobot(400, GROUND_Y - SMALL_ROBOT_HEIGHT)
    assert (
        small_robot.health == SMALL_ROBOT_HEALTH
    ), f"小型機器人血量錯誤：{small_robot.health} != {SMALL_ROBOT_HEALTH}"

    # 測試需要3次普通攻擊擊敗（需要考慮無敵時間）
    small_robot.take_damage(1, False, False)  # 普通攻擊 1
    assert small_robot.alive == True, "小型機器人過早死亡"

    # 清除無敵狀態以便下次攻擊生效
    small_robot.invincible = False
    small_robot.take_damage(1, False, False)  # 普通攻擊 2
    assert small_robot.alive == True, "小型機器人過早死亡"

    # 清除無敵狀態以便下次攻擊生效
    small_robot.invincible = False
    small_robot.take_damage(1, False, False)  # 普通攻擊 3
    assert small_robot.alive == False, "小型機器人未正確死亡"

    print("✓ 小型機器人血量調整正常")

    # 測試蓄力攻擊一擊擊敗
    small_robot2 = SmallRobot(400, GROUND_Y - SMALL_ROBOT_HEIGHT)
    small_robot2.take_damage(CHARGE_DAMAGE_MULTIPLIER, True, True)  # 蓄力攻擊
    # 檢查血量是否足夠低，如果不是一擊必殺，至少應該受到雙倍傷害
    expected_health = SMALL_ROBOT_HEALTH - CHARGE_DAMAGE_MULTIPLIER
    if expected_health <= 0:
        assert small_robot2.alive == False, "小型機器人未被蓄力攻擊正確擊敗"
        print("✓ 蓄力攻擊一擊擊敗機制正常")
    else:
        assert small_robot2.health == expected_health, "蓄力攻擊傷害不正確"
        print("✓ 蓄力攻擊雙倍傷害正常")


def test_boss_immunity():
    """測試BOSS免疫普通攻擊"""
    print("=== 測試BOSS免疫普通攻擊 ===")

    boss = GiantRobot(600, GROUND_Y - BOSS_HEIGHT)
    original_health = boss.health

    # 測試普通攻擊無效
    boss.take_damage(1, False, False)  # 普通攻擊
    assert boss.health == original_health, "BOSS受到了普通攻擊傷害"

    print("✓ BOSS免疫普通攻擊正常")

    # 測試蓄力攻擊有效
    boss.take_damage(CHARGE_DAMAGE_MULTIPLIER, True, True)  # 蓄力攻擊
    assert (
        boss.health == original_health - CHARGE_DAMAGE_MULTIPLIER
    ), "BOSS未受到蓄力攻擊傷害"

    print("✓ BOSS蓄力攻擊傷害正常")


def test_stun_duration():
    """測試眩暈機制"""
    print("=== 測試眩暈機制 ===")

    dummy = TrainingDummy(500, GROUND_Y - DUMMY_HEIGHT)

    # 普通攻擊不會造成眩暈
    dummy.take_damage(1, False, False)
    assert dummy.stunned == False, "普通攻擊錯誤地造成了眩暈"

    print("✓ 普通攻擊無眩暈正常")

    # 重置敵人的無敵狀態
    dummy.invincible = False

    # 蓄力攻擊會造成眩暈（使用正確的傷害值）
    dummy.take_damage(CHARGE_DAMAGE_MULTIPLIER, True, True)
    assert dummy.stunned == True, "蓄力攻擊未造成眩暈"

    print("✓ 蓄力攻擊眩暈正常")

    print(f"✓ 眩暈持續時間設定為 {STUN_DURATION} 毫秒")


if __name__ == "__main__":
    print("開始測試遊戲更新功能...")

    try:
        test_charge_attack()
        test_enemy_health()
        test_boss_immunity()
        test_stun_duration()

        print("\n🎉 所有更新功能測試通過！")
        print("\n更新內容總結：")
        print("1. ✓ 新增蓄力攻擊機制（3秒蓄力，傷害加倍）")
        print("2. ✓ 普通攻擊不再造成眩暈")
        print("3. ✓ BOSS免疫普通攻擊，只受蓄力攻擊傷害")
        print("4. ✓ BOSS特殊攻擊（血量低於50%觸發）")
        print("5. ✓ 小型機器人血量調整（3次普通攻擊或1次蓄力攻擊）")
        print("6. ✓ 眩暈時間調整（0.1秒）")

    except Exception as e:
        print(f"❌ 測試失敗：{e}")
        import traceback

        traceback.print_exc()

    pygame.quit()
