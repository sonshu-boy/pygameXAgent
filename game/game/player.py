"""
玩家角色 - 老鼠
"""

import pygame
import math
from constants import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.double_jump_available = True  # 二段跳可用性
        self.health = 3  # 三顆愛心
        self.platform_system = None  # 將由GameLevel設定

        # 狀態
        self.is_defending = False
        self.defense_start_time = 0
        self.defense_cooldown_start = 0
        self.is_crouching = False
        self.is_sliding = False
        self.slide_start_time = 0
        self.slide_direction = 0

        # 無敵時間
        self.invincible = False
        self.invincible_start_time = 0

        # 拳頭
        self.left_fist = Fist(self, "left")
        self.right_fist = Fist(self, "right")

        # 輸入狀態
        self.keys = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()

    def handle_event(self, event):
        """處理單次事件（如跳躍）"""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_UP]:
                if self.on_ground:
                    # 首次跳躍
                    self.vel_y = -PLAYER_JUMP_SPEED
                    self.on_ground = False
                    self.double_jump_available = True
                elif self.double_jump_available:
                    # 二段跳
                    self.vel_y = -PLAYER_DOUBLE_JUMP_SPEED
                    self.double_jump_available = False

    def handle_input(self):
        """處理玩家輸入"""
        self.keys = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()

        # 移動輸入
        moving = False
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
            moving = True
        elif self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
            moving = True
        else:
            self.vel_x = 0

        # 跳躍輸入現在在 handle_event 中處理

        # 防禦輸入
        if self.keys[pygame.K_SPACE] and not self.is_defending:
            if current_time - self.defense_cooldown_start > DEFENSE_COOLDOWN:
                self.is_defending = True
                self.defense_start_time = current_time

        # 蹲下/滑行輸入
        if self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]:
            if moving and not self.is_sliding:
                # 開始滑行
                self.is_sliding = True
                self.slide_start_time = current_time
                self.slide_direction = 1 if self.vel_x > 0 else -1
                self.is_crouching = False
            elif not moving:
                # 蹲下
                self.is_crouching = True
                self.is_sliding = False
        else:
            self.is_crouching = False

        # 攻擊輸入
        mouse_pos = pygame.mouse.get_pos()
        is_air_attack = not self.on_ground  # 檢查是否為空中攻擊

        # 左鍵攻擊
        if self.mouse_buttons[0]:  # 左鍵按下
            if not self.left_fist.charging and not self.left_fist.is_attacking:
                self.left_fist.start_charging()
        else:  # 左鍵釋放
            if self.left_fist.charging:
                self.left_fist.release_attack(mouse_pos, is_air_attack)

        # 右鍵攻擊
        if self.mouse_buttons[2]:  # 右鍵按下
            if not self.right_fist.charging and not self.right_fist.is_attacking:
                self.right_fist.start_charging()
        else:  # 右鍵釋放
            if self.right_fist.charging:
                self.right_fist.release_attack(mouse_pos, is_air_attack)

    def update(self):
        """更新玩家狀態"""
        current_time = pygame.time.get_ticks()

        # 處理輸入
        self.handle_input()

        # 更新防禦狀態
        if self.is_defending:
            if current_time - self.defense_start_time > DEFENSE_DURATION:
                self.is_defending = False
                self.defense_cooldown_start = current_time

        # 更新滑行狀態
        if self.is_sliding:
            slide_duration = current_time - self.slide_start_time
            if slide_duration < 300:  # 滑行持續 300 毫秒
                self.vel_x = self.slide_direction * SLIDE_SPEED
            else:
                self.is_sliding = False

        # 更新無敵時間
        if self.invincible:
            if current_time - self.invincible_start_time > INVINCIBLE_DURATION:
                self.invincible = False

        # 應用重力
        if not self.on_ground:
            self.vel_y += GRAVITY

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

        # 檢查平台碰撞
        self._check_platform_collisions()

        # 地面碰撞檢測
        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True
            self.double_jump_available = True  # 重置二段跳

        # 螢幕邊界限制
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))

        # 更新拳頭
        self.left_fist.update()
        self.right_fist.update()

    def _check_platform_collisions(self):
        """檢查與平台的碰撞"""
        if self.platform_system is None:
            return

        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        platform, new_y = self.platform_system.check_collision(player_rect, self.vel_y)

        if platform is not None:
            self.y = new_y
            self.vel_y = 0
            self.on_ground = True
            self.double_jump_available = True  # 重置二段跳
        else:
            # 檢查是否仍在平台上
            if self.on_ground and self.vel_y >= 0:
                # 檢查是否還在地面或平台上
                on_platform = self.platform_system.is_on_platform(player_rect)
                on_ground = self.y + self.height >= GROUND_Y - 5

                if not on_platform and not on_ground:
                    self.on_ground = False

    def take_damage(self):
        """受到傷害"""
        if not self.invincible and not self.is_defending:
            self.health -= 1
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            return True
        return False

    def check_slide_attack(self, enemies):
        """檢查滑行攻擊碰撞"""
        if not self.is_sliding:
            return

        player_rect = self.get_rect()
        for enemy in enemies:
            if enemy.alive and player_rect.colliderect(enemy.get_rect()):
                # 滑行特殊攻擊：將敵人往上方擊飛
                enemy.take_damage(SLIDE_ATTACK_DAMAGE, knockback=True)

                # 特殊擊退效果：向上擊飛（無論是否無敵都生效）
                enemy.vel_y = -8  # 向上速度（從-15調整為-8）
                enemy.on_ground = False  # 確保敵人離開地面狀態，讓重力生效
                enemy.knockback_vel_x = self.slide_direction * SLIDE_ATTACK_KNOCKBACK
                enemy.knockback = True
                enemy.knockback_start_time = pygame.time.get_ticks()

    def get_rect(self):
        """獲取碰撞矩形"""
        height = (
            self.height // 2 if self.is_crouching or self.is_sliding else self.height
        )
        return pygame.Rect(self.x, self.y + (self.height - height), self.width, height)

    def draw(self, screen):
        """繪製玩家"""
        # 計算實際高度（蹲下時降低）
        actual_height = (
            self.height // 2 if self.is_crouching or self.is_sliding else self.height
        )
        actual_y = self.y + (self.height - actual_height)

        # 無敵時閃爍效果
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            color = (128, 128, 128)  # 灰色閃爍
        else:
            color = BROWN  # 老鼠顏色

        # 防禦時改變顏色
        if self.is_defending:
            color = BLUE

        # 繪製老鼠本體
        pygame.draw.rect(screen, color, (self.x, actual_y, self.width, actual_height))

        # 繪製眼睛
        eye_size = 5
        pygame.draw.circle(
            screen, BLACK, (int(self.x + 15), int(actual_y + 15)), eye_size
        )
        pygame.draw.circle(
            screen, BLACK, (int(self.x + 35), int(actual_y + 15)), eye_size
        )

        # 繪製拳頭
        self.left_fist.draw(screen)
        self.right_fist.draw(screen)


