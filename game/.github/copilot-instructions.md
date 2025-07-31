# 老鼠格鬥遊戲 - AI 開發指南

## 專案架構概覽

這是一個基於 Pygame 的 2D 橫向格鬥遊戲，使用**狀態模式**和**組合模式**實現清晰的架構分離：

```
main.py → GameStateManager → {MenuState, GameLevel, InstructionsState}
GameLevel → Player + Enemies + UI
Player → Fist (left/right) + input handling + physics
```

### 核心設計原則

- **狀態驅動**：遊戲流程完全由 `GameStateManager` 控制狀態切換
- **組合優於繼承**：Player 包含 Fist 物件而非繼承攻擊能力
- **常數驅動配置**：所有遊戲參數定義在 `constants.py`，支援快速調整

## 關鍵架構模式

### 1. 狀態管理模式

```python
# game_states.py - 中央狀態控制器
class GameStateManager:
    def change_state(self, new_state)  # 狀態切換
    def start_level(self, level_number)  # 動態創建關卡實例
```

**重要**：`GameLevel` 實例在關卡結束時會被銷毀，每次重新開始都創建新實例。

### 2. 拳頭攻擊系統（獨特設計）

```python
# player.py - 雙拳獨立控制
self.left_fist = Fist(self, "left")   # 左拳物件
self.right_fist = Fist(self, "right") # 右拳物件
```

拳頭具有獨立的攻擊狀態機：`待機 → 攻擊 → 返回 → 待機`，支援蓄力攻擊和方向性攻擊。

### 3. 繁體中文字體管理

```python
# font_manager.py - 全域字體管理
from font_manager import get_font
font = get_font('large')  # 自動使用最佳中文字體
```

字體管理器會自動檢測 Windows 系統字體，優先使用微軟正黑體。

## 開發工作流程

### 測試與除錯

```bash
# 組件測試（必須先執行）
python test_game.py

# 字體功能測試
python test_fonts.py

# 遊戲啟動
python run_game.py
```

### 新增關卡流程

1. 在 `constants.py` 定義新關卡常數
2. 在 `game_level.py` 的 `_setup_level()` 添加關卡配置
3. 在 `enemies.py` 創建新敵人類別（繼承 `Enemy` 基類）

### 新增敵人行為

```python
class NewEnemy(Enemy):
    def update(self, player):  # 必須實現
        super().update(player)  # 處理無敵/眩暈狀態
        # 自定義 AI 邏輯
```

## 專案特有慣例

### 1. 中英文混合命名

- 類別名稱：英文（`Player`, `Enemy`）
- 方法名稱：英文（`handle_input`, `take_damage`）
- 註解和文字：繁體中文
- 常數：英文大寫（`PLAYER_SPEED`）

### 2. 事件處理模式

所有 UI 狀態都實現三個方法：

```python
def handle_event(self, event)  # 處理輸入事件
def update(self)               # 更新邏輯狀態
def draw(self, screen)         # 繪製視覺內容
```

### 3. 碰撞檢測慣例

- 使用 `get_rect()` 方法獲取碰撞盒
- 拳頭攻擊檢測在 `game_level.py` 的 `_check_fist_collisions()`
- 玩家-敵人碰撞直接在敵人的 `update()` 方法中處理

### 4. 時間管理

- 使用 `pygame.time.get_ticks()` 獲取遊戲時間
- 所有計時器以毫秒為單位（如 `DEFENSE_DURATION = 1000`）
- 無敵時間、冷卻時間都基於時間差計算

## 調試技巧

### 常見問題排查

1. **拳頭不攻擊**：檢查 `Fist.start_attack()` 是否正確設定目標位置
2. **敵人無反應**：確認 `Enemy.update()` 中的 AI 邏輯和狀態檢查
3. **字體顯示問題**：運行 `test_fonts.py` 檢查字體路徑
4. **狀態切換卡住**：檢查 `GameStateManager` 中的狀態字典是否正確更新

### 效能監控

遊戲設計為 60 FPS，如果出現卡頓：

- 檢查 `_check_fist_collisions()` 中的碰撞檢測循環
- 確認敵人 AI 不會進行過多計算
- 使用 `clock.tick(FPS)` 確保幀率穩定

## 擴展指南

### 添加新功能的建議順序

1. 在 `constants.py` 定義相關常數
2. 在對應模組添加核心邏輯
3. 在 `test_game.py` 添加測試案例
4. 更新 UI 顯示（如果需要）

### 保持架構一致性

- 新的遊戲實體應繼承適當的基類（`Enemy` 等）
- 使用依賴注入模式傳遞 `state_manager` 引用
- 遵循現有的事件處理和狀態更新模式
