"""
粒子特效系統
提供各種視覺特效，包括粒子爆炸、光環、連擊特效、擊中特效等
"""

import pygame
import math
import random
import sys
import os

# 添加 src 目錄到 path 以便導入 constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import *


class Particle:
    """單個粒子類別"""

    def __init__(self, x, y, vel_x, vel_y, color, size, lifetime, gravity=0):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = gravity
        self.alive = True

    def update(self):
        """更新粒子狀態"""
        if not self.alive:
            return

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity

        # 更新生命值
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen):
        """繪製粒子"""
        if not self.alive:
            return

        # 根據剩餘生命值調整透明度
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))

        # 創建帶透明度的表面
        particle_surface = pygame.Surface((self.size * 2, self.size * 2))
        particle_surface.set_alpha(alpha)
        particle_surface.set_colorkey(BLACK)

        # 繪製粒子
        pygame.draw.circle(
            particle_surface, self.color, (self.size, self.size), self.size
        )

        screen.blit(particle_surface, (self.x - self.size, self.y - self.size))


class EffectRing:
    """光環特效類別"""

    def __init__(self, x, y, max_radius, color, width=3, lifetime=60, pulse=False):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = max_radius
        self.color = color
        self.width = width
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alive = True
        self.pulse = pulse

    def update(self):
        """更新光環狀態"""
        if not self.alive:
            return

        # 光環擴張
        self.radius = (1 - self.lifetime / self.max_lifetime) * self.max_radius

        # 脈衝效果
        if self.pulse:
            pulse_factor = 1 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
            self.radius *= pulse_factor

        # 更新生命值
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen):
        """繪製光環"""
        if not self.alive or self.radius <= 0:
            return

        # 根據剩餘生命值調整透明度
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))

        # 創建帶透明度的表面
        ring_size = int(self.radius * 2 + self.width * 2)
        ring_surface = pygame.Surface((ring_size, ring_size))
        ring_surface.set_alpha(alpha)
        ring_surface.set_colorkey(BLACK)

        # 繪製光環
        pygame.draw.circle(
            ring_surface,
            self.color,
            (ring_size // 2, ring_size // 2),
            int(self.radius),
            self.width,
        )

        screen.blit(ring_surface, (self.x - ring_size // 2, self.y - ring_size // 2))


class TextEffect:
    """文字特效類別"""

    def __init__(self, x, y, text, color, font_size=24, vel_y=-2, lifetime=90):
        self.x = x
        self.y = y
        self.initial_y = y
        self.text = text
        self.color = color
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alive = True

        # 創建字體
        try:
            from systems.font_manager import get_font

            self.font = get_font("small")
        except:
            self.font = pygame.font.Font(None, font_size)

    def update(self):
        """更新文字特效"""
        if not self.alive:
            return

        # 向上浮動
        self.y += self.vel_y

        # 更新生命值
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen):
        """繪製文字特效"""
        if not self.alive:
            return

        # 根據剩餘生命值調整透明度
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))

        # 渲染文字
        text_surface = self.font.render(self.text, True, self.color)

        # 創建帶透明度的表面
        alpha_surface = pygame.Surface(text_surface.get_size())
        alpha_surface.set_alpha(alpha)
        alpha_surface.blit(text_surface, (0, 0))

        # 繪製到螢幕
        text_rect = alpha_surface.get_rect(center=(self.x, self.y))
        screen.blit(alpha_surface, text_rect)