class Fist:
    def __init__(self, player, side):
        self.player = player
        self.side = side  # "left" 或 "right"
        self.x = 0
        self.y = 0
        self.size = FIST_SIZE
        self.is_attacking = False
        self.charging = False
        self.charge_start_time = 0
        self.attack_start_time = 0
        self.target_x = 0
        self.target_y = 0
        self.returning = False
        self.is_charged = False  # 是否為蓄力攻擊
        self.is_air_attack = False  # 是否為空中攻擊
        self.flash_time = 0  # 閃爍計時器

    def start_charging(self):
        """開始蓄力"""
        if not self.is_attacking and not self.charging:
            self.charging = True
            self.charge_start_time = pygame.time.get_ticks()

    def release_attack(self, mouse_pos, is_air_attack=False):
        """釋放攻擊"""
        if self.charging:
            current_time = pygame.time.get_ticks()
            charge_duration = current_time - self.charge_start_time

            # 設定目標位置（朝向滑鼠方向）
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2

            # 計算方向
            dx = mouse_pos[0] - player_center_x
            dy = mouse_pos[1] - player_center_y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                # 正規化方向向量
                dx /= distance
                dy /= distance

                # 檢查是否為蓄力攻擊
                if charge_duration >= CHARGE_TIME:
                    self.is_charged = True
                    self.size = FIST_CHARGED_SIZE
                    # 蓄力攻擊距離更遠
                    attack_distance = min(distance, FIST_CHARGED_MAX_DISTANCE)
                else:
                    self.is_charged = False
                    self.size = FIST_SIZE
                    # 限制攻擊距離
                    attack_distance = min(distance, FIST_MAX_DISTANCE)

                self.target_x = player_center_x + dx * attack_distance
                self.target_y = player_center_y + dy * attack_distance

                self.is_air_attack = is_air_attack
                self.is_attacking = True
                self.attack_start_time = current_time
                self.returning = False
                self.charging = False

    def start_attack(self, mouse_pos):
        """舊版本的立即攻擊（保持兼容性）"""
        if not self.is_attacking:
            current_time = pygame.time.get_ticks()

            # 設定目標位置（朝向滑鼠方向）
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2

            # 計算方向
            dx = mouse_pos[0] - player_center_x
            dy = mouse_pos[1] - player_center_y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                # 正規化方向向量
                dx /= distance
                dy /= distance

                # 限制攻擊距離
                attack_distance = min(distance, FIST_MAX_DISTANCE)

                self.target_x = player_center_x + dx * attack_distance
                self.target_y = player_center_y + dy * attack_distance

                self.is_attacking = True
                self.attack_start_time = current_time
                self.returning = False
                self.is_charged = False
                self.size = FIST_SIZE

    def update(self):
        """更新拳頭狀態"""
        current_time = pygame.time.get_ticks()

        if self.charging:
            # 蓄力中，拳頭跟隨玩家並變大/閃爍
            offset_x = -20 if self.side == "left" else 20
            self.x = self.player.x + self.player.width // 2 + offset_x
            self.y = self.player.y + self.player.height // 2

            charge_duration = current_time - self.charge_start_time
            if charge_duration >= CHARGE_TIME:
                # 達到完整蓄力時間，拳頭變大並閃爍
                self.size = FIST_CHARGED_SIZE
                self.flash_time = current_time
            else:
                # 蓄力中，拳頭逐漸變大
                charge_ratio = min(charge_duration / CHARGE_TIME, 1.0)
                self.size = FIST_SIZE + int(
                    (FIST_CHARGED_SIZE - FIST_SIZE) * charge_ratio
                )
            return

        if not self.is_attacking:
            # 拳頭跟隨玩家
            offset_x = -20 if self.side == "left" else 20
            self.x = self.player.x + self.player.width // 2 + offset_x
            self.y = self.player.y + self.player.height // 2
            return

        # 攻擊動畫
        if not self.returning:
            # 向目標移動
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            # 根據是否為蓄力攻擊選擇速度
            fist_speed = FIST_CHARGED_SPEED if self.is_charged else FIST_SPEED

            if distance > fist_speed:
                dx = (dx / distance) * fist_speed
                dy = (dy / distance) * fist_speed
                self.x += dx
                self.y += dy
            else:
                # 到達目標，開始返回
                self.returning = True
        else:
            # 返回玩家身邊
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2

            dx = player_center_x - self.x
            dy = player_center_y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > FIST_RETURN_SPEED:
                dx = (dx / distance) * FIST_RETURN_SPEED
                dy = (dy / distance) * FIST_RETURN_SPEED
                self.x += dx
                self.y += dy
            else:
                # 返回完成
                self.is_attacking = False
                self.is_charged = False
                self.size = FIST_SIZE

    def get_rect(self):
        """獲取拳頭碰撞矩形"""
        return pygame.Rect(
            self.x - self.size // 2, self.y - self.size // 2, self.size, self.size
        )

    def draw(self, screen):
        """繪製拳頭"""
        current_time = pygame.time.get_ticks()

        if self.charging:
            charge_duration = current_time - self.charge_start_time
            if charge_duration >= CHARGE_TIME:
                # 完全蓄力時閃爍效果
                if (current_time // 100) % 2:  # 每100毫秒閃爍一次
                    color = WHITE
                else:
                    color = RED
            else:
                # 蓄力中，顏色從黃色漸變到紅色
                charge_ratio = charge_duration / CHARGE_TIME
                red_component = int(255 * charge_ratio)
                yellow_component = int(255 * (1 - charge_ratio))
                color = (255, yellow_component, 0)
        else:
            color = RED if self.is_charged else YELLOW

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size // 2)
