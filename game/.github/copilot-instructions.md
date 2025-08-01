````instructions
# 老鼠格鬥遊戲 - AI 開發指南 (v1.5 清理版)

## 專案架構概覽

這是一個基於 Pygame 的 2D 橫向格鬥遊戲，使用**狀態模式**和**組合模式**實現清晰的架構分離：

```
main.py → GameStateManager → {MenuState, GameLevel, InstructionsState, LevelSelectState}
GameLevel → Player + Enemies + PlatformSystem + UI + ParticleSystem + SaveSystem
Player → Fist (left/right) + charge system + clear screen skill + input handling + physics
Enemies → SmallRobot + GiantRobot + TrainingDummy + MageRobot + EliteMech (AI + physics + platform interaction)
```

### 檔案結構（v1.5 清理後）

```
game/
├── launch_game.py       # 遊戲啟動器
├── requirements.txt     # 依賴清單
├── README.md           # 專案說明
├── game_save.json      # 遊戲存檔
├── assets/             # 遊戲資源
└── src/                # 原始程式碼
    ├── main.py              # 遊戲主迴圈 + Pygame 初始化
    ├── constants.py         # 統一常數配置（所有數值調整的中心）
    ├── entities/            # 遊戲實體模組
    │   ├── player.py       # 玩家類 + Fist 子系統 + 蓄力攻擊 + 清屏技能
    │   ├── enemies.py      # Bullet類 + Enemy基類 + 所有敵人AI
    │   └── items.py        # 血量道具系統 + 拾取特效
    ├── states/             # 遊戲狀態管理
    │   ├── game_states.py  # 中央狀態管理器 + 關卡實例控制
    │   ├── game_level.py   # 關卡邏輯 + 碰撞檢測 + 敵人生成 + 特效整合
    │   ├── menu.py         # 主選單界面
    │   ├── instructions.py # 操作說明界面
    │   └── level_select.py # 關卡選擇界面 + 進度保存
    └── systems/            # 遊戲系統模組
        ├── platform_system.py  # 平台物理 + 碰撞檢測
        ├── font_manager.py     # 繁體中文字體管理
        ├── particle_system.py  # 完整粒子特效系統
        └── save_system.py      # 遊戲進度保存系統
```

### 核心設計原則

- **狀態驅動**：遊戲流程完全由 `GameStateManager` 控制狀態切換
- **組合優於繼承**：Player 包含 Fist 物件而非繼承攻擊能力
- **常數驅動配置**：所有遊戲參數定義在 `constants.py`，支援快速調整
- **平台系統集成**：統一的 `PlatformSystem` 處理所有實體的平台碰撞
- **依賴注入模式**：`platform_system` 通過注入傳遞給所有需要平台碰撞的實體
- **粒子特效系統**：完整的視覺特效系統，支援攻擊、連擊、治療、防禦等特效
- **進度保存系統**：自動保存關卡進度和解鎖狀態

## 關鍵架構模式

### 1. 狀態管理模式

```python
# game_states.py - 中央狀態控制器
class GameStateManager:
    def change_state(self, new_state)  # 狀態切換
    def start_level(self, level_number)  # 動態創建關卡實例
```

**重要**：`GameLevel` 實例在關卡結束時會被銷毀，每次重新開始都創建新實例。

### 2. 輸入處理架構（關鍵設計）

```python
# player.py - 混合輸入模式
def handle_input(self):          # 連續狀態檢查（移動、攻擊）
def handle_event(self, event):   # 單次按鍵事件（跳躍、防禦）
```

**重要設計決策**：
- **移動**使用 `pygame.key.get_pressed()` 實現流暢連續移動
- **跳躍**應使用 `pygame.KEYDOWN` 事件防止連續觸發
- **攻擊**使用連續檢查實現按住蓄力機制

### 3. 平台系統（核心功能）

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

### 4. 蓄力攻擊系統（核心戰鬥機制）

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
- BOSS 戰必須機制：BOSS 對普通攻擊有傷害減免，蓄力攻擊是主要傷害來源

### 5. 清屏技能系統（特殊機制）

```python
# player.py - 清屏技能系統
self.clear_screen_cooldown = 20000  # 20秒冷卻
self.clear_screen_ready = True

def try_clear_screen_skill(self):
    # 檢查冷卻和能量條件
    # 清除範圍內所有敵人子彈
    # 觸發粒子特效
```

**機制特色**：
- 按 Q 鍵觸發，清除半徑 300 像素內的所有敵人子彈
- 20 秒冷卻時間，螢幕右上角顯示冷卻狀態
- 整合粒子特效系統，從玩家位置向外擴散特效