class ParticleSystem:
    """粒子特效系統管理器"""

    def __init__(self):
        self.particles = []
        self.rings = []
        self.text_effects = []

    def add_particle(self, particle):
        """添加粒子"""
        self.particles.append(particle)

    def add_ring(self, ring):
        """添加光環特效"""
        self.rings.append(ring)

    def add_text_effect(self, text_effect):
        """添加文字特效"""
        self.text_effects.append(text_effect)

    def create_explosion(self, x, y, color=YELLOW, particle_count=15):
        """創建爆炸特效"""
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            size = random.randint(2, 5)
            lifetime = random.randint(30, 60)

            particle = Particle(x, y, vel_x, vel_y, color, size, lifetime, gravity=0.1)
            self.add_particle(particle)

    def create_hit_effect(self, x, y, is_charged=False):
        """創建擊中特效"""
        if is_charged:
            # 蓄力攻擊特效
            self.create_explosion(x, y, RED, 20)
            ring = EffectRing(x, y, 60, WHITE, 4, 45)
            self.add_ring(ring)
        else:
            # 普通攻擊特效
            self.create_explosion(x, y, YELLOW, 10)

    def create_combo_effect(self, x, y, combo_count):
        """創建連擊特效"""
        # 連擊數字顯示
        text_color = YELLOW if combo_count < 5 else RED
        text_effect = TextEffect(x, y, f"{combo_count} HIT!", text_color, vel_y=-3)
        self.add_text_effect(text_effect)

        # 連擊光環
        ring_color = YELLOW if combo_count < 5 else RED
        ring = EffectRing(x, y, 40 + combo_count * 5, ring_color, 2, 30, pulse=True)
        self.add_ring(ring)

    def create_damage_text(self, x, y, damage, is_critical=False):
        """創建傷害數字特效"""
        color = RED if is_critical else WHITE
        text = f"-{damage}"
        if is_critical:
            text += "!"

        text_effect = TextEffect(x, y, text, color, vel_y=-2)
        self.add_text_effect(text_effect)

    def create_heal_effect(self, x, y, heal_amount):
        """創建治療特效"""
        # 治療數字
        text_effect = TextEffect(x, y, f"+{heal_amount}", GREEN, vel_y=-1)
        self.add_text_effect(text_effect)

        # 治療光環
        ring = EffectRing(x, y, 30, GREEN, 2, 40, pulse=True)
        self.add_ring(ring)

        # 治療粒子
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed - 1  # 向上飄散

            particle = Particle(x, y, vel_x, vel_y, GREEN, 3, 45, gravity=-0.02)
            self.add_particle(particle)

    def create_defense_effect(self, x, y):
        """創建防禦特效"""
        # 防禦光環
        ring = EffectRing(x, y, 50, BLUE, 3, 60, pulse=True)
        self.add_ring(ring)

        # 防禦粒子
        for _ in range(6):
            angle = random.uniform(0, 2 * math.pi)
            orbit_radius = 40
            orbit_x = x + math.cos(angle) * orbit_radius
            orbit_y = y + math.sin(angle) * orbit_radius

            particle = Particle(orbit_x, orbit_y, 0, 0, BLUE, 4, 30)
            self.add_particle(particle)

    def create_clear_screen_effect(self, x, y):
        """創建清屏技能特效 - 從玩家中心向外擴散的強大衝擊波"""
        # 第一階段：快速的內層光環（從玩家身邊開始）
        for i in range(3):
            max_radius = 80 + i * 60  # 較小但快速的光環
            lifetime = 40 - i * 5  # 快速擴散
            ring = EffectRing(x, y, max_radius, (255, 255, 255), 8, lifetime)
            self.add_ring(ring)

        # 第二階段：大範圍衝擊波光環
        for i in range(4):
            max_radius = 120 + i * 80  # 更大的範圍
            lifetime = 80 - i * 8  # 稍慢的擴散
            ring = EffectRing(x, y, max_radius, (200, 255, 255), 6 + i * 2, lifetime)
            self.add_ring(ring)

        # 第三階段：能量脈衝光環（最外層）
        for i in range(2):
            max_radius = 200 + i * 100  # 最大範圍
            lifetime = 100 - i * 10  # 最慢但範圍最大
            ring = EffectRing(x, y, max_radius, (255, 255, 150), 4 + i * 3, lifetime)
            self.add_ring(ring)

        # 從玩家中心向各個方向發射的能量粒子（第一波：快速擴散）
        for _ in range(60):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(12, 25)  # 更快的初始擴散速度
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed

            # 明亮的白色和黃色粒子
            color = random.choice([(255, 255, 255), (255, 255, 150), (255, 255, 200)])
            size = random.randint(4, 8)
            lifetime = random.randint(60, 120)

            particle = Particle(x, y, vel_x, vel_y, color, size, lifetime, gravity=0.05)
            self.add_particle(particle)

        # 第二波：較慢但持久的能量粒子
        for _ in range(40):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(6, 15)  # 較慢的速度
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed

            # 彩色的能量粒子
            color = random.choice([(200, 255, 255), (255, 200, 255), (255, 255, 100)])
            size = random.randint(3, 6)
            lifetime = random.randint(100, 180)

            particle = Particle(x, y, vel_x, vel_y, color, size, lifetime, gravity=0.02)
            self.add_particle(particle)

        # 玩家周圍的內層強化粒子（表現能量聚集和爆發）
        for _ in range(25):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 40)  # 在玩家附近生成
            start_x = x + math.cos(angle) * distance
            start_y = y + math.sin(angle) * distance

            # 向外爆發的速度
            speed = random.uniform(8, 18)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed

            color = random.choice([(255, 255, 255), (255, 255, 0), (255, 200, 100)])
            size = random.randint(6, 12)
            lifetime = random.randint(80, 140)

            particle = Particle(
                start_x, start_y, vel_x, vel_y, color, size, lifetime, gravity=0.1
            )
            self.add_particle(particle)
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(5, 25)  # 在玩家周圍小範圍
            start_x = x + math.cos(angle) * radius
            start_y = y + math.sin(angle) * radius

            # 向外擴散的速度
            speed = random.uniform(12, 25)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed

            color = (255, 255, 255)  # 純白色內層粒子
            size = random.randint(6, 12)
            lifetime = random.randint(60, 100)

            particle = Particle(
                start_x, start_y, vel_x, vel_y, color, size, lifetime, gravity=0
            )
            self.add_particle(particle)

        # 清屏文字特效增強
        text_effect = TextEffect(
            x, y - 60, "清屏!", (255, 255, 100), vel_y=-3, lifetime=150
        )
        self.add_text_effect(text_effect)

        # 添加副標題文字
        text_effect2 = TextEffect(
            x, y - 30, "衝擊波!", (255, 200, 200), vel_y=-1, lifetime=120
        )
        self.add_text_effect(text_effect2)

    def create_level_complete_effect(self, x, y):
        """創建關卡完成特效"""
        # 勝利文字
        text_effect = TextEffect(x, y, "關卡完成!", YELLOW, vel_y=0, lifetime=180)
        self.add_text_effect(text_effect)

        # 慶祝粒子
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed - 5  # 向上噴射
            color = random.choice([YELLOW, GREEN, BLUE, RED])
            size = random.randint(2, 6)

            particle = Particle(x, y, vel_x, vel_y, color, size, 90, gravity=0.2)
            self.add_particle(particle)

    def create_teleport_effect(self, x, y):
        """創建瞬移特效（法師機器人用）"""
        # 瞬移光環
        ring = EffectRing(x, y, 60, (150, 0, 255), 4, 30)
        self.add_ring(ring)

        # 瞬移粒子
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed

            particle = Particle(x, y, vel_x, vel_y, (255, 100, 255), 4, 40, gravity=0)
            self.add_particle(particle)

    def update(self):
        """更新所有特效"""
        # 更新粒子
        self.particles = [p for p in self.particles if p.alive]
        for particle in self.particles:
            particle.update()

        # 更新光環
        self.rings = [r for r in self.rings if r.alive]
        for ring in self.rings:
            ring.update()

        # 更新文字特效
        self.text_effects = [t for t in self.text_effects if t.alive]
        for text_effect in self.text_effects:
            text_effect.update()

    def draw(self, screen):
        """繪製所有特效"""
        # 先繪製光環（背景層）
        for ring in self.rings:
            ring.draw(screen)

        # 繪製粒子（中間層）
        for particle in self.particles:
            particle.draw(screen)

        # 繪製文字特效（前景層）
        for text_effect in self.text_effects:
            text_effect.draw(screen)

    def clear_all(self):
        """清除所有特效"""
        self.particles.clear()
        self.rings.clear()
        self.text_effects.clear()

    def get_effect_count(self):
        """獲取當前特效總數"""
        return len(self.particles) + len(self.rings) + len(self.text_effects)


# 全域粒子系統實例
particle_system = ParticleSystem()
