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


class MissileBullet(Bullet):
    """導彈子彈 - 具有追蹤能力"""

    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, target_x, target_y)
        self.size = 12  # 比普通子彈大
        self.speed = 6  # 比普通子彈慢但有追蹤
        self.tracking = True
        self.explosion_radius = 30
        self.exploded = False

    def update(self, player=None):
        """更新導彈位置，具有微弱追蹤能力"""
        if player and self.tracking:
            # 微調方向朝向玩家
            dx = (player.x + player.width // 2) - self.x
            dy = (player.y + player.height // 2) - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                # 混合原始方向和追蹤方向
                track_strength = 0.1  # 追蹤強度
                self.vel_x = (
                    self.vel_x * (1 - track_strength)
                    + (dx / distance) * self.speed * track_strength
                )
                self.vel_y = (
                    self.vel_y * (1 - track_strength)
                    + (dy / distance) * self.speed * track_strength
                )

        super().update()

    def draw(self, screen):
        """繪製導彈"""
        # 導彈主體（橙色）
        pygame.draw.circle(
            screen, (255, 165, 0), (int(self.x), int(self.y)), self.size // 2
        )
        # 導彈尾焰效果
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(self.x - self.vel_x), int(self.y - self.vel_y)),
            self.size // 4,
        )


class LaserBeam(Bullet):
    """雷射光束 - 寬範圍直線攻擊"""

    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, target_x, target_y)
        self.width = 15  # 雷射寬度
        self.length = 0  # 雷射長度，逐漸增長
        self.max_length = 400
        self.grow_speed = 20
        self.damage_dealt = False

        # 計算雷射方向
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance
        else:
            self.direction_x = 1
            self.direction_y = 0

    def update(self, player=None):
        """更新雷射光束"""
        self.length = min(self.length + self.grow_speed, self.max_length)

        # 雷射存在時間限制
        if self.length >= self.max_length:
            # 保持一段時間後消失
            import pygame

            if not hasattr(self, "start_time"):
                self.start_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.start_time > 500:
                self.alive = False

    def get_rect(self):
        """獲取雷射碰撞矩形"""
        end_x = self.x + self.direction_x * self.length
        end_y = self.y + self.direction_y * self.length

        # 創建沿雷射路徑的矩形
        min_x = min(self.x, end_x) - self.width // 2
        max_x = max(self.x, end_x) + self.width // 2
        min_y = min(self.y, end_y) - self.width // 2
        max_y = max(self.y, end_y) + self.width // 2

        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw(self, screen):
        """繪製雷射光束"""
        if self.length > 0:
            end_x = self.x + self.direction_x * self.length
            end_y = self.y + self.direction_y * self.length

            # 繪製雷射光束（紅色核心，外圍白光）
            pygame.draw.line(
                screen, WHITE, (self.x, self.y), (end_x, end_y), self.width + 4
            )
            pygame.draw.line(screen, RED, (self.x, self.y), (end_x, end_y), self.width)
            pygame.draw.line(
                screen, YELLOW, (self.x, self.y), (end_x, end_y), self.width // 2
            )