### 6. 粒子特效系統（v1.5 核心系統）

```python
# systems/particle_system.py - 完整特效系統
from systems.particle_system import particle_system

# 在遊戲邏輯中觸發特效
particle_system.create_hit_effect(x, y, is_charged=True)
particle_system.create_combo_effect(x, y, combo_count)
particle_system.create_damage_text(x, y, damage, is_critical=True)
particle_system.create_heal_effect(x, y, heal_amount)
particle_system.create_defense_effect(x, y)
particle_system.create_clear_screen_effect(x, y)
```

**特效系統特點**：
- **多種特效類型**：攻擊爆炸、連擊光環、傷害數字、治療粒子、防禦光環、清屏擴散
- **分層渲染**：光環（背景）→ 粒子（中間）→ 文字（前景）
- **性能優化**：自動清理過期特效，支援最大數量限制
- **物理模擬**：粒子受重力影響，透明度漸變效果

### 7. 敵人 AI 跳躍系統

```python
# enemies.py - 智能跳躍追擊
class SmallRobot(Enemy):
    def _try_jump_to_player(self, player):  # 檢測並跳躍至玩家平台
```

**AI 跳躍邏輯**：
- 檢測玩家是否在上方平台（利用 `platform_system.get_nearest_platform_above()`）
- 有跳躍冷卻時間防止過度跳躍（小機器人 3 秒，BOSS 4 秒）
- 空中移動：跳躍時可調整水平方向追擊玩家

### 8. 進度保存系統

```python
# systems/save_system.py - 全域保存實例
save_system.unlock_level(level_number)
save_system.complete_level(level_number, completion_time, player_health)
save_system.is_level_unlocked(level_number)
```

**保存機制**：
- 自動保存關卡解鎖狀態和完成情況
- JSON 格式存檔，支援關卡統計和隱藏關卡解鎖
- 全域單例模式，各狀態模組共享同一實例

## 開發工作流程

### 遊戲啟動

```bash
# 主要啟動方式
python launch_game.py

# 或使用批次檔案（Windows）
start_game_restructured.bat

# 直接運行
cd src && python main.py
```

### 開發與除錯

```bash
# 檢查項目結構和運行狀態
python -c "import src.main; print('項目結構正確')"

# 測試字體系統
python -c "from src.systems.font_manager import get_font; print('字體系統正常')"

# 測試粒子系統
python -c "from src.systems.particle_system import particle_system; print('粒子系統正常')"
```

### 新增關卡流程

1. 在 `constants.py` 定義新關卡常數（如 `LEVEL_4 = 4`）
2. 在 `game_level.py` 的 `_setup_level()` 添加關卡配置
3. 在 `enemies.py` 創建新敵人類別（繼承 `Enemy` 基類）
4. 配置關卡平台佈局（呼叫 `platform_system.add_platform()`）
5. 整合粒子特效到戰鬥和互動中

### 新增敵人行為模式

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

    def take_damage(self, damage, knockback=False, stun=False, source_x=None):
        super().take_damage(damage, knockback, stun, source_x)
        # 添加受傷特效
        from systems.particle_system import particle_system
        hit_x = self.x + self.width // 2
        hit_y = self.y + self.height // 2
        particle_system.create_hit_effect(hit_x, hit_y, knockback)
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

### 3. 依賴注入模式
```python
# game_level.py - 依賴注入模式
self.platform_system = PlatformSystem()
self.player.platform_system = self.platform_system  # 注入到玩家
for enemy in self.enemies:
    enemy.platform_system = self.platform_system    # 注入到敵人
```

**重要**：所有需要平台碰撞的實體都必須設定 `platform_system` 屬性。

### 4. 時間管理
- 使用 `pygame.time.get_ticks()` 獲取遊戲時間
- 所有計時器以毫秒為單位（如 `DEFENSE_DURATION = 1000`）
- 無敵時間、冷卻時間都基於時間差計算

## 常見問題排查

### 核心系統問題
1. **拳頭不攻擊**：檢查 `Fist.start_attack()` 是否正確設定目標位置
2. **蓄力攻擊無效**：確認 `start_charging()` 和 `release_attack()` 配對調用
3. **清屏技能無效**：檢查冷卻時間和 `particle_system` 導入
4. **敵人無反應**：確認 `Enemy.update()` 中的 AI 邏輯和狀態檢查
5. **BOSS 戰異常**：BOSS 對普通攻擊有傷害減免，檢查 `is_charged` 參數傳遞

