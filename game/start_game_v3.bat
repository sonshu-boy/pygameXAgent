@echo off
echo 正在啟動老鼠格鬥遊戲 v1.3...
echo.
echo 新功能：
echo - 蓄力攻擊增強（更快更遠）
echo - 二段跳系統
echo - 滑行特殊攻擊
echo - 空中攻擊加成
echo - BOSS 遠程攻擊
echo.
echo 操作提示：
echo - 長按滑鼠蓄力攻擊
echo - 空中按 W 進行二段跳
echo - Shift + 移動進行滑行攻擊
echo - 空白鍵防禦 BOSS 子彈
echo.
pause
cd game
python run_game.py
pause
