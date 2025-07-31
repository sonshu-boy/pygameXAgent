````instructions
# 老鼠格鬥遊戲 - AI 開發指南

## 專案架構概覽

這是一個基於 Pygame 的 2D 橫向格鬥遊戲，使用**狀態模式**和**組合模式**實現清晰的架構分離：

```
main.py → GameStateManager → {MenuState, GameLevel, InstructionsState}
GameLevel → Player + Enemies + PlatformSystem + UI + effects/sound systems
Player → Fist (left/right) + charge system + input handling + physics + platform collision
```

### 核心設計原則

- **狀態驅動**：遊戲流程完全由 `GameStateManager` 控制狀態切換
- **組合優於繼承**：Player 包含 Fist 物件而非繼承攻擊能力
- **常數驅動配置**：所有遊戲參數定義在 `constants.py`，支援快速調整
- **平台系統集成**：統一的 `PlatformSystem` 處理所有實體的平台碰撞
- **模組化擴展**：預留 `combo_system.py`、`effects.py`、`sound_manager.py` 等空模組用於未來功能

## 關鍵架構模式

### 1. 狀態管理模式

```python
# game_states.py - 中央狀態控制器
class GameStateManager:
    def change_state(self, new_state)  # 狀態切換
    def start_level(self, level_number)  # 動態創建關卡實例
```

**重要**：`GameLevel` 實例在關卡結束時會被銷毀，每次重新開始都創建新實例。

### 2. 輸入處理架構（v1.3 關鍵問題）

```python
# player.py - 混合輸入模式
def handle_input(self):          # 連續狀態檢查（移動、攻擊）
def handle_event(self, event):   # 單次按鍵事件（跳躍、防禦）
```

**重要設計決策**：
- **移動**使用 `pygame.key.get_pressed()` 實現流暢連續移動
- **跳躍**應使用 `pygame.KEYDOWN` 事件防止連續觸發
- **攻擊**使用連續檢查實現按住蓄力機制

### 3. 平台系統（v1.2 新增核心功能）

```python
# platform_system.py - 統一平台碰撞管理
class PlatformSystem:
    def check_collision(self, entity_rect, vel_y)  # 平台碰撞檢測
    def is_on_platform(self, entity_rect)          # 平台站立檢測
    def get_nearest_platform_above(self, x, y)     # AI跳躍目標選擇
```

**關鍵機制**：
- 只能從上方落到平台上（vel_y >= 0 且實體底部接觸平台頂部）
- 所有實體（玩家+敵人）都通過同一個 `PlatformSystem` 實例處理碰撞
- 敵人 AI 會利用 `get_nearest_platform_above()` 智能跳躍追擊玩家

### 4. 二段跳系統（v1.3 核心功能）

```python
# player.py - 二段跳狀態機
self.double_jump_available = True  # 地面重置為True
# 首次跳躍：設定double_jump_available = True（錯誤！）
# 二段跳：設定double_jump_available = False
```

**已知問題**：
- 目前使用連續按鍵檢查導致無法正確觸發二段跳
- 首次跳躍錯誤地重設 `double_jump_available = True`
- 需要改為事件驅動的跳躍處理

### 5. 蓄力攻擊系統（核心戰鬥機制）

```python
# player.py - 雙拳獨立控制 + 蓄力系統
self.left_fist = Fist(self, "left")   # 左拳物件
self.right_fist = Fist(self, "right") # 右拳物件

# 蓄力攻擊狀態機：
# 待機 → 開始蓄力(start_charging) → 蓄力中(charging=True) → 釋放攻擊(release_attack) → 待機
```

**重要蓄力機制**：
- 按住攻擊鍵觸發 `start_charging()`，釋放鍵觸發 `release_attack()`
- 蓄力 1 秒完成，造成 2 倍傷害 + 眩暈 + 擊退
- 視覺反饋：拳頭變大 + 顏色變化（黃 → 紅 → 閃白光）
- BOSS 戰必須機制：BOSS 免疫普通攻擊，只受蓄力攻擊傷害

### 6. 滑行攻擊系統（v1.3 特殊機制）

```python
# player.py - 滑行特殊攻擊
def check_slide_attack(self, enemies):
    # 當前實作：enemy.vel_y = -15（太強力）
    # 問題：敵人飛太高且難以回到地面
```

**已知問題**：
- 滑行攻擊的向上擊飛力度（`vel_y = -15`）太強
- 敵人被擊飛後不容易回到地面繼續戰鬥
- 需要調整為較小的向上速度（建議 `-8` 到 `-10`）

### 7. 敵人 AI 跳躍系統（v1.2 新增）

```python
# enemies.py - 智能跳躍追擊
class SmallRobot(Enemy):
    def _try_jump_to_player(self, player):  # 檢測並跳躍至玩家平台
```

**AI 跳躍邏輯**：
- 檢測玩家是否在上方平台（利用 `platform_system.get_nearest_platform_above()`）
- 有跳躍冷卻時間防止過度跳躍（小機器人 3 秒，BOSS 4 秒）
- 空中移動：跳躍時可調整水平方向追擊玩家