### 系統整合問題
6. **字體顯示問題**：檢查 `font_manager.py` 中的字體路徑
7. **狀態切換卡住**：檢查 `GameStateManager` 中的狀態字典是否正確更新
8. **平台問題**：檢查實體的 `platform_system` 屬性是否正確設定
9. **粒子特效問題**：檢查 `particle_system.py` 導入和 `update()/draw()` 調用
10. **存檔問題**：檢查 `save_system.py` 的 JSON 檔案讀寫權限

### 效能監控
遊戲設計為 60 FPS，如果出現卡頓：
- 檢查 `_check_fist_collisions()` 中的碰撞檢測循環
- 確認敵人 AI 不會進行過多計算
- 使用 `clock.tick(FPS)` 確保幀率穩定
- 監控粒子特效數量，避免同時產生過多特效

## 擴展指南

### 添加新功能的建議順序
1. 在 `constants.py` 定義相關常數
2. 在對應模組添加核心邏輯
3. 更新 UI 顯示（如果需要）
4. 整合粒子特效增強視覺體驗
5. 測試功能並調整參數

### 保持架構一致性
- 新的遊戲實體應繼承適當的基類（`Enemy` 等）
- 使用依賴注入模式傳遞系統引用
- 遵循現有的事件處理和狀態更新模式
- 跳躍類輸入使用事件處理，連續動作使用狀態檢查
- 確保新功能整合到粒子特效和進度保存系統中

````

# 老鼠格鬥遊戲 - AI 開發指南

## 專案架構概覽

這是一個基於 Pygame 的 2D 橫向格鬥遊戲，使用**狀態模式**和**組合模式**實現清晰的架構分離：

```
main.py → GameStateManager → {MenuState, GameLevel, InstructionsState}
GameLevel → Player + Enemies + PlatformSystem + BulletSystem + UI + effects
Player → Fist (left/right) + charge system + input handling + physics + platform collision
Enemies → SmallRobot + GiantRobot + TrainingDummy + MageRobot (with AI + physics + platform interaction)
```

### 檔案結構（v1.5 最新）

```
game/src/
├── main.py              # 遊戲主迴圈 + Pygame 初始化
├── constants.py         # 統一常數配置（所有數值調整的中心）
├── entities/            # 遊戲實體模組
│   ├── player.py       # 玩家類 + Fist 子系統 + 蓄力攻擊 + 連擊系統
│   ├── enemies.py      # Bullet類 + Enemy基類 + 所有敵人AI + 法師機器人
│   └── items.py        # 血量道具系統 + 拾取特效
├── states/             # 遊戲狀態管理
│   ├── game_states.py  # 中央狀態管理器 + 關卡實例控制
│   ├── game_level.py   # 關卡邏輯 + 碰撞檢測 + 敵人生成 + 特效整合
│   ├── menu.py         # 主選單界面
│   ├── instructions.py # 操作說明界面
│   └── level_select.py # 關卡選擇界面 + 進度保存
└── systems/            # 遊戲系統模組
    ├── platform_system.py  # 平台物理 + 碰撞檢測
    ├── font_manager.py     # 繁體中文字體管理
    ├── particle_system.py  # 完整粒子特效系統（v1.5 新增）
    └── save_system.py      # 遊戲進度保存系統
```

### 核心設計原則

- **狀態驅動**：遊戲流程完全由 `GameStateManager` 控制狀態切換
- **組合優於繼承**：Player 包含 Fist 物件而非繼承攻擊能力
- **常數驅動配置**：所有遊戲參數定義在 `constants.py`，支援快速調整
- **平台系統集成**：統一的 `PlatformSystem` 處理所有實體的平台碰撞
- **依賴注入模式**：`platform_system` 通過注入傳遞給所有需要平台碰撞的實體
- **粒子特效系統**：完整的視覺特效系統，支援攻擊、連擊、治療、防禦等特效
- **模組化擴展**：各系統模組支援獨立開發和測試

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

### 4. 二段跳系統（已修復核心功能）

```python
# player.py + enemies.py - 二段跳狀態機
self.double_jump_available = True  # 地面重置為True
# 首次跳躍：設定double_jump_available = True
# 二段跳：設定double_jump_available = False
```

**重要機制**：

- 玩家和所有敵人都支援二段跳（`SmallRobot`, `GiantRobot`）
- 落地時重置 `double_jump_available = True`
- 敵人 AI 會利用二段跳追擊玩家到更高平台

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
- BOSS 戰必須機制：BOSS 對普通攻擊有傷害減免，蓄力攻擊是主要傷害來源

