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

        # 敵人（遠離安全區域）
        enemies.extend(
            [
                Enemy(100, base_y + 50, "basic"),  # 在左下方平台
                Enemy(270, base_y + 90, "basic"),  # 在中間平台
                Enemy(270, base_y + 220, "basic"),  # 在下方平台
                Enemy(440, base_y + 190, "basic"),  # 在右下方平台
            ]
        )

        # 起司
        cheeses.extend(
            [
                # 安全平台上的歡迎起司
                Cheese(450, base_y - 10),  # 在安全平台上
                Cheese(500, base_y - 10),  # 在安全平台上
                Cheese(550, base_y - 10),  # 在安全平台上
                # 其他區域的起司
                Cheese(120, base_y + 50),
                Cheese(290, base_y + 90),
                Cheese(290, base_y + 220),
                Cheese(460, base_y + 190),
                Cheese(350, base_y + 350),
                Cheese(550, base_y + 330),
            ]
        )

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

        # 巡邏敵人
        enemies.extend(
            [
                Enemy(120, base_y + 20, "basic"),
                Enemy(400, base_y + 20, "basic"),
                Enemy(670, base_y + 40, "basic"),
                Enemy(220, base_y + 120, "basic"),
                Enemy(470, base_y + 140, "basic"),
                Enemy(720, base_y + 160, "basic"),
                Enemy(180, base_y + 250, "basic"),
                Enemy(380, base_y + 290, "basic"),
                Enemy(580, base_y + 270, "basic"),
            ]
        )

        # 更多起司獎勵
        cheeses.extend(
            [
                Cheese(130, base_y + 20),
                Cheese(280, base_y + 50),
                Cheese(410, base_y + 20),
                Cheese(560, base_y + 70),
                Cheese(680, base_y + 40),
                Cheese(230, base_y + 120),
                Cheese(360, base_y + 170),
                Cheese(480, base_y + 140),
                Cheese(610, base_y + 190),
                Cheese(380, base_y + 290),
                Cheese(580, base_y + 270),
            ]
        )

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

        # 大量敵人
        enemies.extend(
            [
                Enemy(20, base_y + 50, "basic"),
                Enemy(100, base_y + 50, "basic"),
                Enemy(240, base_y + 90, "basic"),
                Enemy(320, base_y + 90, "basic"),
                Enemy(440, base_y + 50, "basic"),
                Enemy(520, base_y + 50, "basic"),
                Enemy(660, base_y + 110, "basic"),
                Enemy(740, base_y + 110, "boss"),
                Enemy(120, base_y + 170, "basic"),
                Enemy(200, base_y + 170, "basic"),
                Enemy(370, base_y + 210, "basic"),
                Enemy(450, base_y + 210, "basic"),
                Enemy(600, base_y + 170, "basic"),
                Enemy(680, base_y + 170, "boss"),
                Enemy(70, base_y + 290, "basic"),
                Enemy(150, base_y + 290, "basic"),
                Enemy(270, base_y + 330, "basic"),
                Enemy(440, base_y + 300, "basic"),
                Enemy(520, base_y + 300, "basic"),
                Enemy(640, base_y + 350, "boss"),
                Enemy(800, base_y + 320, "boss"),
            ]
        )

        # 豐富的起司獎勵
        cheeses.extend(
            [
                Cheese(50, base_y + 50),
                Cheese(130, base_y + 50),
                Cheese(270, base_y + 90),
                Cheese(350, base_y + 90),
                Cheese(470, base_y + 50),
                Cheese(550, base_y + 50),
                Cheese(150, base_y + 170),
                Cheese(230, base_y + 170),
                Cheese(400, base_y + 210),
                Cheese(480, base_y + 210),
                Cheese(100, base_y + 290),
                Cheese(300, base_y + 330),
                Cheese(470, base_y + 300),
                Cheese(670, base_y + 350),
            ]
        )

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

        # 精英敵人
        enemies.extend(
            [
                Enemy(140, base_y + 30, "basic"),
                Enemy(240, base_y + 60, "basic"),
                Enemy(330, base_y + 30, "basic"),
                Enemy(430, base_y + 70, "basic"),
                Enemy(520, base_y + 40, "basic"),
                Enemy(620, base_y + 80, "basic"),
                Enemy(710, base_y + 50, "basic"),
                Enemy(100, base_y + 140, "boss"),
                Enemy(200, base_y + 110, "basic"),
                Enemy(290, base_y + 150, "basic"),
                Enemy(370, base_y + 120, "boss"),
                Enemy(470, base_y + 160, "basic"),
                Enemy(560, base_y + 130, "basic"),
                Enemy(640, base_y + 170, "boss"),
                Enemy(740, base_y + 140, "basic"),
                Enemy(180, base_y + 240, "boss"),
                Enemy(310, base_y + 210, "basic"),
                Enemy(430, base_y + 250, "boss"),
                Enemy(550, base_y + 220, "basic"),
                Enemy(670, base_y + 260, "boss"),
            ]
        )

        # 高價值起司
        cheeses.extend(
            [
                Cheese(150, base_y + 30),
                Cheese(250, base_y + 60),
                Cheese(340, base_y + 30),
                Cheese(440, base_y + 70),
                Cheese(530, base_y + 40),
                Cheese(630, base_y + 80),
                Cheese(720, base_y + 50),
                Cheese(110, base_y + 140),
                Cheese(210, base_y + 110),
                Cheese(300, base_y + 150),
                Cheese(380, base_y + 120),
                Cheese(480, base_y + 160),
                Cheese(570, base_y + 130),
                Cheese(650, base_y + 170),
                Cheese(750, base_y + 140),
                Cheese(190, base_y + 240),
                Cheese(320, base_y + 210),
                Cheese(440, base_y + 250),
                Cheese(560, base_y + 220),
                Cheese(680, base_y + 260),
                Cheese(130, base_y + 320),
                Cheese(330, base_y + 350),
                Cheese(530, base_y + 330),
                Cheese(730, base_y + 360),
            ]
        )

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

        # Boss和最終敵人
        enemies.extend(
            [
                Enemy(250, base_y + 70, "boss"),  # 主Boss
                Enemy(300, base_y + 70, "boss"),  # 副Boss
                Enemy(520, base_y + 120, "boss"),
                Enemy(120, base_y + 170, "boss"),
                Enemy(370, base_y + 220, "boss"),
                Enemy(620, base_y + 190, "boss"),
                Enemy(200, base_y + 290, "boss"),
                Enemy(300, base_y + 290, "boss"),
                Enemy(520, base_y + 330, "boss"),
                Enemy(770, base_y + 310, "boss"),
            ]
        )

        # 最終獎勵起司
        cheeses.extend(
            [
                Cheese(260, base_y + 70),
                Cheese(310, base_y + 70),
                Cheese(530, base_y + 120),
                Cheese(130, base_y + 170),
                Cheese(380, base_y + 220),
                Cheese(630, base_y + 190),
                Cheese(220, base_y + 290),
                Cheese(320, base_y + 290),
                Cheese(530, base_y + 330),
                Cheese(780, base_y + 310),
                Cheese(200, base_y + 420),  # 終點獎勵
                Cheese(400, base_y + 420),
                Cheese(600, base_y + 420),
                Cheese(800, base_y + 420),
            ]
        )

        return platforms, enemies, cheeses

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
            platforms, enemies, cheeses = section_func(base_y)
            all_platforms.extend(platforms)
            all_enemies.extend(enemies)
            all_cheeses.extend(cheeses)

        return all_platforms, all_enemies, all_cheeses