### 8. 擊退系統（v1.2 修正）

```python
# enemies.py - 通用擊退機制
def apply_knockback(self, source_x):
    # 計算擊退方向（遠離攻擊源或螢幕中心）
    # 設置擊退速度和持續時間
```

**擊退機制**：
- 所有敵人現在都支援擊退（之前版本的已知問題已修正）
- 擊退方向：遠離攻擊源或螢幕中心
- 差異化擊退：BOSS 擊退距離減半但仍會被擊退

### 9. 繁體中文字體管理

```python
# font_manager.py - 全域字體管理
from font_manager import get_font
font = get_font('large')  # 自動使用最佳中文字體
```

字體管理器會自動檢測 Windows 系統字體，優先使用微軟正黑體。

## 開發工作流程

### 測試與除錯

```bash
# v1.3 功能測試（含二段跳、滑行攻擊）
python test_update_v3.py

# 組件測試
python test_game.py

# 新功能測試（v1.2 平台系統與敵人跳躍）
python test_update_features.py

# 遊戲啟動
python run_game.py
```

### 新增關卡流程

1. 在 `constants.py` 定義新關卡常數
2. 在 `game_level.py` 的 `_setup_level()` 添加關卡配置
3. 在 `enemies.py` 創建新敵人類別（繼承 `Enemy` 基類）
4. **v1.2 新增**：配置關卡平台佈局（呼叫 `platform_system.add_platform()`）

### 新增敵人行為

```python
class NewEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.platform_system = None  # 將由GameLevel設定
        self.jump_speed = 12         # 跳躍能力
        self.jump_cooldown = 3000    # 跳躍冷卻時間
        self.last_jump_time = 0

    def update(self, player):  # 必須實現
        super().update(player)  # 處理無敵/眩暈/擊退狀態
        # 自定義 AI 邏輯
        self._try_jump_to_player(player)  # 智能跳躍
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
- **v1.2 新增**：平台碰撞統一在 `PlatformSystem.check_collision()` 處理

### 4. 時間管理

- 使用 `pygame.time.get_ticks()` 獲取遊戲時間
- 所有計時器以毫秒為單位（如 `DEFENSE_DURATION = 1000`）
- 無敵時間、冷卻時間都基於時間差計算

### 5. 平台系統整合模式（v1.2 關鍵）

```python
# game_level.py - 依賴注入模式
self.platform_system = PlatformSystem()
self.player.platform_system = self.platform_system  # 注入到玩家
for enemy in self.enemies:
    enemy.platform_system = self.platform_system    # 注入到敵人
```

**重要**：所有需要平台碰撞的實體都必須設定 `platform_system` 屬性。

## 調試技巧

### v1.3 已知問題和修復指南

1. **二段跳無法觸發**：
   - **問題**：使用連續按鍵檢查 `self.keys[pygame.K_w]`
   - **修復**：改為在 `handle_event()` 中處理 `pygame.KEYDOWN` 事件
   - **位置**：`player.py` 第 62-71 行的跳躍邏輯

2. **滑行攻擊擊飛過強**：
   - **問題**：`enemy.vel_y = -15` 讓敵人飛太高
   - **修復**：調整為 `enemy.vel_y = -8` 讓敵人小幅上升
   - **位置**：`player.py` 第 207 行的 `check_slide_attack()`

### 常見問題排查

1. **拳頭不攻擊**：檢查 `Fist.start_attack()` 是否正確設定目標位置
2. **蓄力攻擊無效**：確認 `start_charging()` 和 `release_attack()` 配對調用
3. **敵人無反應**：確認 `Enemy.update()` 中的 AI 邏輯和狀態檢查
4. **BOSS 戰異常**：BOSS 只受蓄力攻擊傷害，檢查 `is_charged` 參數傳遞
5. **字體顯示問題**：運行 `test_fonts.py` 檢查字體路徑
6. **狀態切換卡住**：檢查 `GameStateManager` 中的狀態字典是否正確更新
7. **平台問題**：檢查實體的 `platform_system` 屬性是否正確設定
8. **敵人不跳躍**：確認敵人類別有 `jump_speed` 屬性和 `_try_jump_to_player()` 方法

### 效能監控

遊戲設計為 60 FPS，如果出現卡頓：

- 檢查 `_check_fist_collisions()` 中的碰撞檢測循環
- 確認敵人 AI 不會進行過多計算
- 使用 `clock.tick(FPS)` 確保幀率穩定

## 擴展指南

### 添加新功能的建議順序

1. 在 `constants.py` 定義相關常數
2. 在對應模組添加核心邏輯
3. 在 `test_update_v3.py` 添加測試案例
4. 更新 UI 顯示（如果需要）

### 保持架構一致性

- 新的遊戲實體應繼承適當的基類（`Enemy` 等）
- 使用依賴注入模式傳遞 `state_manager` 引用
- 遵循現有的事件處理和狀態更新模式
- 跳躍類輸入使用事件處理，連續動作使用狀態檢查

````
