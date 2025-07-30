"""
測試安全平台生成的腳本
"""

from config.settings import *
from levels.level_generator import LevelGenerator


def test_safe_platforms():
    """測試安全平台的生成"""
    print("=== 測試安全平台生成 ===")

    # 生成完整塔樓
    platforms, enemies, cheeses = LevelGenerator.generate_complete_tower()

    print(f"總平台數量: {len(platforms)}")
    print(f"總敵人數量: {len(enemies)}")
    print(f"總起司數量: {len(cheeses)}")

    # 統計綠色（安全）平台
    safe_platforms = [p for p in platforms if p.color == GREEN]
    print(f"安全平台數量: {len(safe_platforms)}")

    # 顯示各區域的安全平台
    for i in range(1, TOTAL_SECTIONS):  # 從區域1開始，因為區域0沒有安全過渡平台
        section_y = i * SECTION_HEIGHT
        section_safe_platforms = [
            p for p in safe_platforms if section_y - 100 <= p.rect.y <= section_y + 100
        ]
        print(f"區域 {i} 的安全平台數量: {len(section_safe_platforms)}")
        for platform in section_safe_platforms:
            print(
                f"  - 位置: ({platform.rect.x}, {platform.rect.y}), 大小: {platform.rect.width}x{platform.rect.height}"
            )

    # 檢查安全平台上的起司
    safe_platform_cheeses = []
    for cheese in cheeses:
        cheese_y = cheese.y
        for platform in safe_platforms:
            if (
                platform.rect.x <= cheese.x <= platform.rect.x + platform.rect.width
                and platform.rect.y - 100 <= cheese_y <= platform.rect.y
            ):
                safe_platform_cheeses.append(cheese)
                break

    print(f"安全平台上的起司數量: {len(safe_platform_cheeses)}")

    print("\n=== 測試完成 ===")


if __name__ == "__main__":
    test_safe_platforms()
