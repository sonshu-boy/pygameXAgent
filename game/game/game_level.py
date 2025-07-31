"""
遊戲關卡系統
"""

import pygame
from constants import *
from player import Player
from enemies import TrainingDummy, SmallRobot, GiantRobot
from font_manager import get_font


class GameLevel:
    def __init__(self, state_manager, level_number):
        self.state_manager = state_manager
        self.level_number = level_number
        self.player = Player(100, GROUND_Y - PLAYER_HEIGHT)
        self.enemies = []
        self.level_complete = False
        self.game_over = False

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
            self.enemies.append(TrainingDummy(500, GROUND_Y - DUMMY_HEIGHT))

        elif self.level_number == LEVEL_2:
            # 第二關：工廠
            self.level_name = "第二關：工廠"
            self.background_color = (100, 100, 100)  # 灰色
            for i in range(3):
                self.enemies.append(
                    SmallRobot(400 + i * 150, GROUND_Y - SMALL_ROBOT_HEIGHT)
                )

        elif self.level_number == LEVEL_3:
            # 第三關：實驗室（BOSS）
            self.level_name = "第三關：實驗室 - BOSS戰"
            self.background_color = (80, 50, 100)  # 紫色
            self.enemies.append(GiantRobot(600, GROUND_Y - BOSS_HEIGHT))

    def handle_event(self, event):
        """處理關卡事件"""
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
                    # 遊戲完成，返回主選單
                    self.state_manager.return_to_menu()

    def update(self):
        """更新關卡邏輯"""
        if self.game_over or self.level_complete:
            return

        # 更新玩家
        self.player.update()

        # 檢查玩家生命值
        if self.player.health <= 0:
            self.game_over = True
            return

        # 更新敵人
        for enemy in self.enemies[:]:  # 使用切片複製列表避免修改時出錯
            if enemy.alive:
                enemy.update(self.player)
            else:
                self.enemies.remove(enemy)

        # 檢查拳頭攻擊敵人
        self._check_fist_collisions()

        # 檢查關卡完成條件
        if not self.enemies:  # 所有敵人都被擊敗
            self.level_complete = True

    def _check_fist_collisions(self):
        """檢查拳頭與敵人的碰撞"""
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
                if self.player.left_fist.is_charged:
                    damage = CHARGE_DAMAGE_MULTIPLIER
                    knockback = True
                    stun = True
                else:
                    damage = 1
                    knockback = False
                    stun = False  # 普通攻擊不會造成眩暈

                enemy.take_damage(damage, knockback, stun)
                self.player.left_fist.returning = True  # 拳頭立即返回

            # 檢查右拳碰撞
            if (
                self.player.right_fist.is_attacking
                and not self.player.right_fist.returning
                and self.player.right_fist.get_rect().colliderect(enemy.get_rect())
            ):
                # 計算傷害和效果
                if self.player.right_fist.is_charged:
                    damage = CHARGE_DAMAGE_MULTIPLIER
                    knockback = True
                    stun = True
                else:
                    damage = 1
                    knockback = False
                    stun = False  # 普通攻擊不會造成眩暈

                enemy.take_damage(damage, knockback, stun)
                self.player.right_fist.returning = True  # 拳頭立即返回

    def draw(self, screen):
        """繪製關卡"""
        # 繪製背景
        screen.fill(self.background_color)

        # 繪製地面
        pygame.draw.rect(
            screen, BROWN, (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y)
        )

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

        # 防禦冷卻指示
        if self.player.is_defending:
            defense_text = self.font_small.render("防禦中", True, BLUE)
            screen.blit(defense_text, (10, 100))
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
            screen.blit(cooldown_text, (10, 100))

        # 敵人數量
        enemy_count = len([e for e in self.enemies if e.alive])
        enemy_text = self.font_small.render(f"剩餘敵人: {enemy_count}", True, WHITE)
        screen.blit(enemy_text, (WINDOW_WIDTH - 150, 10))

        # 操作提示
        controls = [
            "WASD/方向鍵: 移動跳躍",
            "按住左鍵/右鍵: 蓄力攻擊",
            "空白鍵: 防禦",
            "Shift: 蹲下/滑行",
            "ESC: 返回選單",
        ]

        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, WHITE)
            screen.blit(control_text, (10, WINDOW_HEIGHT - 120 + i * 20))

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
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        screen.blit(complete_text, complete_rect)

        # 下一步提示
        if self.level_number < LEVEL_3:
            next_text = self.font_medium.render(
                "按 Enter 進入下一關，按 R 重新開始", True, WHITE
            )
        else:
            next_text = self.font_medium.render(
                "恭喜完成所有關卡！按 Enter 返回選單", True, YELLOW
            )

        next_rect = next_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
        )
        screen.blit(next_text, next_rect)
