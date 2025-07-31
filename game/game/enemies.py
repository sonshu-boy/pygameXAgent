"""
敵人類別定義
"""

import pygame
import math
from constants import *


class Bullet:
    """BOSS 發射的子彈"""

    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = BOSS_BULLET_SIZE

        # 計算朝向目標的方向
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.vel_x = (dx / distance) * BOSS_BULLET_SPEED
            self.vel_y = (dy / distance) * BOSS_BULLET_SPEED
        else:
            self.vel_x = 0
            self.vel_y = 0

        self.alive = True

    def update(self):
        """更新子彈位置"""
        self.x += self.vel_x
        self.y += self.vel_y

        # 檢查是否超出螢幕邊界
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            self.alive = False

    def get_rect(self):
        """獲取子彈碰撞矩形"""
        return pygame.Rect(
            self.x - self.size // 2, self.y - self.size // 2, self.size, self.size
        )

    def draw(self, screen):
        """繪製子彈"""
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size // 2)


class Enemy:
    """敵人基類"""

    def __init__(self, x, y, width, height, health=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.alive = True
        self.platform_system = None  # 將由GameLevel設定

        # 物理狀態
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.double_jump_available = True  # 二段跳可用性

        # 狀態
        self.invincible = False
        self.invincible_start_time = 0
        self.stunned = False
        self.stun_start_time = 0

        # 擊退狀態
        self.knockback = False
        self.knockback_start_time = 0
        self.knockback_vel_x = 0

    def take_damage(self, damage=1, knockback=False, stun=False):
        """受到傷害"""
        if not self.invincible and self.alive:
            self.health -= damage
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

            if knockback:
                self._apply_knockback()
            if stun:
                self.stunned = True
                self.stun_start_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.alive = False

    def _apply_knockback(self):
        """應用擊退效果"""
        self.knockback = True
        self.knockback_start_time = pygame.time.get_ticks()
        # 根據敵人位置決定擊退方向（遠離螢幕中心）
        center_x = WINDOW_WIDTH // 2
        if self.x < center_x:
            self.knockback_vel_x = -KNOCKBACK_FORCE
        else:
            self.knockback_vel_x = KNOCKBACK_FORCE

    def update(self, player):
        """更新敵人狀態（子類重寫）"""
        current_time = pygame.time.get_ticks()

        # 更新無敵時間
        if self.invincible:
            if current_time - self.invincible_start_time > INVINCIBLE_DURATION:
                self.invincible = False

        # 更新眩暈狀態
        if self.stunned:
            if current_time - self.stun_start_time > STUN_DURATION:
                self.stunned = False

        # 更新擊退狀態
        if self.knockback:
            if current_time - self.knockback_start_time > KNOCKBACK_DURATION:
                self.knockback = False
                self.knockback_vel_x = 0
            else:
                # 應用擊退移動並檢查邊界
                old_x = self.x
                self.x += self.knockback_vel_x * 0.1
                # 確保不超出邊界
                self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))

        # 應用重力（如果不在地面上）
        if not self.on_ground:
            self.vel_y += GRAVITY

        # 更新垂直位置
        self.y += self.vel_y

        # 檢查平台碰撞
        self._check_platform_collisions()

        # 地面碰撞檢測
        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True
            self.double_jump_available = True  # 重置二段跳

        # 螢幕邊界限制（子類可以覆蓋）
        self._apply_screen_boundary()

    def _apply_screen_boundary(self):
        """應用螢幕邊界限制（子類可以覆蓋此方法）"""
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))

    def _check_platform_collisions(self):
        """檢查與平台的碰撞"""
        if self.platform_system is None:
            return

        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        platform, new_y = self.platform_system.check_collision(enemy_rect, self.vel_y)

        if platform is not None:
            self.y = new_y
            self.vel_y = 0
            self.on_ground = True
            self.double_jump_available = True  # 重置二段跳
        else:
            # 檢查是否仍在平台上
            if self.on_ground and self.vel_y >= 0:
                # 檢查是否還在地面或平台上
                on_platform = self.platform_system.is_on_platform(enemy_rect)
                on_ground = self.y + self.height >= GROUND_Y - 5

                if not on_platform and not on_ground:
                    self.on_ground = False

    def can_jump_to_player(self, player):
        """判斷是否可以跳躍到玩家位置"""
        if not self.on_ground or self.stunned or self.knockback:
            return False

        # 檢查玩家是否在上方
        if player.y >= self.y - 50:  # 玩家不在足夠高的位置
            return False

        # 檢查水平距離是否合理
        horizontal_distance = abs(player.x - self.x)
        if horizontal_distance > 150:  # 距離太遠
            return False

        return True

    def jump_towards_player(self, player):
        """朝玩家方向跳躍（包含二段跳）"""
        jump_speed = getattr(self, "jump_speed", PLAYER_JUMP_SPEED)
        double_jump_speed = getattr(self, "double_jump_speed", PLAYER_DOUBLE_JUMP_SPEED)

        if self.on_ground:
            # 首次跳躍
            self.vel_y = -jump_speed
            self.on_ground = False
            self.double_jump_available = True
        elif self.double_jump_available and not self.stunned and not self.knockback:
            # 二段跳
            self.vel_y = -double_jump_speed
            self.double_jump_available = False

        # 添加水平移動朝向玩家
        if player.x > self.x:
            self.vel_x = min(self.vel_x + 2, 5)
        else:
            self.vel_x = max(self.vel_x - 2, -5)

        return True

    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """繪製敵人（子類重寫）"""
        pass