### 6. 滑行攻擊系統（v1.3 特殊機制）

```python
# player.py - 滑行特殊攻擊
def check_slide_attack(self, enemies):
    # 當前實作：適度的向上擊飛力度
    # 為敵人提供合理的戰術調整時間
```

**機制特色**：

- 滑行攻擊會給敵人適度的向上擊飛力度
- 敵人被擊飛後能夠回到地面繼續戰鬥
- 玩家可以利用滑行攻擊創造戰術空間

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

### 9. BOSS 子彈系統（v1.4 新增）

```python
# enemies.py - 子彈物件系統
class Bullet:
    def __init__(self, x, y, target_x, target_y)  # 朝向目標的追蹤彈
class GiantRobot:
    self.bullets = []  # 子彈集合
    def ranged_attack(self, player)  # 發射多發子彈攻擊
```

**子彈機制**：

- 獨立的 `Bullet` 類別處理 BOSS 遠程攻擊
- 支援散彈、連發、高頻率攻擊模式
- 在 `game_level.py` 的 `_check_bullet_collisions()` 處理玩家碰撞
- 玩家防禦可格擋子彈攻擊

### 10. 擊退方向修正（v1.4 修復）

```python
# enemies.py - 訓練人偶擊退修正
class TrainingDummy:
    def apply_knockback(self, source_x):
        # 修正：正確計算相對於攻擊源的擊退方向
        # 確保被蓄力攻擊時向拳頭反方向擊退
```

### 11. 粒子特效系統（v1.5 新增核心系統）

```python
# systems/particle_system.py - 完整特效系統
from systems.particle_system import particle_system

# 在遊戲邏輯中觸發特效
particle_system.create_hit_effect(x, y, is_charged=True)
particle_system.create_combo_effect(x, y, combo_count)
particle_system.create_damage_text(x, y, damage, is_critical=True)
particle_system.create_heal_effect(x, y, heal_amount)
particle_system.create_defense_effect(x, y)
particle_system.create_clear_screen_effect(x, y)
```

**特效系統特點**：

- **多種特效類型**：攻擊爆炸、連擊光環、傷害數字、治療粒子、防禦光環
- **分層渲染**：光環（背景）→ 粒子（中間）→ 文字（前景）
- **性能優化**：自動清理過期特效，支援最大數量限制
- **物理模擬**：粒子受重力影響，透明度漸變效果
- **易於擴展**：新特效只需調用對應方法即可

### 12. 繁體中文字體管理

```python
# systems/font_manager.py - 全域字體管理
from systems.font_manager import get_font
font = get_font('large')  # 自動使用最佳中文字體
```

字體管理器會自動檢測 Windows 系統字體，優先使用微軟正黑體。

## 開發工作流程

### 遊戲啟動

```bash
# 主要啟動方式
python game/launch_game.py

# 或使用批次檔案（Windows）
start_game_restructured.bat

# 直接運行
cd game/src && python main.py
```

### 特效系統測試

```bash
# 測試粒子特效系統
cd game/src && python ../test_particle_effects.py

# 按數字鍵觸發不同特效：
# 1-2: 攻擊特效  3-4: 連擊特效  5-6: 傷害數字
# 7: 治療特效   8: 防禦特效    9: 清屏特效
# 0: 關卡完成   T: 瞬移特效    C: 清除特效
```

### 測試與除錯

```bash
# 檢查項目結構和運行狀態
cd game
python -c "import src.main; print('項目結構正確')"

# 測試字體系統
python -c "from src.systems.font_manager import get_font; print('字體系統正常')"
```

### 新增關卡流程

1. 在 `constants.py` 定義新關卡常數
2. 在 `game_level.py` 的 `_setup_level()` 添加關卡配置
3. 在 `enemies.py` 創建新敵人類別（繼承 `Enemy` 基類）
4. **v1.2 新增**：配置關卡平台佈局（呼叫 `platform_system.add_platform()`）
5. **v1.5 新增**：整合粒子特效到戰鬥和互動中

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

    def take_damage(self, damage, knockback=False, stun=False, source_x=None):
        super().take_damage(damage, knockback, stun, source_x)
        # 添加受傷特效
        try:
            from systems.particle_system import particle_system
            hit_x = self.x + self.width // 2
            hit_y = self.y + self.height // 2
            particle_system.create_hit_effect(hit_x, hit_y, knockback)
        except ImportError:
            pass
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

### 最新修復指南（2025 年 8 月）