class TrackingBullet:
    """法師機器人發射的追蹤子彈"""

    def __init__(self, x, y, target_player):
        self.x = x
        self.y = y
        self.target_player = target_player
        self.size = TRACKING_BULLET_SIZE
        self.speed = TRACKING_BULLET_SPEED
        self.alive = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = TRACKING_BULLET_LIFETIME

        # 初始速度方向（朝向玩家）
        dx = target_player.x + target_player.width // 2 - x
        dy = target_player.y + target_player.height // 2 - y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = self.speed
            self.vel_y = 0

    def update(self):
        """更新追蹤子彈"""
        current_time = pygame.time.get_ticks()

        # 檢查存在時間
        if current_time - self.spawn_time > self.lifetime:
            self.alive = False
            return

        # 檢查螢幕邊界
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            self.alive = False
            return

        # 追蹤玩家
        if self.target_player and self.target_player.health > 0:
            target_x = self.target_player.x + self.target_player.width // 2
            target_y = self.target_player.y + self.target_player.height // 2

            # 計算朝向目標的方向
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                # 混合當前速度和追蹤方向
                target_vel_x = (dx / distance) * self.speed
                target_vel_y = (dy / distance) * self.speed

                # 應用追蹤強度
                self.vel_x += (
                    target_vel_x - self.vel_x
                ) * TRACKING_BULLET_TRACKING_STRENGTH
                self.vel_y += (
                    target_vel_y - self.vel_y
                ) * TRACKING_BULLET_TRACKING_STRENGTH

                # 確保速度不超過最大值
                current_speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
                if current_speed > self.speed:
                    self.vel_x = (self.vel_x / current_speed) * self.speed
                    self.vel_y = (self.vel_y / current_speed) * self.speed

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

    def get_rect(self):
        """獲取子彈碰撞矩形"""
        return pygame.Rect(
            self.x - self.size // 2, self.y - self.size // 2, self.size, self.size
        )

    def draw(self, screen):
        """繪製追蹤子彈"""
        # 繪製子彈本體（紫色）
        pygame.draw.circle(
            screen, (150, 0, 255), (int(self.x), int(self.y)), self.size // 2
        )

        # 繪製追蹤光環效果
        pygame.draw.circle(
            screen, (255, 100, 255), (int(self.x), int(self.y)), self.size // 2 + 2, 2
        )

        # 繪製中心亮點
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 4)


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
        self.death_sound_played = False  # 防止死亡音效重複播放
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

    def take_damage(self, damage=1, knockback=False, stun=False, source_x=None):
        """受到傷害"""
        if not self.invincible and self.alive:
            self.health -= damage
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

            if knockback:
                self.apply_knockback(source_x)
            if stun:
                self.stunned = True
                self.stun_start_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.alive = False
                # 播放死亡音效（僅播放一次）
                if not self.death_sound_played:
                    try:
                        from systems.sound_manager import sound_manager

                        sound_manager.play_death_sound()
                        self.death_sound_played = True
                    except ImportError:
                        pass
            else:
                # 敵人受傷但未死亡，播放受傷音效
                try:
                    from systems.sound_manager import sound_manager

                    sound_manager.play_enemy_hurt_sound()
                except ImportError:
                    pass

    def apply_knockback(self, source_x=None):
        """應用擊退效果"""
        self.knockback = True
        self.knockback_start_time = pygame.time.get_ticks()

        if source_x is not None:
            # 根據攻擊源位置決定擊退方向
            enemy_center_x = self.x + self.width // 2
            if enemy_center_x < source_x:
                self.knockback_vel_x = -KNOCKBACK_FORCE  # 向左擊退
            else:
                self.knockback_vel_x = KNOCKBACK_FORCE  # 向右擊退
        else:
            # 如果沒有攻擊源位置，使用原始邏輯（遠離螢幕中心）
            center_x = WINDOW_WIDTH // 2
            enemy_center_x = self.x + self.width // 2
            if enemy_center_x < center_x:
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
        super().__init__(x, y, DUMMY_WIDTH, DUMMY_HEIGHT, health=DUMMY_HEALTH)
        self.color = GRAY

    def update(self, player):
        """更新訓練人偶（不主動攻擊）"""
        super().update(player)

        # 訓練人偶不會主動移動或跳躍，只會被動受擊

    def apply_knockback(self, source_x=None):
        """應用擊退效果 - 訓練人偶專用版本"""
        self.knockback = True
        self.knockback_start_time = pygame.time.get_ticks()

        if source_x is not None:
            # 根據攻擊源位置決定擊退方向
            enemy_center_x = self.x + self.width // 2
            if enemy_center_x < source_x:
                self.knockback_vel_x = -KNOCKBACK_FORCE  # 向左擊退（遠離攻擊源）
            else:
                self.knockback_vel_x = KNOCKBACK_FORCE  # 向右擊退（遠離攻擊源）
        else:
            # 如果沒有攻擊源位置，使用原始邏輯（遠離螢幕中心）
            center_x = WINDOW_WIDTH // 2
            enemy_center_x = self.x + self.width // 2
            if enemy_center_x < center_x:
                self.knockback_vel_x = -KNOCKBACK_FORCE
            else:
                self.knockback_vel_x = KNOCKBACK_FORCE

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

    def apply_knockback(self, source_x=None):
        """應用擊退效果"""
        self.charging = False  # 停止衝撞
        self.charge_cooldown = pygame.time.get_ticks() + 1500
        # 調用父類的擊退方法
        super().apply_knockback(source_x)

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