class TrainingDummy(Enemy):
    """訓練用人偶 - 第一關敵人"""

    def __init__(self, x, y):
        super().__init__(x, y, DUMMY_WIDTH, DUMMY_HEIGHT, health=3)
        self.color = GRAY

    def update(self, player):
        """更新訓練人偶（不主動攻擊）"""
        super().update(player)

        # 訓練人偶不會主動移動或跳躍，只會被動受擊

    def draw(self, screen):
        """繪製訓練人偶"""
        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製十字標記
        cross_size = 10
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        pygame.draw.line(
            screen,
            RED,
            (center_x - cross_size, center_y),
            (center_x + cross_size, center_y),
            3,
        )
        pygame.draw.line(
            screen,
            RED,
            (center_x, center_y - cross_size),
            (center_x, center_y + cross_size),
            3,
        )


class SmallRobot(Enemy):
    """小型老鼠機器人 - 第二關敵人"""

    def __init__(self, x, y):
        super().__init__(
            x, y, SMALL_ROBOT_WIDTH, SMALL_ROBOT_HEIGHT, health=SMALL_ROBOT_HEALTH
        )
        self.color = (100, 100, 150)  # 藍灰色
        self.speed = SMALL_ROBOT_SPEED
        self.charging = False
        self.charge_speed = SMALL_ROBOT_CHARGE_SPEED
        self.charge_cooldown = 0
        self.direction = 1  # 1 為右，-1 為左
        self.jump_speed = SMALL_ROBOT_JUMP_SPEED
        self.double_jump_speed = SMALL_ROBOT_DOUBLE_JUMP_SPEED
        self.jump_cooldown = 0

    def update(self, player):
        """更新小型機器人"""
        current_time = pygame.time.get_ticks()

        # 在更新物理狀態之前先處理AI行為
        if not self.stunned and not self.knockback:
            # 計算與玩家的距離
            distance_to_player = abs(self.x - player.x)
            height_difference = self.y - player.y

            # 嘗試跳躍到玩家位置（如果玩家在上方）
            if (
                height_difference > 50
                and distance_to_player < 100
                and current_time > self.jump_cooldown
                and self.can_jump_to_player(player)
            ):

                if self.jump_towards_player(player):
                    self.jump_cooldown = current_time + 3000  # 3秒跳躍冷卻

            # 如果玩家在附近且冷卻時間結束，開始衝撞
            elif distance_to_player < 200 and current_time > self.charge_cooldown:
                if not self.charging:
                    self.charging = True
                    self.direction = 1 if player.x > self.x else -1

            # 執行衝撞
            if self.charging:
                # 預計移動位置
                new_x = self.x + self.direction * self.charge_speed

                # 檢查邊界，如果會超出螢幕則停止衝刺並反彈
                if new_x <= 0 or new_x >= WINDOW_WIDTH - self.width:
                    self.charging = False
                    self.charge_cooldown = current_time + 2000  # 2秒冷卻
                    self.direction *= -1  # 反轉方向
                    # 確保不超出邊界
                    self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))
                else:
                    # 安全移動
                    self.x = new_x

                # 檢查是否衝撞到玩家
                if self.get_rect().colliderect(player.get_rect()):
                    player.take_damage()
                    self.charging = False
                    self.charge_cooldown = current_time + 2000  # 2秒冷卻

            else:
                # 普通移動（加入水平速度）
                if not self.on_ground:
                    # 空中移動
                    new_x = self.x + self.vel_x
                    # 邊界檢查
                    if new_x <= 0:
                        self.x = 0
                        self.vel_x = 0
                        self.direction = 1  # 設定向右移動
                    elif new_x >= WINDOW_WIDTH - self.width:
                        self.x = WINDOW_WIDTH - self.width
                        self.vel_x = 0
                        self.direction = -1  # 設定向左移動
                    else:
                        self.x = new_x
                    self.vel_x *= 0.95  # 空中阻力
                else:
                    # 地面移動
                    new_x = self.x + self.direction * self.speed
                    # 邊界檢查和反彈
                    if new_x <= 0:
                        self.x = 0
                        self.direction = 1  # 反轉方向向右
                    elif new_x >= WINDOW_WIDTH - self.width:
                        self.x = WINDOW_WIDTH - self.width
                        self.direction = -1  # 反轉方向向左
                    else:
                        self.x = new_x
                    self.vel_x = 0

        # 調用父類更新方法（處理物理、狀態等）
        super().update(player)

    def _apply_screen_boundary(self):
        """SmallRobot 使用自定義的邊界處理，不使用父類的強制限制"""
        # 不執行任何操作，讓自定義的邊界處理邏輯生效
        pass

    def _apply_knockback(self):
        """應用擊退效果"""
        self.charging = False  # 停止衝撞
        self.charge_cooldown = pygame.time.get_ticks() + 1500
        # 調用父類的擊退方法
        super()._apply_knockback()

    def draw(self, screen):
        """繪製小型機器人"""
        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW  # 眩暈時變黃
        elif self.charging:
            color = RED  # 衝撞時變紅
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製機械眼睛
        eye_size = 3
        pygame.draw.circle(screen, RED, (int(self.x + 10), int(self.y + 10)), eye_size)
        pygame.draw.circle(screen, RED, (int(self.x + 30), int(self.y + 10)), eye_size)


