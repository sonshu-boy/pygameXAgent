"""
啟動腳本
"""

from main import Game

if __name__ == "__main__":
    print("正在啟動老鼠格鬥遊戲...")
    print("遊戲操作說明：")
    print("- WASD/方向鍵：移動和跳躍")
    print("- 左鍵/右鍵：攻擊（長按蓄力）")
    print("- 空白鍵：防禦")
    print("- Shift：蹲下/滑行")
    print("- ESC：返回選單")
    print("- E：互動")
    print()

    try:
        # 啟動遊戲（pygame 會在 Game 類中初始化）
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("遊戲已結束")
    except Exception as e:
        print(f"遊戲發生錯誤：{e}")
        import traceback

        traceback.print_exc()