class EliteMech(Enemy):
    """精英機甲兵 - 新的中級敵人"""

    def __init__(self, x, y):
        super().__init__(
            x, y, ELITE_MECH_WIDTH, ELITE_MECH_HEIGHT, health=ELITE_MECH_HEALTH
        )
        self.color = (100, 150, 200)  # 藍色
        self.speed = ELITE_MECH_SPEED
        self.direction = 1
        self.attack_cooldown = 0
        self.shield_active = False
        self.shield_cooldown = 0
        self.shield_duration = 2000  # 護盾持續時間
        self.leap_attack_cooldown = 0
        self.jump_speed = ELITE_MECH_JUMP_SPEED
        self.double_jump_speed = ELITE_MECH_DOUBLE_JUMP_SPEED

    def update(self, player):
        """更新精英機甲兵"""
        current_time = pygame.time.get_ticks()
        super().update(player)

        if not self.stunned and not self.knockback:
            distance_to_player = abs(self.x - player.x)

            # 護盾技能
            if current_time > self.shield_cooldown and distance_to_player < 150:
                self.shield_active = True
                self.shield_cooldown = current_time + 8000  # 8秒冷卻

            # 護盾持續時間結束
            if self.shield_active and current_time > self.shield_cooldown - 6000:
                self.shield_active = False

            # 跳躍攻擊
            if (
                distance_to_player < 200
                and current_time > self.leap_attack_cooldown
                and self.can_jump_to_player(player)
            ):
                self.jump_towards_player(player)
                self.leap_attack_cooldown = current_time + 4000

            # 基本移動
            if distance_to_player > 80:
                if player.x > self.x:
                    self.x += self.speed
                    self.direction = 1
                else:
                    self.x -= self.speed
                    self.direction = -1

    def take_damage(self, damage=1, knockback=False, stun=False, source_x=None):
        """精英機甲兵受傷 - 護盾可以減少傷害"""
        if self.shield_active:
            damage = max(1, damage // 2)  # 護盾減少50%傷害
        super().take_damage(damage, knockback, stun, source_x)

    def draw(self, screen):
        """繪製精英機甲兵"""
        # 基本身體顏色
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW
        else:
            color = self.color

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 護盾效果
        if self.shield_active:
            shield_color = (0, 200, 255, 100)  # 半透明藍色
            pygame.draw.rect(
                screen,
                (0, 200, 255),
                (self.x - 5, self.y - 5, self.width + 10, self.height + 10),
                3,
            )

        # 機甲裝飾
        pygame.draw.rect(
            screen, (200, 200, 200), (self.x + 10, self.y + 10, self.width - 20, 15)
        )
        pygame.draw.circle(screen, RED, (int(self.x + 30), int(self.y + 15)), 4)


class MageRobot(Enemy):
    """法師機器人 - 2.5關敵人"""

    def __init__(self, x, y):
        super().__init__(
            x, y, MAGE_ROBOT_WIDTH, MAGE_ROBOT_HEIGHT, health=MAGE_ROBOT_HEALTH
        )
        self.color = (120, 50, 150)  # 紫色
        self.speed = MAGE_ROBOT_SPEED
        self.direction = 1
        self.attack_cooldown = 0
        self.bullets = []  # 追蹤子彈列表
        self.retreat_distance = 150  # 保持與玩家的距離
        self.attack_range = MAGE_ROBOT_ATTACK_RANGE

        # 跳躍系統屬性
        self.jump_speed = MAGE_ROBOT_JUMP_SPEED
        self.double_jump_speed = MAGE_ROBOT_DOUBLE_JUMP_SPEED
        self.jump_cooldown = 0
        self.last_jump_time = 0

        # 瞬移系統
        self.teleport_cooldown = 0
        self.last_teleport_time = 0
        self.teleporting = False
        self.teleport_charge_time = 0

    def update(self, player):
        """更新法師機器人"""
        current_time = pygame.time.get_ticks()
        super().update(player)

        if not self.stunned and not self.knockback:
            distance_to_player = abs(self.x - player.x)
            height_difference = self.y - player.y

            # 瞬移技能：危險時逃脫
            if (
                distance_to_player < 80  # 玩家太近
                and current_time > self.teleport_cooldown
                and self.platform_system is not None
            ):
                self._attempt_teleport(player)
                self.teleport_cooldown = current_time + MAGE_ROBOT_TELEPORT_COOLDOWN

            # 跳躍邏輯：主動追擊玩家到不同平台
            elif (
                current_time > self.jump_cooldown
                and current_time - self.last_jump_time > MAGE_ROBOT_JUMP_COOLDOWN
            ):
                # 如果玩家在不同高度的平台上，嘗試跳躍追擊
                if abs(height_difference) > 60 and distance_to_player < 300:
                    if self._try_jump_to_player(player):
                        self.jump_cooldown = current_time + 1000  # 短期冷卻避免連續跳躍
                        self.last_jump_time = current_time

            # 攻擊邏輯：在攻擊範圍內發射追蹤子彈
            if (
                distance_to_player <= self.attack_range
                and current_time > self.attack_cooldown
            ):
                self._tracking_shot_attack(player)
                self.attack_cooldown = current_time + MAGE_ROBOT_ATTACK_COOLDOWN

            # 移動邏輯：保持距離，遠離玩家
            if distance_to_player < self.retreat_distance:
                # 遠離玩家
                if player.x > self.x:
                    # 玩家在右邊，向左移動
                    new_x = self.x - self.speed
                    if new_x > 0:  # 不超出左邊界
                        self.x = new_x
                        self.direction = -1
                else:
                    # 玩家在左邊，向右移動
                    new_x = self.x + self.speed
                    if new_x < WINDOW_WIDTH - self.width:  # 不超出右邊界
                        self.x = new_x
                        self.direction = 1
            elif distance_to_player > self.attack_range + 50:
                # 距離太遠，適當靠近
                if player.x > self.x:
                    self.x += self.speed * 0.5
                    self.direction = 1
                else:
                    self.x -= self.speed * 0.5
                    self.direction = -1

        # 更新子彈
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)

    def _try_jump_to_player(self, player):
        """嘗試跳躍到玩家位置"""
        if not self.on_ground or self.stunned or self.knockback:
            return False

        # 檢查玩家位置是否需要跳躍
        height_difference = self.y - player.y
        horizontal_distance = abs(self.x - player.x)

        # 如果玩家在上方且距離合理
        if height_difference > 50 and horizontal_distance < 250:
            return self.jump_towards_player(player)

        # 如果玩家在下方，尋找合適的平台跳下去
        elif height_difference < -30 and horizontal_distance < 200:
            return self._jump_down_towards_player(player)

        return False

    def _jump_down_towards_player(self, player):
        """向下跳躍接近玩家"""
        if not self.on_ground:
            return False

        # 簡單的向前跳躍，依靠重力下落
        if player.x > self.x:
            self.vel_x = 3
            self.direction = 1
        else:
            self.vel_x = -3
            self.direction = -1

        # 小幅度跳躍以脫離當前平台
        self.vel_y = -8  # 較小的跳躍力度
        self.on_ground = False
        return True

    def _attempt_teleport(self, player):
        """嘗試瞬移到安全位置"""
        if self.platform_system is None:
            return False

        # 尋找最遠的平台進行瞬移
        best_platform = None
        max_distance = 0

        for platform in self.platform_system.platforms:
            platform_center_x = platform.x + platform.width // 2
            platform_center_y = platform.y

            # 計算到玩家的距離
            player_center_x = player.x + player.width // 2
            distance_to_player = abs(platform_center_x - player_center_x)

            # 選擇距離玩家最遠但在瞬移範圍內的平台
            distance_to_self = abs(platform_center_x - (self.x + self.width // 2))
            if (
                distance_to_player > max_distance
                and distance_to_self <= MAGE_ROBOT_TELEPORT_RANGE
                and platform_center_x >= 0
                and platform_center_x <= WINDOW_WIDTH - self.width
            ):

                max_distance = distance_to_player
                best_platform = platform

        # 執行瞬移
        if best_platform:
            self.x = best_platform.x + (best_platform.width - self.width) // 2
            self.y = best_platform.y - self.height
            self.vel_y = 0
            self.on_ground = True
            self.double_jump_available = True

            # 瞬移特效
            try:
                from ..systems.particle_system import particle_system

                teleport_x = self.x + self.width // 2
                teleport_y = self.y + self.height // 2
                particle_system.create_teleport_effect(teleport_x, teleport_y)
            except ImportError:
                pass  # 如果粒子系統不可用就跳過特效

            self.teleporting = True
            self.teleport_charge_time = pygame.time.get_ticks()

            return True

        return False

    def _tracking_shot_attack(self, player):
        """發射追蹤子彈攻擊"""
        # 從法師機器人中心發射追蹤子彈
        mage_center_x = self.x + self.width // 2
        mage_center_y = self.y + self.height // 2

        tracking_bullet = TrackingBullet(mage_center_x, mage_center_y, player)
        self.bullets.append(tracking_bullet)

    def draw(self, screen):
        """繪製法師機器人"""
        # 瞬移特效
        if (
            self.teleporting
            and pygame.time.get_ticks() - self.teleport_charge_time < 300
        ):
            # 閃爍效果表示剛瞬移
            if (pygame.time.get_ticks() // 50) % 2:
                alpha_surface = pygame.Surface((self.width, self.height))
                alpha_surface.set_alpha(128)
                alpha_surface.fill((255, 255, 255))
                screen.blit(alpha_surface, (self.x, self.y))
        else:
            self.teleporting = False

        # 根據狀態決定顏色
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW
        else:
            color = self.color

        # 繪製身體
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # 繪製法師帽子（三角形）
        hat_points = [
            (self.x + self.width // 2, self.y - 10),  # 帽子頂端
            (self.x + 5, self.y + 5),  # 左下
            (self.x + self.width - 5, self.y + 5),  # 右下
        ]
        pygame.draw.polygon(screen, (80, 30, 120), hat_points)

        # 繪製法師眼睛（發光效果）
        eye_color = (255, 100, 255) if not self.invincible else WHITE
        pygame.draw.circle(screen, eye_color, (int(self.x + 12), int(self.y + 20)), 4)
        pygame.draw.circle(
            screen, eye_color, (int(self.x + self.width - 12), int(self.y + 20)), 4
        )

        # 繪製法師杖（如果有空間）
        staff_x = self.x + (self.width // 2) + (10 if self.direction == 1 else -10)
        staff_y = self.y + 15
        pygame.draw.line(
            screen, (139, 69, 19), (staff_x, staff_y), (staff_x, staff_y + 25), 3
        )
        pygame.draw.circle(screen, (255, 215, 0), (staff_x, staff_y), 5)

        # 繪製瞬移充能效果
        current_time = pygame.time.get_ticks()
        if current_time < self.teleport_cooldown:
            cooldown_remaining = (
                self.teleport_cooldown - current_time
            ) / MAGE_ROBOT_TELEPORT_COOLDOWN
            if cooldown_remaining < 0.3:  # 冷卻即將結束時顯示充能效果
                charge_color = (100, 200, 255)
                pygame.draw.circle(
                    screen,
                    charge_color,
                    (int(self.x + self.width // 2), int(self.y + self.height // 2)),
                    int(15 * (1 - cooldown_remaining / 0.3)),
                    2,
                )

        # 繪製子彈
        for bullet in self.bullets:
            bullet.draw(screen)


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

        # 特殊攻擊視覺效果
        self.special_attack_active = False
        self.special_attack_start_time = 0
        self.special_attack_duration = 1000  # 視覺效果持續時間（毫秒）
        self.shockwave_rings = []  # 衝擊波環效果

        # 新的BOSS技能
        self.rage_mode = False
        self.missile_barrage_cooldown = 0
        self.laser_charge_time = 0
        self.laser_charging = False

    def update(self, player):
        """更新巨型機器人BOSS"""
        super().update(player)
        current_time = pygame.time.get_ticks()

        # 檢查是否進入狂暴模式
        if self.health / self.max_health <= 0.3 and not self.rage_mode:
            self.rage_mode = True
            self.speed *= 1.5  # 提升移動速度

        if not self.stunned and not self.knockback:
            # 計算與玩家的距離和高度差
            distance_to_player = abs(self.x - player.x)
            height_difference = self.y - player.y

            # 新增：導彈齊射攻擊（狂暴模式下）
            if (
                self.rage_mode
                and distance_to_player > 250
                and current_time > self.missile_barrage_cooldown
            ):
                self._missile_barrage_attack(player)
                self.missile_barrage_cooldown = current_time + 6000  # 6秒冷卻

            # 新增：雷射蓄力攻擊
            if (
                distance_to_player < 300
                and current_time > self.laser_charge_time + 8000
            ):
                if not self.laser_charging:
                    self.laser_charging = True
                    self.laser_charge_time = current_time
                elif current_time - self.laser_charge_time > 2000:  # 蓄力2秒
                    self._laser_beam_attack(player)
                    self.laser_charging = False
                    self.laser_charge_time = current_time

            # 優先處理平台跳躍邏輯 - BOSS現在能夠更積極地追逐玩家
            if current_time > self.jump_cooldown:
                jump_attempted = False

                # 檢查玩家是否在上方的平台上
                if height_difference > 30:  # 玩家在較高位置
                    # 嘗試直接跳向玩家（如果距離合理）
                    if distance_to_player < 200 and self.can_jump_to_player(player):
                        if self.jump_towards_player(player):
                            self.jump_cooldown = current_time + 3000  # 縮短冷卻到3秒
                            jump_attempted = True

                    # 如果直接跳躍不可行，尋找中間平台
                    elif distance_to_player < 350 and self.platform_system:
                        target_platform = self._find_path_to_player(player)
                        if target_platform and self.on_ground:
                            # 跳向中間平台
                            platform_center_x = (
                                target_platform.x + target_platform.width // 2
                            )
                            self._jump_to_position(platform_center_x, target_platform.y)
                            self.jump_cooldown = current_time + 2500  # 更短的冷卻
                            jump_attempted = True

                # 如果玩家在同一水平但距離較遠，也可以考慮跳躍靠近
                elif (
                    distance_to_player > 100
                    and distance_to_player < 250
                    and abs(height_difference) < 50
                ):
                    if self.on_ground and self.can_jump_to_player(player):
                        if self.jump_towards_player(player):
                            self.jump_cooldown = current_time + 3500  # 水平跳躍稍長冷卻
                            jump_attempted = True

            # 地面移動邏輯（如果沒有跳躍）
            if distance_to_player > 50:
                if player.x > self.x:
                    move_amount = self.speed
                    if not self.on_ground:
                        move_amount = min(self.vel_x + 1, 4)  # 空中移動加速
                    self.x += move_amount
                    self.direction = 1
                else:
                    move_amount = self.speed
                    if not self.on_ground:
                        move_amount = max(self.vel_x - 1, -4)  # 空中移動加速
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

        # 更新特殊攻擊視覺效果
        if self.special_attack_active:
            if (
                current_time - self.special_attack_start_time
                > self.special_attack_duration
            ):
                self.special_attack_active = False
                self.shockwave_rings.clear()
            else:
                # 更新衝擊波環效果並檢測碰撞
                player_center_x = player.x + player.width // 2
                player_center_y = player.y + player.height // 2

                for ring in self.shockwave_rings[:]:
                    ring["radius"] += ring["expand_speed"]
                    ring["alpha"] = max(0, ring["alpha"] - 3)  # 逐漸變透明

                    # 檢查衝擊波是否擊中玩家（只在第一次擊中時造成傷害）
                    if not ring["damage_dealt"]:
                        distance_to_player = math.sqrt(
                            (player_center_x - ring["x"]) ** 2
                            + (player_center_y - ring["y"]) ** 2
                        )

                        # 檢查玩家是否在衝擊波環的範圍內（環的厚度約為20像素）
                        if abs(distance_to_player - ring["radius"]) <= 20:
                            if not player.is_defending:
                                player.take_damage()
                            ring["damage_dealt"] = True  # 標記已造成傷害，避免重複傷害

                    if ring["alpha"] <= 0:
                        self.shockwave_rings.remove(ring)

    def _find_path_to_player(self, player):
        """尋找到達玩家位置的最佳平台路徑"""
        if not self.platform_system:
            return None

        # 獲取所有可能的中間平台
        current_x = self.x + self.width // 2
        current_y = self.y
        player_x = player.x + player.width // 2
        player_y = player.y

        best_platform = None
        min_total_distance = float("inf")

        for platform in self.platform_system.platforms:
            platform_center_x = platform.x + platform.width // 2
            platform_center_y = platform.y

            # 檢查平台是否在玩家和BOSS之間的合理位置
            if platform_center_y < current_y and platform_center_y > player_y - 50:
                # 計算到平台的距離
                distance_to_platform = abs(platform_center_x - current_x)
                # 計算從平台到玩家的距離
                distance_platform_to_player = abs(platform_center_x - player_x)

                # 總距離作為評估指標
                total_distance = distance_to_platform + distance_platform_to_player

                # 優先選擇水平距離合理且總距離最短的平台
                if (
                    distance_to_platform < 150
                    and distance_platform_to_player < 200
                    and total_distance < min_total_distance
                ):
                    min_total_distance = total_distance
                    best_platform = platform

        return best_platform

    def _jump_to_position(self, target_x, target_y):
        """跳躍到指定位置"""
        if not self.on_ground:
            return False

        # 計算跳躍方向
        direction_x = 1 if target_x > self.x else -1

        # 執行跳躍
        self.vel_y = -self.jump_speed
        self.on_ground = False
        self.double_jump_available = True

        # 添加水平移動力
        horizontal_force = min(abs(target_x - self.x) / 50, 3)  # 根據距離調整力度
        self.vel_x = direction_x * horizontal_force

        return True

    def can_jump_to_player(self, player):
        """判斷是否可以跳躍到玩家位置 - BOSS專用增強版"""
        if not self.on_ground or self.stunned or self.knockback:
            return False

        # BOSS的跳躍能力更強，放寬限制條件
        horizontal_distance = abs(player.x - self.x)
        height_difference = self.y - player.y

        # 如果玩家在上方且距離合理
        if height_difference > 20 and horizontal_distance < 250:  # 增加跳躍範圍
            return True

        # 如果玩家在同一水平但需要跳躍接近
        if (
            abs(height_difference) < 30
            and horizontal_distance > 80
            and horizontal_distance < 200
        ):
            return True

        return False

    def jump_towards_player(self, player):
        """朝玩家方向跳躍（包含二段跳）- BOSS專用增強版"""
        jump_speed = self.jump_speed
        double_jump_speed = self.double_jump_speed

        if self.on_ground:
            # 首次跳躍
            self.vel_y = -jump_speed
            self.on_ground = False
            self.double_jump_available = True

            # 增強水平移動力度
            horizontal_distance = abs(player.x - self.x)
            if horizontal_distance > 100:
                base_force = 3
            else:
                base_force = 2

            if player.x > self.x:
                self.vel_x = base_force
            else:
                self.vel_x = -base_force

        elif self.double_jump_available and not self.stunned and not self.knockback:
            # 二段跳 - BOSS在空中也能調整方向
            self.vel_y = -double_jump_speed
            self.double_jump_available = False

            # 空中方向調整
            if player.x > self.x:
                self.vel_x = min(self.vel_x + 2, 4)
            else:
                self.vel_x = max(self.vel_x - 2, -4)

        return True

    def _ranged_attack(self, player):
        """遠程攻擊：發射子彈"""
        # 從 BOSS 中心發射子彈朝向玩家
        boss_center_x = self.x + self.width // 2
        boss_center_y = self.y + self.height // 2
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2

        bullet = Bullet(boss_center_x, boss_center_y, player_center_x, player_center_y)
        self.bullets.append(bullet)

    def _missile_barrage_attack(self, player):
        """新攻擊：子彈齊射"""
        boss_center_x = self.x + self.width // 2
        boss_center_y = self.y + self.height // 2

        # 發射5發子彈，形成扇形攻擊
        import math

        for i in range(5):
            angle_offset = (i - 2) * 15  # -30, -15, 0, 15, 30 度
            angle_rad = math.radians(angle_offset)

            # 計算目標點（在玩家附近但有些分散）
            target_x = player.x + player.width // 2 + math.sin(angle_rad) * 100
            target_y = player.y + player.height // 2 + math.cos(angle_rad) * 50

            bullet = Bullet(boss_center_x, boss_center_y, target_x, target_y)
            self.bullets.append(bullet)

    def _laser_beam_attack(self, player):
        """新攻擊：雷射光束"""
        boss_center_x = self.x + self.width // 2
        boss_center_y = self.y + self.height // 2
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2

        laser = LaserBeam(
            boss_center_x, boss_center_y, player_center_x, player_center_y
        )
        self.bullets.append(laser)

    def _special_attack(self, player):
        """特殊攻擊技能 - 範圍攻擊"""
        # 啟動視覺效果
        self.special_attack_active = True
        self.special_attack_start_time = pygame.time.get_ticks()

        # 創建衝擊波環效果
        boss_center_x = self.x + self.width // 2
        boss_center_y = self.y + self.height // 2

        # 創建多個衝擊波環，不同大小和速度
        for i in range(3):
            ring = {
                "x": boss_center_x,
                "y": boss_center_y,
                "radius": 10 + i * 15,
                "expand_speed": 3 + i * 0.5,
                "alpha": 255 - i * 30,
                "color": (255, 100 + i * 50, 0),  # 橙紅色漸變
                "damage_dealt": False,  # 追蹤是否已造成傷害
            }
            self.shockwave_rings.append(ring)

    def apply_knockback(self, source_x=None):
        """BOSS受到擊退效果較小但仍會有效果"""
        self.knockback = True
        self.knockback_start_time = pygame.time.get_ticks()

        if source_x is not None:
            # 根據攻擊源位置決定擊退方向
            boss_center_x = self.x + self.width // 2
            if boss_center_x < source_x:
                self.knockback_vel_x = -KNOCKBACK_FORCE * 0.5  # 向左擊退，但力度減半
            else:
                self.knockback_vel_x = KNOCKBACK_FORCE * 0.5  # 向右擊退，但力度減半
        else:
            # 如果沒有攻擊源位置，使用原始邏輯
            center_x = WINDOW_WIDTH // 2
            boss_center_x = self.x + self.width // 2
            if boss_center_x < center_x:
                self.knockback_vel_x = -KNOCKBACK_FORCE * 0.5
            else:
                self.knockback_vel_x = KNOCKBACK_FORCE * 0.5

    def take_damage(self, damage=1, knockback=False, stun=False, source_x=None):
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
                self.apply_knockback(source_x)
            if stun:
                self.stunned = True
                self.stun_start_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.alive = False
                # 播放死亡音效（僅播放一次）
                if not self.death_sound_played:
                    try:
                        from systems.sound_manager import sound_manager

                        sound_manager.play_death_sound()
                        self.death_sound_played = True
                    except ImportError:
                        pass
            else:
                # BOSS 受傷但未死亡，播放受傷音效
                try:
                    from systems.sound_manager import sound_manager

                    sound_manager.play_enemy_hurt_sound()
                except ImportError:
                    pass

    def draw(self, screen):
        """繪製巨型機器人BOSS"""
        # 特殊攻擊時的螢幕震動效果
        shake_offset_x = 0
        shake_offset_y = 0
        if self.special_attack_active:
            import random

            shake_intensity = 5
            shake_offset_x = random.randint(-shake_intensity, shake_intensity)
            shake_offset_y = random.randint(-shake_intensity, shake_intensity)

        # 根據狀態決定顏色
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = WHITE
        elif self.stunned:
            color = YELLOW
        elif self.rage_mode:
            # 狂暴模式時身體發出暗紅光
            color = (200, 50, 50)
        elif self.laser_charging:
            # 雷射蓄力時發出藍光
            color = (100, 100, 255)
        elif self.special_attack_active:
            # 特殊攻擊時身體發紅光
            color = (255, 100, 100)
        else:
            color = self.color

        # 繪製身體（加入震動偏移）
        body_rect = (
            self.x + shake_offset_x,
            self.y + shake_offset_y,
            self.width,
            self.height,
        )
        pygame.draw.rect(screen, color, body_rect)

        # 繪製狂暴模式的能量光環
        if self.rage_mode:
            pygame.draw.rect(
                screen,
                (255, 0, 0, 100),
                (self.x - 3, self.y - 3, self.width + 6, self.height + 6),
                3,
            )

        # 繪製雷射蓄力效果
        if self.laser_charging:
            charge_progress = (pygame.time.get_ticks() - self.laser_charge_time) / 2000
            charge_size = int(20 * charge_progress)
            pygame.draw.circle(
                screen,
                (0, 255, 255),
                (int(self.x + self.width // 2), int(self.y + self.height // 2)),
                charge_size,
                3,
            )

        # 繪製威脅性的紅眼（加入震動偏移）
        eye_size = 6
        if self.special_attack_active:
            eye_size = 8  # 特殊攻擊時眼睛變大
            eye_color = (255, 255, 255)  # 變成白色發光
        elif self.rage_mode:
            eye_size = 7
            eye_color = (255, 100, 100)  # 狂暴模式橙紅色
        else:
            eye_color = RED

        pygame.draw.circle(
            screen,
            eye_color,
            (int(self.x + 20 + shake_offset_x), int(self.y + 20 + shake_offset_y)),
            eye_size,
        )
        pygame.draw.circle(
            screen,
            eye_color,
            (int(self.x + 60 + shake_offset_x), int(self.y + 20 + shake_offset_y)),
            eye_size,
        )

        # 繪製特殊攻擊的衝擊波效果
        if self.special_attack_active:
            self._draw_special_attack_effects(screen)

        # 繪製血量條
        self._draw_health_bar(screen)

        # 繪製子彈
        for bullet in self.bullets:
            bullet.draw(screen)

    def _draw_special_attack_effects(self, screen):
        """繪製特殊攻擊的視覺效果"""
        # 繪製衝擊波環
        for ring in self.shockwave_rings:
            if ring["alpha"] > 0:
                # 創建帶透明度的表面
                ring_surface = pygame.Surface((ring["radius"] * 2, ring["radius"] * 2))
                ring_surface.set_alpha(ring["alpha"])
                ring_surface.set_colorkey(BLACK)

                # 繪製環形（外圈和內圈）
                pygame.draw.circle(
                    ring_surface,
                    ring["color"],
                    (ring["radius"], ring["radius"]),
                    ring["radius"],
                    3,
                )

                # 繪製到螢幕上
                screen.blit(
                    ring_surface,
                    (ring["x"] - ring["radius"], ring["y"] - ring["radius"]),
                )

        # 繪製地面裂痕效果
        boss_center_x = self.x + self.width // 2
        ground_y = GROUND_Y

        # 從BOSS位置向外發射的裂痕線
        import random

        for i in range(8):
            angle = (i * 45) * math.pi / 180  # 每45度一條裂痕
            end_x = boss_center_x + math.cos(angle) * 150
            end_y = ground_y + math.sin(angle) * 30

            # 隨機抖動讓裂痕看起來更自然
            end_x += random.randint(-10, 10)
            end_y = min(end_y, ground_y + 20)  # 確保不超出地面太多

            pygame.draw.line(
                screen,
                (255, 150, 0),  # 橙色裂痕
                (boss_center_x, ground_y),
                (end_x, end_y),
                2,
            )

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
