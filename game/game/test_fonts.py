"""
字體測試腳本
"""

import pygame
from font_manager import get_font_manager, get_font, render_text


def test_fonts():
    """測試字體功能"""
    print("測試字體管理器...")

    # 初始化 pygame
    pygame.init()

    try:
        # 測試字體管理器初始化
        font_manager = get_font_manager()
        print("✓ 字體管理器初始化成功")

        # 測試不同大小的字體
        sizes = ["large", "medium", "small", "tiny"]
        for size in sizes:
            font = get_font(size)
            print(f"✓ {size} 字體獲取成功")

        # 測試文字渲染
        test_texts = [
            "老鼠格鬥遊戲",
            "開始遊戲",
            "遊戲說明",
            "第一關：訓練場",
            "攻擊系統測試",
            "繁體中文顯示測試",
        ]

        for text in test_texts:
            rendered = render_text(text, "medium", (255, 255, 255))
            print(f"✓ 文字渲染成功: {text}")

        print("\n🎉 所有字體測試通過！")
        return True

    except Exception as e:
        print(f"❌ 字體測試失敗: {e}")
        return False
    finally:
        pygame.quit()


if __name__ == "__main__":
    test_fonts()
