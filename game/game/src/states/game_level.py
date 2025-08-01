"""
遊戲關卡系統
"""

import pygame
import math
import random
from constants import *
from entities.player import Player
from entities.enemies import TrainingDummy, SmallRobot, GiantRobot, EliteMech, MageRobot
from entities.items import HealthItemSpawner
from systems.platform_system import PlatformSystem
from systems.font_manager import get_font
from systems.save_system import save_system
from systems.particle_system import particle_system
from systems.sound_manager import sound_manager


class GameLevel:
    def __init__(self, state_manager, level_number):
        self.state_manager = state_manager
        self.level_number = level_number
        self.player = Player(100, GROUND_Y - PLAYER_HEIGHT)
        self.enemies = []
        self.level_complete = False
        self.game_over = False
        self.death_sound_played = False  # 防止死亡音效重複播放

        # 計時系統
        self.start_time = pygame.time.get_ticks()
        self.completion_time = None
        self.level_completed_saved = False  # 確保只保存一次

        # 平台系統
        self.platform_system = PlatformSystem()
        self.player.platform_system = self.platform_system

        # UI 字體 - 使用支援中文的字體
        self.font_large = get_font("large")
        self.font_medium = get_font("medium")
        self.font_small = get_font("small")

        # 血量道具生成器
        self.health_item_spawner = HealthItemSpawner()

        # 關卡設定
        self._setup_level()

    def _setup_level(self):
        """設定關卡內容"""
        if self.level_number == LEVEL_1:
            # 第一關：訓練場
            self.level_name = "第一關：訓練場"
            self.background_color = (50, 100, 50)  # 綠色

            # 添加敵人
            enemy = TrainingDummy(500, GROUND_Y - DUMMY_HEIGHT)
            enemy.platform_system = self.platform_system
            self.enemies.append(enemy)

            # 添加簡單的平台
            self.platform_system.add_platform(300, GROUND_Y - 120, 150, 20)
            self.platform_system.add_platform(600, GROUND_Y - 160, 120, 20)

        elif self.level_number == LEVEL_2:
            # 第二關：工廠
            self.level_name = "第二關：工廠"
            self.background_color = (100, 100, 100)  # 灰色

            # 添加混合敵人類型
            # 2個小機器人
            for i in range(2):
                enemy = SmallRobot(400 + i * 180, GROUND_Y - SMALL_ROBOT_HEIGHT)
                enemy.platform_system = self.platform_system
                self.enemies.append(enemy)

            # 1個精英機甲兵
            elite_enemy = EliteMech(650, GROUND_Y - 70)
            elite_enemy.platform_system = self.platform_system
            self.enemies.append(elite_enemy)

            # 添加更多平台，創造更複雜的戰鬥環境
            self.platform_system.add_platform(200, GROUND_Y - 100, 100, 20)
            self.platform_system.add_platform(450, GROUND_Y - 180, 120, 20)
            self.platform_system.add_platform(700, GROUND_Y - 140, 100, 20)
            self.platform_system.add_platform(350, GROUND_Y - 260, 80, 20)

        elif self.level_number == LEVEL_2_5:
            # 第2.5關：廢棄工廠（隱藏關卡）
            self.level_name = "第2.5關：廢棄工廠"
            self.background_color = (60, 40, 30)  # 深棕色

            # 複雜的平台佈局，適合躲避和跳躍
            # 低層平台
            self.platform_system.add_platform(100, GROUND_Y - 80, 120, 20)
            self.platform_system.add_platform(300, GROUND_Y - 60, 100, 20)
            self.platform_system.add_platform(500, GROUND_Y - 90, 130, 20)
            self.platform_system.add_platform(700, GROUND_Y - 70, 110, 20)

            # 中層平台
            self.platform_system.add_platform(150, GROUND_Y - 160, 140, 20)
            self.platform_system.add_platform(400, GROUND_Y - 180, 120, 20)
            self.platform_system.add_platform(650, GROUND_Y - 150, 100, 20)

            # 高層平台
            self.platform_system.add_platform(80, GROUND_Y - 240, 100, 20)
            self.platform_system.add_platform(250, GROUND_Y - 280, 150, 20)
            self.platform_system.add_platform(450, GROUND_Y - 260, 120, 20)
            self.platform_system.add_platform(600, GROUND_Y - 220, 140, 20)

            # 頂層平台（法師生成位置）
            top_platform = self.platform_system.add_platform(
                350, GROUND_Y - 350, 100, 20
            )

            # 添加法師機器人敵人 - 生成在最高平台上
            for i in range(2):
                if i == 0:
                    # 第一個法師生成在頂層平台上
                    mage_x = (
                        top_platform.x + (top_platform.width - MAGE_ROBOT_WIDTH) // 2
                    )
                    mage_y = top_platform.y - MAGE_ROBOT_HEIGHT
                else:
                    # 第二個法師生成在第二高的平台上
                    second_high_platform_y = GROUND_Y - 280
                    mage_x = (
                        250 + (150 - MAGE_ROBOT_WIDTH) // 2
                    )  # 在250寬度150的平台中央
                    mage_y = second_high_platform_y - MAGE_ROBOT_HEIGHT

                mage = MageRobot(mage_x, mage_y)
                mage.platform_system = self.platform_system
                self.enemies.append(mage)

        elif self.level_number == LEVEL_3:
            # 第三關：實驗室（BOSS）
            self.level_name = "第三關：實驗室 - BOSS戰"
            self.background_color = (80, 50, 100)  # 紫色

            # 添加BOSS
            boss = GiantRobot(600, GROUND_Y - BOSS_HEIGHT)
            boss.platform_system = self.platform_system
            self.enemies.append(boss)

            # BOSS戰場地，增加更多平台提供豐富的戰術走位選擇
            # 左側低平台
            self.platform_system.add_platform(50, GROUND_Y - 100, 150, 25)
            # 中央中等高度平台
            self.platform_system.add_platform(250, GROUND_Y - 160, 200, 25)
            # 右側中等高度平台
            self.platform_system.add_platform(550, GROUND_Y - 140, 180, 25)
            # 左側高平台
            self.platform_system.add_platform(80, GROUND_Y - 250, 140, 25)
            # 中央高平台
            self.platform_system.add_platform(350, GROUND_Y - 280, 160, 25)
            # 右側高平台
            self.platform_system.add_platform(650, GROUND_Y - 220, 150, 25)
            # 頂部極高平台（逃生用）
            self.platform_system.add_platform(400, GROUND_Y - 350, 120, 25)
            # 左右兩側小跳台
            self.platform_system.add_platform(150, GROUND_Y - 320, 80, 20)
            self.platform_system.add_platform(780, GROUND_Y - 300, 80, 20)

    def handle_event(self, event):
        """處理關卡事件"""
        # 將事件傳遞給玩家
        if self.player:
            self.player.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # 返回主選單時恢復背景音樂音量
                sound_manager.restore_bgm_volume()
                self.state_manager.return_to_menu()
            elif event.key == pygame.K_q:
                # 處理Q鍵：反擊或清屏技能
                if self.player.counter_attack_ready:
                    if self.player.try_counter_attack(self.enemies):
                        # 反擊成功，添加視覺效果
                        player_center_x = self.player.x + self.player.width // 2
                        player_center_y = self.player.y + self.player.height // 2
                        particle_system.create_defense_effect(
                            player_center_x, player_center_y
                        )
                elif self.player.clear_screen_available:
                    # 執行清屏技能
                    if self.player.activate_clear_screen_skill():
                        self._execute_clear_screen_skill()
            elif event.key == pygame.K_r and (self.game_over or self.level_complete):
                # 重新開始關卡
                self.__init__(self.state_manager, self.level_number)
            elif event.key == pygame.K_RETURN and self.level_complete:
                # 進入下一關
                if self.level_number == LEVEL_2:
                    # 檢查是否滿血進入2.5關
                    if self.player.health == 3:
                        self.state_manager.start_level(LEVEL_2_5)
                    else:
                        self.state_manager.start_level(LEVEL_3)
                elif self.level_number == LEVEL_2_5:
                    self.state_manager.start_level(LEVEL_3)
                elif self.level_number < LEVEL_3:
                    self.state_manager.start_level(self.level_number + 1)
                else:
                    # 遊戲完成，返回關卡選擇時恢復背景音樂音量
                    sound_manager.restore_bgm_volume()
                    self.state_manager.change_state(LEVEL_SELECT_STATE)
            elif event.key == pygame.K_TAB and self.level_complete:
                # 返回關卡選擇時恢復背景音樂音量
                sound_manager.restore_bgm_volume()
                self.state_manager.change_state(LEVEL_SELECT_STATE)

    def update(self):
        """更新關卡邏輯"""
        if self.game_over or self.level_complete:
            # 即使遊戲結束也要更新粒子系統
            particle_system.update()
            return

        # 更新粒子系統
        particle_system.update()

        # 更新玩家
        self.player.update()

        # 更新血量道具系統
        self.health_item_spawner.update(self.platform_system)

        # 檢查道具拾取
        self.health_item_spawner.check_collection(self.player)

        # 檢查玩家生命值
        if self.player.health <= 0:
            if not self.game_over:  # 只在第一次死亡時觸發
                self.game_over = True
                # 播放玩家死亡音效
                if not self.death_sound_played:
                    try:
                        from systems.sound_manager import sound_manager

                        sound_manager.play_death_sound()
                        self.death_sound_played = True
                    except ImportError:
                        pass
            return

        # 更新敵人
        for enemy in self.enemies[:]:  # 使用切片複製列表避免修改時出錯
            if enemy.alive:
                enemy.update(self.player)
            else:
                # 敵人死亡時更新統計
                save_system.add_enemy_defeat()
                self.enemies.remove(enemy)

        # 檢查拳頭攻擊敵人
        self._check_fist_collisions()

        # 檢查拳頭打掉追蹤子彈
        self._check_fist_bullet_collisions()

        # 檢查滑行攻擊
        self.player.check_slide_attack(self.enemies)

        # 檢查 BOSS 子彈攻擊玩家
        self._check_bullet_collisions()

        # 檢查法師機器人子彈碰撞
        self._check_mage_bullet_collisions()

        # 檢查關卡完成條件
        if not self.enemies:  # 所有敵人都被擊敗
            if not self.level_complete:
                self.level_complete = True
                self.completion_time = (
                    pygame.time.get_ticks() - self.start_time
                ) / 1000.0  # 轉換為秒

                # 添加關卡完成特效
                screen_center_x = WINDOW_WIDTH // 2
                screen_center_y = WINDOW_HEIGHT // 2
                particle_system.create_level_complete_effect(
                    screen_center_x, screen_center_y
                )

                # 保存關卡完成進度（只保存一次）
                if not self.level_completed_saved:
                    save_system.complete_level(
                        self.level_number, self.completion_time, self.player.health
                    )
                    self.level_completed_saved = True

    def _check_fist_collisions(self):
        """檢查拳頭與敵人的碰撞"""
        hit_enemy = False

        for enemy in self.enemies:
            if not enemy.alive:
                continue

            # 檢查左拳碰撞
            if (
                self.player.left_fist.is_attacking
                and not self.player.left_fist.returning
                and self.player.left_fist.get_rect().colliderect(enemy.get_rect())
            ):
                # 計算傷害和效果
                base_damage = (
                    CHARGE_DAMAGE_MULTIPLIER if self.player.left_fist.is_charged else 1
                )

                # 應用連擊傷害倍數
                damage_multiplier = self.player.get_combo_damage_multiplier()
                final_damage = int(base_damage * damage_multiplier)

                # 空中攻擊傷害加成
                if self.player.left_fist.is_air_attack:
                    final_damage = int(final_damage * AIR_ATTACK_DAMAGE_MULTIPLIER)

                knockback = self.player.left_fist.is_charged
                stun = self.player.left_fist.is_charged  # 只有蓄力攻擊造成眩暈

                # 傳遞左拳位置作為攻擊源
                enemy.take_damage(
                    final_damage, knockback, stun, source_x=self.player.left_fist.x
                )

                # 播放攻擊音效
                try:
                    from systems.sound_manager import sound_manager

                    sound_manager.play_hit_sound(
                        is_charged=self.player.left_fist.is_charged
                    )
                except ImportError:
                    pass

                # 添加擊中特效
                hit_x = enemy.x + enemy.width // 2
                hit_y = enemy.y + enemy.height // 2
                is_charged = self.player.left_fist.is_charged
                particle_system.create_hit_effect(hit_x, hit_y, is_charged)

                # 添加傷害數字特效
                is_critical = damage_multiplier > 1.0 or final_damage > base_damage
                particle_system.create_damage_text(
                    hit_x, hit_y - 20, final_damage, is_critical
                )

                self.player.left_fist.returning = True  # 拳頭立即返回
                hit_enemy = True

            # 檢查右拳碰撞
            if (
                self.player.right_fist.is_attacking
                and not self.player.right_fist.returning
                and self.player.right_fist.get_rect().colliderect(enemy.get_rect())
            ):
                # 計算傷害和效果
                base_damage = (
                    CHARGE_DAMAGE_MULTIPLIER if self.player.right_fist.is_charged else 1
                )

                # 應用連擊傷害倍數
                damage_multiplier = self.player.get_combo_damage_multiplier()
                final_damage = int(base_damage * damage_multiplier)

                # 空中攻擊傷害加成
                if self.player.right_fist.is_air_attack:
                    final_damage = int(final_damage * AIR_ATTACK_DAMAGE_MULTIPLIER)

                knockback = self.player.right_fist.is_charged
                stun = self.player.right_fist.is_charged  # 只有蓄力攻擊造成眩暈

                # 傳遞右拳位置作為攻擊源
                enemy.take_damage(
                    final_damage, knockback, stun, source_x=self.player.right_fist.x
                )

                # 播放攻擊音效
                try:
                    from systems.sound_manager import sound_manager

                    sound_manager.play_hit_sound(
                        is_charged=self.player.right_fist.is_charged
                    )
                except ImportError:
                    pass

                # 添加擊中特效
                hit_x = enemy.x + enemy.width // 2
                hit_y = enemy.y + enemy.height // 2
                is_charged = self.player.right_fist.is_charged
                particle_system.create_hit_effect(hit_x, hit_y, is_charged)

                # 添加傷害數字特效
                is_critical = damage_multiplier > 1.0 or final_damage > base_damage
                particle_system.create_damage_text(
                    hit_x, hit_y - 20, final_damage, is_critical
                )

                self.player.right_fist.returning = True  # 拳頭立即返回
                hit_enemy = True

        # 更新連擊系統
        self.player.update_combo_system(hit_enemy)

        # 如果擊中敵人且連擊數達到閾值，添加連擊特效
        if hit_enemy and self.player.combo_count >= COMBO_EFFECT_THRESHOLD:
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            particle_system.create_combo_effect(
                player_center_x, player_center_y, self.player.combo_count
            )

    def _check_fist_bullet_collisions(self):
        """檢查拳頭是否打掉追蹤子彈"""
        for enemy in self.enemies:
            if hasattr(enemy, "bullets") and isinstance(enemy, MageRobot):
                for bullet in enemy.bullets[:]:
                    # 檢查左拳碰撞
                    if (
                        self.player.left_fist.is_attacking
                        and not self.player.left_fist.returning
                        and self.player.left_fist.get_rect().colliderect(
                            bullet.get_rect()
                        )
                    ):
                        enemy.bullets.remove(bullet)
                        # 拳頭打掉子彈不需要返回

                    # 檢查右拳碰撞
                    elif (
                        self.player.right_fist.is_attacking
                        and not self.player.right_fist.returning
                        and self.player.right_fist.get_rect().colliderect(
                            bullet.get_rect()
                        )
                    ):
                        enemy.bullets.remove(bullet)
                        # 拳頭打掉子彈不需要返回

    def _check_bullet_collisions(self):
        """檢查 BOSS 子彈與玩家的碰撞"""
        for enemy in self.enemies:
            if hasattr(enemy, "bullets"):  # 檢查敵人是否有子彈（主要是 BOSS）
                for bullet in enemy.bullets[:]:
                    if bullet.get_rect().colliderect(self.player.get_rect()):
                        # 對於雷射光束等持續性攻擊，確保只觸發一次傷害
                        if hasattr(bullet, "damage_dealt") and bullet.damage_dealt:
                            continue  # 已經造成過傷害，跳過

                        # 子彈擊中玩家
                        if self.player.is_defending:
                            # 玩家防禦成功，所有子彈攻擊都被格擋
                            # 防禦可以完全格擋所有類型的攻擊，包括雷射光束
                            pass  # 防禦成功，不造成任何傷害
                        else:
                            # 玩家受到傷害
                            self.player.take_damage()

                        # 標記雷射光束等持續性攻擊已處理
                        if hasattr(bullet, "damage_dealt"):
                            bullet.damage_dealt = True

                        # 移除子彈（除了雷射光束等持續性攻擊）
                        if not (hasattr(bullet, "width") and bullet.width > 10):
                            enemy.bullets.remove(bullet)

                    # 特殊處理：導彈的追蹤更新
                    if hasattr(bullet, "tracking") and bullet.tracking:
                        bullet.update(self.player)  # 傳入玩家以供追蹤

    def _check_mage_bullet_collisions(self):
        """檢查法師機器人追蹤子彈與玩家的碰撞"""
        for enemy in self.enemies:
            if hasattr(enemy, "bullets") and isinstance(enemy, MageRobot):
                for bullet in enemy.bullets[:]:
                    if bullet.get_rect().colliderect(self.player.get_rect()):
                        # 子彈擊中玩家
                        if self.player.is_defending:
                            # 玩家防禦成功
                            pass
                        else:
                            # 玩家受到傷害
                            self.player.take_damage()

                        # 移除子彈
                        enemy.bullets.remove(bullet)

    def _execute_clear_screen_skill(self):
        """執行清屏技能效果"""
        player_center_x = self.player.x + self.player.width // 2
        player_center_y = self.player.y + self.player.height // 2

        # 播放清屏技能音效
        try:
            from systems.sound_manager import sound_manager

            sound_manager.play_clear_screen_sound()
        except ImportError:
            pass

        # 添加清屏技能特效 - 從玩家位置擴散
        particle_system.create_clear_screen_effect(player_center_x, player_center_y)

        # 清除所有類型的子彈（包括法師機器人的追蹤子彈）
        for enemy in self.enemies:
            if hasattr(enemy, "bullets"):
                # 為被清除的每個子彈創建消散特效
                for bullet in enemy.bullets:
                    try:
                        bullet_x = getattr(bullet, "x", player_center_x)
                        bullet_y = getattr(bullet, "y", player_center_y)
                        # 創建子彈消散特效
                        for _ in range(8):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(3, 8)
                            vel_x = math.cos(angle) * speed
                            vel_y = math.sin(angle) * speed
                            from ..systems.particle_system import Particle

                            particle = Particle(
                                bullet_x,
                                bullet_y,
                                vel_x,
                                vel_y,
                                (255, 255, 255),
                                3,
                                30,
                                gravity=0,
                            )
                            particle_system.add_particle(particle)
                    except:
                        pass  # 如果獲取子彈位置失敗就跳過特效

                enemy.bullets.clear()

        # 擊退所有在範圍內的敵人
        for enemy in self.enemies:
            if enemy.alive:
                # 計算真實距離（包含Y軸）
                enemy_center_x = enemy.x + enemy.width // 2
                enemy_center_y = enemy.y + enemy.height // 2
                distance = math.sqrt(
                    (enemy_center_x - player_center_x) ** 2
                    + (enemy_center_y - player_center_y) ** 2
                )

                if distance <= CLEAR_SCREEN_RANGE:
                    # 應用強力擊退
                    enemy.knockback = True
                    enemy.knockback_start_time = pygame.time.get_ticks()

                    # 計算擊退方向（遠離玩家中心）
                    if distance > 0:
                        # 正規化方向向量
                        direction_x = (enemy_center_x - player_center_x) / distance
                        direction_y = (enemy_center_y - player_center_y) / distance

                        # 水平擊退
                        enemy.knockback_vel_x = direction_x * CLEAR_SCREEN_KNOCKBACK

                        # 向上擊飛（保證向上分量）
                        enemy.vel_y = -8 + max(0, direction_y * -5)
                        enemy.on_ground = False
                    else:
                        # 如果距離為0，隨機擊退方向
                        enemy.knockback_vel_x = random.choice(
                            [-CLEAR_SCREEN_KNOCKBACK, CLEAR_SCREEN_KNOCKBACK]
                        )
                        enemy.vel_y = -8
                        enemy.on_ground = False

    def draw(self, screen):
        """繪製關卡"""
        # 繪製背景
        screen.fill(self.background_color)

        # 繪製地面
        pygame.draw.rect(
            screen, BROWN, (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y)
        )

        # 繪製平台
        self.platform_system.draw(screen)

        # 繪製玩家
        self.player.draw(screen)

        # 繪製敵人
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(screen)

        # 繪製血量道具
        self.health_item_spawner.draw(screen)

        # 繪製粒子特效系統
        particle_system.draw(screen)

        # 繪製UI
        self._draw_ui(screen)

        # 繪製遊戲狀態提示
        if self.game_over:
            self._draw_game_over(screen)
        elif self.level_complete:
            self._draw_level_complete(screen)

    def _draw_ui(self, screen):
        """繪製遊戲UI"""
        # 關卡名稱
        level_text = self.font_medium.render(self.level_name, True, WHITE)
        screen.blit(level_text, (10, 10))

        # 玩家生命值（愛心）
        heart_size = 30
        for i in range(3):
            color = RED if i < self.player.health else GRAY
            heart_x = 10 + i * (heart_size + 5)
            heart_y = 50

            # 簡單的愛心形狀（使用圓形代替）
            pygame.draw.circle(
                screen,
                color,
                (heart_x + heart_size // 2, heart_y + heart_size // 2),
                heart_size // 2,
            )

        # 連擊系統顯示
        if self.player.combo_count > 0:
            combo_text = self.font_medium.render(
                f"連擊 x{self.player.combo_count}", True, YELLOW
            )
            screen.blit(combo_text, (10, 120))

            # 連擊倍數顯示
            multiplier = self.player.get_combo_damage_multiplier()
            if multiplier > 1.0:
                multiplier_text = self.font_small.render(
                    f"傷害 +{int((multiplier-1)*100)}%", True, GREEN
                )
                screen.blit(multiplier_text, (10, 150))

        # 反擊系統顯示
        current_time = pygame.time.get_ticks()
        if self.player.counter_attack_ready:
            remaining_time = (
                self.player.counter_attack_window
                - (current_time - self.player.counter_attack_start_time)
            ) / 1000
            if remaining_time > 0:
                counter_color = YELLOW if self.player.perfect_defense_bonus else GREEN
                counter_text = self.font_medium.render(
                    f"反擊就緒! {remaining_time:.1f}s", True, counter_color
                )
                screen.blit(counter_text, (WINDOW_WIDTH - 250, 50))

        # 防禦冷卻指示
        if self.player.is_defending:
            defense_text = self.font_small.render("防禦中", True, BLUE)
            screen.blit(defense_text, (10, 180))
        elif (
            pygame.time.get_ticks() - self.player.defense_cooldown_start
            < DEFENSE_COOLDOWN
        ):
            cooldown_remaining = (
                DEFENSE_COOLDOWN
                - (pygame.time.get_ticks() - self.player.defense_cooldown_start)
            ) / 1000
            cooldown_text = self.font_small.render(
                f"防禦冷卻: {cooldown_remaining:.1f}s", True, GRAY
            )
            screen.blit(cooldown_text, (10, 180))

        # 清屏技能冷卻指示
        if not self.player.clear_screen_available:
            clear_cooldown_remaining = (
                CLEAR_SCREEN_COOLDOWN
                - (pygame.time.get_ticks() - self.player.clear_screen_cooldown_start)
            ) / 1000
            clear_text = self.font_small.render(
                f"清屏技能冷卻: {clear_cooldown_remaining:.1f}s", True, (255, 165, 0)
            )
            screen.blit(clear_text, (10, 200))
        else:
            clear_ready_text = self.font_small.render("Q鍵: 清屏技能就緒", True, GREEN)
            screen.blit(clear_ready_text, (10, 200))

        # 敵人數量
        enemy_count = len([e for e in self.enemies if e.alive])
        enemy_text = self.font_small.render(f"剩餘敵人: {enemy_count}", True, WHITE)
        screen.blit(enemy_text, (WINDOW_WIDTH - 150, 10))

        # 操作提示
        controls = [
            "WASD/方向鍵: 移動跳躍",
            "按住左鍵/右鍵: 蓄力攻擊",
            "空白鍵: 防禦",
            "Q鍵: 反擊/清屏技能",
            "Shift: 蹲下/滑行",
            "ESC: 返回選單",
        ]

        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, WHITE)
            screen.blit(control_text, (10, WINDOW_HEIGHT - 140 + i * 20))

    def _draw_game_over(self, screen):
        """繪製遊戲結束畫面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 遊戲結束文字
        game_over_text = self.font_large.render("遊戲結束", True, RED)
        game_over_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        screen.blit(game_over_text, game_over_rect)

        # 重新開始提示
        restart_text = self.font_medium.render(
            "按 R 重新開始，按 ESC 返回選單", True, WHITE
        )
        restart_rect = restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
        )
        screen.blit(restart_text, restart_rect)

    def _draw_level_complete(self, screen):
        """繪製關卡完成畫面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 關卡完成文字
        complete_text = self.font_large.render("關卡完成！", True, GREEN)
        complete_rect = complete_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80)
        )
        screen.blit(complete_text, complete_rect)

        # 顯示完成時間
        if self.completion_time:
            time_text = self.font_medium.render(
                f"完成時間：{self.completion_time:.2f} 秒", True, YELLOW
            )
            time_rect = time_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)
            )
            screen.blit(time_text, time_rect)

        # 下一步提示
        if self.level_number == LEVEL_2:
            if self.player.health == 3:
                next_text = self.font_medium.render(
                    "滿血狀態！按 Enter 進入隱藏關卡", True, YELLOW
                )
            else:
                next_text = self.font_medium.render("按 Enter 進入第三關", True, WHITE)
            next_rect = next_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
            )
            screen.blit(next_text, next_rect)
        elif self.level_number == LEVEL_2_5:
            next_text = self.font_medium.render("按 Enter 進入最終關卡", True, WHITE)
            next_rect = next_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
            )
            screen.blit(next_text, next_rect)
        elif self.level_number < LEVEL_3:
            next_text = self.font_medium.render("按 Enter 進入下一關", True, WHITE)
            next_rect = next_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
            )
            screen.blit(next_text, next_rect)
        else:
            next_text = self.font_medium.render("恭喜完成所有關卡！", True, YELLOW)
            next_rect = next_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
            )
            screen.blit(next_text, next_rect)

        # 其他選項
        options_text = self.font_small.render(
            "Tab：返回關卡選擇    R：重新開始    ESC：主選單", True, GRAY
        )
        options_rect = options_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        )
        screen.blit(options_text, options_rect)