class GiantRobot(Enemy):
    """巨型老鼠機器人 - 第三關BOSS"""

    def __init__(self, x, y):
        super().__init__(x, y, BOSS_WIDTH, BOSS_HEIGHT, health=BOSS_HEALTH)
        self.color = (150, 50, 50)  # 深紅色
        self.speed = BOSS_SPEED
        self.direction = 1
        self.attack_cooldown = 0
        self.special_attack_cooldown = 0
        self.attack_pattern = 0  # 攻擊模式
        self.jump_speed = BOSS_JUMP_SPEED
        self.double_jump_speed = BOSS_DOUBLE_JUMP_SPEED
        self.jump_cooldown = 0
        self.bullets = []  # 子彈列表
        self.ranged_attack_cooldown = 0

    def update(self, player):
        """更新巨型機器人BOSS"""
        super().update(player)
        current_time = pygame.time.get_ticks()

        if not self.stunned and not self.knockback:
            # 計算與玩家的距離和高度差
            distance_to_player = abs(self.x - player.x)
            height_difference = self.y - player.y

            # 嘗試跳躍到玩家位置（如果玩家在上方且不太遠）
            if (
                height_difference > 50
                and distance_to_player < 150
                and current_time > self.jump_cooldown
                and self.can_jump_to_player(player)
            ):

                if self.jump_towards_player(player):
                    self.jump_cooldown = current_time + 4000  # 4秒跳躍冷卻

            # 移動朝向玩家
            elif distance_to_player > 50:
                if player.x > self.x:
                    move_amount = self.speed
                    if not self.on_ground:
                        move_amount = self.vel_x
                    self.x += move_amount
                    self.direction = 1
                else:
                    move_amount = self.speed
                    if not self.on_ground:
                        move_amount = self.vel_x
                    self.x -= move_amount
                    self.direction = -1

            # 普通攻擊與遠程攻擊選擇
            if current_time > self.attack_cooldown:
                if distance_to_player < 100:
                    # 近距離攻擊
                    if self.get_rect().colliderect(player.get_rect()):
                        player.take_damage()
                        self.attack_cooldown = current_time + 1500
                elif (
                    distance_to_player > BOSS_RANGED_ATTACK_DISTANCE
                    and current_time > self.ranged_attack_cooldown
                ):
                    # 遠程攻擊：玩家離得太遠時發射子彈
                    self._ranged_attack(player)
                    self.ranged_attack_cooldown = (
                        current_time + BOSS_RANGED_ATTACK_COOLDOWN
                    )

            # 特殊攻擊 - 當血量低於50%時觸發
            if (self.health / self.max_health) <= BOSS_SPECIAL_ATTACK_THRESHOLD:
                if current_time > self.special_attack_cooldown:
                    self._special_attack(player)
                    self.special_attack_cooldown = current_time + 5000  # 5秒冷卻

            # 在空中時應用水平移動慣性
            if not self.on_ground:
                self.x += self.vel_x
                self.vel_x *= 0.9  # 空中阻力

        # 更新子彈
        for bullet in self.bullets[:]:  # 使用切片創建副本來安全地修改列表
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)

    def _ranged_attack(self, player):
        """遠程攻擊：發射子彈"""
        # 從 BOSS 中心發射子彈朝向玩家
        boss_center_x = self.x + self.width // 2
        boss_center_y = self.y + self.height // 2
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2

        bullet = Bullet(boss_center_x, boss_center_y, player_center_x, player_center_y)
        self.bullets.append(bullet)

    def _special_attack(self, player):
        """特殊攻擊技能 - 範圍攻擊"""
        # 強力範圍攻擊，只能通過防禦抵擋
        distance_to_player = abs(self.x - player.x)
        if distance_to_player < 200:  # 更大的攻擊範圍
            if not player.is_defending:
                player.take_damage()
                # 可以在這裡添加視覺效果表示範圍攻擊

    def _apply_knockback(self):
        """BOSS受到擊退效果較小但仍會有效果"""
        self.knockback = True
        self.knockback_start_time = pygame.time.get_ticks()
        # BOSS的擊退力度減半
        center_x = WINDOW_WIDTH // 2
        if self.x < center_x:
            self.knockback_vel_x = -KNOCKBACK_FORCE * 0.5
        else:
            self.knockback_vel_x = KNOCKBACK_FORCE * 0.5

    def take_damage(self, damage=1, knockback=False, stun=False):
        """BOSS受傷處理 - 現在普通攻擊也能造成傷害"""
        # BOSS現在接受所有攻擊，但對普通攻擊有傷害減免
        if not self.invincible and self.alive:
            # 如果是普通攻擊（傷害值為1），減少傷害值但仍然有效
            if damage < CHARGE_DAMAGE_MULTIPLIER:
                actual_damage = max(1, damage // 2)  # 普通攻擊傷害減半但至少為1
            else:
                actual_damage = damage  # 蓄力攻擊保持原有傷害

            self.health -= actual_damage
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

            if knockback:
                self._apply_knockback()
            if stun:
                self.stunned = True
                self.stun_start_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.alive = False

    def draw(self, screen):
        """繪製巨型機器人BOSS"""
        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製威脅性的紅眼
        eye_size = 6
        pygame.draw.circle(screen, RED, (int(self.x + 20), int(self.y + 20)), eye_size)
        pygame.draw.circle(screen, RED, (int(self.x + 60), int(self.y + 20)), eye_size)

        # 繪製血量條
        self._draw_health_bar(screen)

        # 繪製子彈
        for bullet in self.bullets:
            bullet.draw(screen)

    def _draw_health_bar(self, screen):
        """繪製BOSS血量條"""
        bar_width = 200
        bar_height = 10
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = 30

        # 背景
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

        # 血量
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        color = GREEN if health_ratio > 0.5 else (YELLOW if health_ratio > 0.2 else RED)
        pygame.draw.rect(screen, color, (bar_x, bar_y, health_width, bar_height))

        # 邊框
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
