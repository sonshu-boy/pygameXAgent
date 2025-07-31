"""
字體管理模組 - 支援繁體中文顯示
"""

import pygame
import os


class FontManager:
    """字體管理器，提供支援繁體中文的字體"""

    def __init__(self):
        self.fonts = {}
        self._init_fonts()

    def _init_fonts(self):
        """初始化字體，優先使用系統中文字體"""
        # Windows 系統字體路徑
        chinese_fonts = [
            "C:/Windows/Fonts/msjh.ttc",  # 微軟正黑體
            "C:/Windows/Fonts/msyh.ttc",  # 微軟雅黑
            "C:/Windows/Fonts/mingliu.ttc",  # 細明體
            "C:/Windows/Fonts/simsun.ttc",  # 宋體
        ]

        # 查找可用的中文字體
        available_font = None
        for font_path in chinese_fonts:
            if os.path.exists(font_path):
                available_font = font_path
                break

        # 如果找不到中文字體，回退到預設字體
        if available_font is None:
            print("警告：找不到中文字體，使用預設字體")
            available_font = None

        # 初始化不同大小的字體
        try:
            self.fonts = {
                "large": pygame.font.Font(available_font, 48),
                "medium": pygame.font.Font(available_font, 32),
                "small": pygame.font.Font(available_font, 24),
                "tiny": pygame.font.Font(available_font, 18),
            }
            print(
                f"字體初始化成功：{available_font if available_font else '系統預設字體'}"
            )
        except Exception as e:
            print(f"字體初始化失敗：{e}")
            # 回退到系統預設字體
            self.fonts = {
                "large": pygame.font.Font(None, 48),
                "medium": pygame.font.Font(None, 32),
                "small": pygame.font.Font(None, 24),
                "tiny": pygame.font.Font(None, 18),
            }

    def get_font(self, size="medium"):
        """
        獲取指定大小的字體

        Args:
            size (str): 字體大小 ('large', 'medium', 'small', 'tiny')

        Returns:
            pygame.font.Font: 字體物件
        """
        return self.fonts.get(size, self.fonts["medium"])

    def render_text(self, text, size="medium", color=(255, 255, 255), antialias=True):
        """
        渲染文字

        Args:
            text (str): 要渲染的文字
            size (str): 字體大小
            color (tuple): 文字顏色 (R, G, B)
            antialias (bool): 是否開啟反鋸齒

        Returns:
            pygame.Surface: 渲染後的文字表面
        """
        font = self.get_font(size)
        return font.render(text, antialias, color)


# 全域字體管理器實例
_font_manager = None


def get_font_manager():
    """獲取全域字體管理器實例"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager


def get_font(size="medium"):
    """便捷函數：獲取指定大小的字體"""
    return get_font_manager().get_font(size)


def render_text(text, size="medium", color=(255, 255, 255)):
    """便捷函數：渲染文字"""
    return get_font_manager().render_text(text, size, color)
