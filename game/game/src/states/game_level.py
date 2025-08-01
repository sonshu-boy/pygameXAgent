"""
遊戲關卡系統
"""

import pygame
from constants import *
from entities.player import Player
from entities.enemies import TrainingDummy, SmallRobot, GiantRobot, EliteMech
from systems.platform_system import PlatformSystem
from systems.font_manager import get_font
from systems.save_system import save_system


class GameLevel:
    def __init__(self, state_manager, level_number):
        self.state_manager = state_manager
        self.level_number = level_number
        self.player = Player(100, GROUND_Y - PLAYER_HEIGHT)
        self.enemies = []
        self.level_complete = False
        self.game_over = False

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
                self.state_manager.return_to_menu()
            elif event.key == pygame.K_r and (self.game_over or self.level_complete):
                # 重新開始關卡
                self.__init__(self.state_manager, self.level_number)
            elif event.key == pygame.K_RETURN and self.level_complete:
                # 進入下一關
                if self.level_number < LEVEL_3:
                    self.state_manager.start_level(self.level_number + 1)
                else:
                    # 遊戲完成，返回關卡選擇
                    self.state_manager.change_state(LEVEL_SELECT_STATE)
            elif event.key == pygame.K_TAB and self.level_complete:
                # 返回關卡選擇
                self.state_manager.change_state(LEVEL_SELECT_STATE)

    def update(self):
        """更新關卡邏輯"""
        if self.game_over or self.level_complete:
            return

        # 更新玩家
        self.player.update()

        # 檢查反擊輸入
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        if keys[pygame.K_q] or (len(mouse_buttons) > 2 and mouse_buttons[2]):
            if self.player.try_counter_attack(self.enemies):
                # 反擊成功，添加視覺效果
                pass

        # 檢查玩家生命值
        if self.player.health <= 0:
            self.game_over = True
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

        # 檢查滑行攻擊
        self.player.check_slide_attack(self.enemies)

        # 檢查 BOSS 子彈攻擊玩家
        self._check_bullet_collisions()

        # 檢查關卡完成條件
        if not self.enemies:  # 所有敵人都被擊敗
            if not self.level_complete:
                self.level_complete = True
                self.completion_time = (
                    pygame.time.get_ticks() - self.start_time
                ) / 1000.0  # 轉換為秒

                # 保存關卡完成進度（只保存一次）
                if not self.level_completed_saved:
                    save_system.complete_level(self.level_number, self.completion_time)
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
                self.player.right_fist.returning = True  # 拳頭立即返回
                hit_enemy = True

        # 更新連擊系統
        self.player.update_combo_system(hit_enemy)

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

        # 敵人數量
        enemy_count = len([e for e in self.enemies if e.alive])
        enemy_text = self.font_small.render(f"剩餘敵人: {enemy_count}", True, WHITE)
        screen.blit(enemy_text, (WINDOW_WIDTH - 150, 10))

        # 操作提示
        controls = [
            "WASD/方向鍵: 移動跳躍",
            "按住左鍵/右鍵: 蓄力攻擊",
            "空白鍵: 防禦",
            "Q鍵/滑鼠中鍵: 反擊",
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
        if self.level_number < LEVEL_3:
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