1. **粒子特效系統新增（v1.5）**：

   - **新增**：完整的 `particle_system.py` 模組，支援多種視覺特效
   - **功能**：攻擊爆炸、連擊光環、傷害數字、治療粒子、防禦光環等
   - **整合**：已整合到所有戰鬥、技能、道具拾取系統中
   - **測試**：`test_particle_effects.py` 提供完整特效演示

2. **BOSS 子彈系統升級（v1.4）**：

   - **新增**：獨立的 `Bullet` 類別實現物件化子彈系統
   - **功能**：支援散彈、連發、高頻率攻擊
   - **位置**：`enemies.py` 中的 `Bullet` 類和 `GiantRobot.ranged_attack()`

3. **擊退方向修正（v1.4）**：

   - **修復**：訓練人偶被蓄力攻擊時的擊退方向錯誤
   - **改進**：正確計算相對於攻擊源的擊退方向
   - **位置**：`enemies.py` 中的 `TrainingDummy.apply_knockback()`

4. **平台系統擴展（v1.4）**：

   - **修復**：訓練人偶被蓄力攻擊時的擊退方向錯誤
   - **改進**：正確計算相對於攻擊源的擊退方向
   - **位置**：`enemies.py` 中的 `TrainingDummy.apply_knockback()`

5. **平台系統擴展（v1.4）**：

   - **增強**：第三關平台數量增加，提供更豐富的戰鬥空間
   - **影響**：改善 BOSS 戰的戰術深度
   - **位置**：`game_level.py` 中的 `_setup_level()` 方法

6. **敵人邊界卡住問題（之前版本已修復）**：

   - **問題**：小型敵人在螢幕邊緣卡住無法反彈
   - **修復**：改進衝刺邊界檢查，使用預測位置而非事後修正
   - **位置**：`enemies.py` 中的 `SmallRobot.update()` 和 `_apply_screen_boundary()`

7. **BOSS 傷害機制調整（之前版本已修復）**：
   - **變更**：BOSS 現在會受普通攻擊傷害（減半）但蓄力攻擊仍是主要傷害源
   - **影響**：戰鬥更流暢，保持挑戰性
   - **位置**：`enemies.py` 中的 `GiantRobot.take_damage()`

### 常見問題排查

1. **拳頭不攻擊**：檢查 `Fist.start_attack()` 是否正確設定目標位置
2. **蓄力攻擊無效**：確認 `start_charging()` 和 `release_attack()` 配對調用
3. **敵人無反應**：確認 `Enemy.update()` 中的 AI 邏輯和狀態檢查
4. **BOSS 戰異常**：BOSS 對普通攻擊有傷害減免，檢查 `is_charged` 參數傳遞
5. **字體顯示問題**：運行 `test_fonts.py` 檢查字體路徑
6. **狀態切換卡住**：檢查 `GameStateManager` 中的狀態字典是否正確更新
7. **平台問題**：檢查實體的 `platform_system` 屬性是否正確設定
8. **敵人不跳躍**：確認敵人類別有 `jump_speed` 屬性和 `_try_jump_to_player()` 方法
9. **敵人邊界卡住**：檢查 `_apply_screen_boundary()` 覆蓋和衝刺邊界邏輯
10. **BOSS 子彈問題**：檢查 `Bullet` 類別初始化和 `_check_bullet_collisions()` 方法
11. **擊退方向錯誤**：確認 `apply_knockback(source_x)` 中的方向計算邏輯
12. **粒子特效問題**：檢查 `particle_system.py` 導入和 `update()/draw()` 調用
13. **特效性能問題**：使用 `particle_system.get_effect_count()` 監控特效數量

### 效能監控

遊戲設計為 60 FPS，如果出現卡頓：

- 檢查 `_check_fist_collisions()` 中的碰撞檢測循環
- 確認敵人 AI 不會進行過多計算
- 使用 `clock.tick(FPS)` 確保幀率穩定
- 監控粒子特效數量，避免同時產生過多特效

## 擴展指南

### 添加新功能的建議順序

1. 在 `constants.py` 定義相關常數
2. 在對應模組添加核心邏輯
3. 在 `test_particle_effects.py` 或相關測試文件添加測試案例
4. 更新 UI 顯示（如果需要）
5. 整合粒子特效增強視覺體驗

### 保持架構一致性

- 新的遊戲實體應繼承適當的基類（`Enemy` 等）
- 使用依賴注入模式傳遞 `state_manager` 引用
- 遵循現有的事件處理和狀態更新模式
- 跳躍類輸入使用事件處理，連續動作使用狀態檢查

```

```
