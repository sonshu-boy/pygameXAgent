"""
玩家角色類別定義
"""

import pygame
from config.settings import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.attack_power = ATTACK_DAMAGE
        self.facing_right = True
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_charge = 0
        self.max_attack_charge = 60
        self.is_defending = False
        self.slide_timer = 0
        self.slide_cooldown = 0
        self.cheese_count = 0
        self.jump_hold_timer = 0
        self.max_jump_hold = PLAYER_MAX_JUMP_HOLD
        self.jump_count = 0
        self.max_jumps = PLAYER_MAX_JUMPS
        self.coyote_time = 0
        self.max_coyote_time = PLAYER_MAX_COYOTE_TIME

    def update(self, platforms, enemies):
        """更新玩家狀態"""
        # 重力
        if not self.on_ground:
            self.vel_y += GRAVITY

        # 限制下降速度
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

        # 攻擊計時器
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False

        # 滑行計時器
        if self.slide_timer > 0:
            self.slide_timer -= 1

        if self.slide_cooldown > 0:
            self.slide_cooldown -= 1

        # 跳躍蓄力計時器
        if self.jump_hold_timer > 0:
            self.jump_hold_timer -= 1

        # 土狼時間（離開平台後的短暫跳躍窗口）
        if self.on_ground:
            self.jump_count = 0
            self.coyote_time = self.max_coyote_time
        else:
            if self.coyote_time > 0:
                self.coyote_time -= 1

        # 碰撞檢測
        self.check_platform_collision(platforms)
        self.check_enemy_collision(enemies)

        # 邊界檢查
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width

    def check_platform_collision(self, platforms):
        """檢查與平台的碰撞"""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on_ground = False

        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # 從上方落下 - 更精確的碰撞檢測
                if self.vel_y > 0 and self.y < platform.rect.top - 5:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # 從下方撞上
                elif self.vel_y < 0 and self.y > platform.rect.bottom:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
                # 從左側撞上
                elif self.vel_x > 0 and self.x < platform.rect.left - 5:
                    self.x = platform.rect.left - self.width
                    self.vel_x = 0
                # 從右側撞上
                elif self.vel_x < 0 and self.x > platform.rect.right:
                    self.x = platform.rect.right
                    self.vel_x = 0

    def check_enemy_collision(self, enemies):
        """檢查與敵人的碰撞"""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()) and enemy.health > 0:
                if not self.is_defending:
                    self.take_damage(10)

    def jump(self):
        """跳躍功能 - 支援連續跳躍"""
        # 允許連續跳躍：在地面上、土狼時間內、或還有空中跳躍次數
        can_jump = (self.on_ground or 
                   self.coyote_time > 0 or 
                   self.jump_count < self.max_jumps)
        
        if can_jump:
            if self.on_ground or self.coyote_time > 0:
                # 地面跳躍或土狼跳躍
                self.vel_y = JUMP_STRENGTH
                self.jump_count = 1
                self.coyote_time = 0
            else:
                # 空中跳躍
                self.vel_y = JUMP_STRENGTH * 0.8  # 空中跳躍稍弱一些
                self.jump_count += 1
            
            self.on_ground = False
            self.jump_hold_timer = self.max_jump_hold

    def continue_jump(self):
        """變長跳躍 - 按住空白鍵可以跳得更高"""
        if self.jump_hold_timer > 0 and self.vel_y < 0:
            self.vel_y += -0.3  # 額外的上升力

    def move_left(self, running=False):
        """向左移動"""
        speed = PLAYER_RUN_SPEED if running else PLAYER_SPEED
        self.vel_x = -speed
        self.facing_right = False

    def move_right(self, running=False):
        """向右移動"""
        speed = PLAYER_RUN_SPEED if running else PLAYER_SPEED
        self.vel_x = speed
        self.facing_right = True

    def stop_moving(self):
        """停止水平移動"""
        self.vel_x = 0

    def slide(self):
        """滑行"""
        if self.slide_cooldown <= 0 and self.on_ground:
            self.slide_timer = 20
            self.slide_cooldown = 60
            slide_speed = 12 if self.facing_right else -12
            self.vel_x = slide_speed

    def attack(self, enemies, charge_time=0):
        """攻擊功能"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 30

            # 計算攻擊範圍
            attack_width = 60 if charge_time >= self.max_attack_charge else 40
            attack_height = 40
            attack_x = (
                self.x + self.width if self.facing_right else self.x - attack_width
            )
            attack_y = self.y

            attack_rect = pygame.Rect(attack_x, attack_y, attack_width, attack_height)

            # 傷害計算
            damage = self.attack_power
            if charge_time >= self.max_attack_charge:
                damage *= 2  # 蓄力攻擊雙倍傷害

            # 攻擊敵人
            for enemy in enemies:
                if attack_rect.colliderect(enemy.get_rect()):
                    enemy.take_damage(damage)

    def take_damage(self, damage):
        """受到傷害"""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """恢復生命值"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def collect_cheese(self):
        """收集起司"""
        self.cheese_count += 1
        self.heal(CHEESE_HEAL)

    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_offset_y=0):
        """繪製玩家"""
        draw_y = self.y + camera_offset_y
        
        # 玩家身體（老鼠）
        color = PINK if self.slide_timer > 0 else GRAY
        pygame.draw.rect(surface, color, (self.x, draw_y, self.width, self.height))

        # 老鼠耳朵
        ear_size = 8
        if self.facing_right:
            pygame.draw.circle(surface, color, (self.x + 5, draw_y + 5), ear_size)
            pygame.draw.circle(surface, color, (self.x + 15, draw_y + 5), ear_size)
        else:
            pygame.draw.circle(
                surface, color, (self.x + self.width - 15, draw_y + 5), ear_size
            )
            pygame.draw.circle(
                surface, color, (self.x + self.width - 5, draw_y + 5), ear_size
            )

        # 老鼠眼睛
        eye_color = RED if self.health < 30 else BLACK
        if self.facing_right:
            pygame.draw.circle(surface, eye_color, (self.x + 8, draw_y + 12), 3)
            pygame.draw.circle(surface, eye_color, (self.x + 18, draw_y + 12), 3)
        else:
            pygame.draw.circle(
                surface, eye_color, (self.x + self.width - 18, draw_y + 12), 3
            )
            pygame.draw.circle(
                surface, eye_color, (self.x + self.width - 8, draw_y + 12), 3
            )

        # 攻擊效果
        if self.is_attacking:
            attack_width = 40
            attack_height = 40
            attack_x = (
                self.x + self.width if self.facing_right else self.x - attack_width
            )
            attack_y = draw_y
            pygame.draw.rect(
                surface, YELLOW, (attack_x, attack_y, attack_width, attack_height), 3
            )

        # 防禦效果
        if self.is_defending:
            pygame.draw.circle(
                surface,
                BLUE,
                (self.x + self.width // 2, draw_y + self.height // 2),
                max(self.width, self.height) // 2 + 5,
                3,
            )
