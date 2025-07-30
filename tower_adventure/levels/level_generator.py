"""
關卡設計和生成模組
"""

from config.settings import *
from src.game_objects import Platform, Enemy, Cheese


class LevelGenerator:
    """關卡生成器"""

    @staticmethod
    def create_section_1(base_y):
        """區域1：入門區域 - 簡單的平台和基礎敵人"""
        platforms = []
        enemies = []
        cheeses = []

        # 安全起始平台 - 玩家出生點
        platforms.extend(
            [
                Platform(400, base_y + 20, 200, 30),  # 大型安全起始平台
                # 裝飾性邊框平台，標示安全區域
                Platform(380, base_y + 15, 20, 10),  # 左邊框
                Platform(600, base_y + 15, 20, 10),  # 右邊框
                Platform(420, base_y + 10, 160, 5),  # 頂部邊框
            ]
        )

        # 起始區域平台（距離安全平台有一定距離）
        platforms.extend(
            [
                Platform(80, base_y + 80, 120, 20),
                Platform(250, base_y + 120, 100, 20),
                Platform(400, base_y + 90, 120, 20),
                Platform(580, base_y + 140, 100, 20),
                Platform(750, base_y + 100, 120, 20),
                Platform(50, base_y + 200, 150, 20),
                Platform(250, base_y + 250, 120, 20),
                Platform(420, base_y + 220, 100, 20),
                Platform(580, base_y + 280, 120, 20),
                Platform(750, base_y + 240, 100, 20),
                # 連接到下一區域的平台
                Platform(0, base_y + 350, 200, 20),
                Platform(300, base_y + 380, 150, 20),
                Platform(500, base_y + 360, 200, 20),
                Platform(750, base_y + 400, 150, 20),
            ]
        )

        # 敵人（已移除）
        # enemies.extend([])

        # 起司（已移除）
        # cheeses.extend([])

        return platforms, enemies, cheeses

    @staticmethod
    def create_section_2(base_y):
        """區域2：平台跳躍區域 - 需要精確跳躍的平台"""
        platforms = []
        enemies = []
        cheeses = []

        # 跳躍挑戰平台
        platforms.extend(
            [
                Platform(100, base_y + 50, 80, 20),
                Platform(250, base_y + 80, 60, 20),
                Platform(380, base_y + 50, 80, 20),
                Platform(530, base_y + 100, 60, 20),
                Platform(650, base_y + 70, 80, 20),
                Platform(800, base_y + 120, 60, 20),
                Platform(50, base_y + 180, 100, 20),
                Platform(200, base_y + 150, 80, 20),
                Platform(330, base_y + 200, 60, 20),
                Platform(450, base_y + 170, 80, 20),
                Platform(580, base_y + 220, 60, 20),
                Platform(700, base_y + 190, 100, 20),
                Platform(150, base_y + 280, 120, 20),
                Platform(350, base_y + 320, 100, 20),
                Platform(550, base_y + 300, 120, 20),
                Platform(750, base_y + 350, 100, 20),
            ]
        )

        # 巡邏敵人（已移除）
        # enemies.extend([])

        # 更多起司獎勵（已移除）
        # cheeses.extend([])

        return platforms, enemies, cheeses

    @staticmethod
    def create_section_3(base_y):
        """區域3：敵人密集區域 - 更多戰鬥挑戰"""
        platforms = []
        enemies = []
        cheeses = []

        # 戰鬥平台
        platforms.extend(
            [
                Platform(0, base_y + 80, 180, 20),
                Platform(220, base_y + 120, 160, 20),
                Platform(420, base_y + 80, 180, 20),
                Platform(640, base_y + 140, 160, 20),
                Platform(820, base_y + 100, 120, 20),
                Platform(100, base_y + 200, 200, 20),
                Platform(350, base_y + 240, 180, 20),
                Platform(580, base_y + 200, 200, 20),
                Platform(50, base_y + 320, 150, 20),
                Platform(250, base_y + 360, 120, 20),
                Platform(420, base_y + 330, 150, 20),
                Platform(620, base_y + 380, 120, 20),
                Platform(780, base_y + 350, 150, 20),
            ]
        )

        # 大量敵人（已移除）
        # enemies.extend([])

        # 豐富的起司獎勵（已移除）
        # cheeses.extend([])

        return platforms, enemies, cheeses

    @staticmethod
    def create_section_4(base_y):
        """區域4：精密跳躍區域 - 需要完美時機的挑戰"""
        platforms = []
        enemies = []
        cheeses = []

        # 小型精密平台
        platforms.extend(
            [
                Platform(120, base_y + 60, 60, 15),
                Platform(220, base_y + 90, 50, 15),
                Platform(310, base_y + 60, 60, 15),
                Platform(410, base_y + 100, 50, 15),
                Platform(500, base_y + 70, 60, 15),
                Platform(600, base_y + 110, 50, 15),
                Platform(690, base_y + 80, 60, 15),
                Platform(790, base_y + 120, 50, 15),
                Platform(80, base_y + 170, 70, 15),
                Platform(180, base_y + 140, 60, 15),
                Platform(270, base_y + 180, 50, 15),
                Platform(350, base_y + 150, 70, 15),
                Platform(450, base_y + 190, 60, 15),
                Platform(540, base_y + 160, 50, 15),
                Platform(620, base_y + 200, 70, 15),
                Platform(720, base_y + 170, 60, 15),
                Platform(810, base_y + 210, 50, 15),
                Platform(150, base_y + 270, 80, 20),
                Platform(280, base_y + 240, 70, 20),
                Platform(400, base_y + 280, 80, 20),
                Platform(520, base_y + 250, 70, 20),
                Platform(640, base_y + 290, 80, 20),
                Platform(760, base_y + 260, 70, 20),
                Platform(100, base_y + 350, 120, 20),
                Platform(300, base_y + 380, 100, 20),
                Platform(500, base_y + 360, 120, 20),
                Platform(700, base_y + 390, 100, 20),
            ]
        )

        # 精英敵人（已移除）
        # enemies.extend([])

        # 高價值起司（已移除）
        # cheeses.extend([])

        return platforms, enemies, cheeses

    @staticmethod
    def create_section_5(base_y):
        """區域5：Boss區域和終點"""
        platforms = []
        enemies = []
        cheeses = []

        # Boss戰平台和終點
        platforms.extend(
            [
                Platform(200, base_y + 100, 200, 30),  # Boss戰平台
                Platform(500, base_y + 150, 150, 20),
                Platform(100, base_y + 200, 180, 20),
                Platform(350, base_y + 250, 200, 20),
                Platform(600, base_y + 220, 150, 20),
                Platform(150, base_y + 320, 250, 30),  # 大型休息平台
                Platform(500, base_y + 360, 200, 20),
                Platform(750, base_y + 340, 150, 20),
                Platform(0, base_y + 450, WINDOW_WIDTH, 50),  # 最終地面
            ]
        )

        # Boss和最終敵人（已移除）
        # enemies.extend([])

        # 最終獎勵起司（已移除）
        # cheeses.extend([])

        return platforms, enemies, cheeses

    @staticmethod
    def create_safe_transition_platform(section_start_y):
        """在每個區域開始處創建安全過渡平台"""
        platforms = []
        cheeses = []

        # 大型安全平台 - 橫跨大部分螢幕寬度
        main_platform_width = 600
        main_platform_x = (WINDOW_WIDTH - main_platform_width) // 2
        platforms.append(
            Platform(
                main_platform_x, section_start_y - 50, main_platform_width, 40, GREEN
            )
        )

        # 裝飾性邊框平台，突出安全區域
        border_width = 20
        platforms.extend(
            [
                Platform(
                    main_platform_x - border_width,
                    section_start_y - 55,
                    border_width,
                    10,
                    GREEN,
                ),  # 左邊框
                Platform(
                    main_platform_x + main_platform_width,
                    section_start_y - 55,
                    border_width,
                    10,
                    GREEN,
                ),  # 右邊框
                Platform(
                    main_platform_x, section_start_y - 60, main_platform_width, 5, GREEN
                ),  # 頂部邊框
            ]
        )

        # 在安全平台上放置治療起司（已移除）
        # cheese_spacing = 80
        # cheese_start_x = main_platform_x + 50
        # for i in range(6):  # 6個治療起司
        #     cheese_x = cheese_start_x + i * cheese_spacing
        #     if cheese_x < main_platform_x + main_platform_width - 50:
        #         cheeses.append(Cheese(cheese_x, section_start_y - 80))

        return platforms, cheeses

    @classmethod
    def generate_complete_tower(cls):
        """生成完整的塔樓"""
        all_platforms = []
        all_enemies = []
        all_cheeses = []

        # 生成所有區域
        sections = [
            cls.create_section_1,
            cls.create_section_2,
            cls.create_section_3,
            cls.create_section_4,
            cls.create_section_5,
        ]

        for i, section_func in enumerate(sections):
            base_y = i * SECTION_HEIGHT

            # 在每個區域開始前添加安全平台（除了第一個區域）
            if i > 0:  # 不在第一個區域添加，因為已經有安全起始平台
                safe_platforms, safe_cheeses = cls.create_safe_transition_platform(
                    base_y
                )
                all_platforms.extend(safe_platforms)
                # 安全起司已移除
                # all_cheeses.extend(safe_cheeses)

            # 生成該區域的內容
            platforms, enemies, cheeses = section_func(base_y)
            all_platforms.extend(platforms)
            # 敵人和起司已移除
            # all_enemies.extend(enemies)
            # all_cheeses.extend(cheeses)

        return all_platforms, all_enemies, all_cheeses
