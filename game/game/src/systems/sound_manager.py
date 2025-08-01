"""
音效管理系統
"""

import pygame
import os


class SoundManager:
    """音效管理器 - 單例模式"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not SoundManager._initialized:
            self.sounds = {}
            self.enabled = True
            self.volume = 0.7  # 預設音量
            SoundManager._initialized = True

    def ensure_loaded(self):
        """確保音效已載入（延遲載入）"""
        if not self.sounds:
            self._load_sounds()

    def _load_sounds(self):
        """載入所有音效檔案"""
        try:
            # 音效檔案路徑 - 相對於 src/systems/ 目錄
            # 從 game/game/src/systems/ 到 assets/sounds/: ../../assets/sounds
            base_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "assets", "sounds"
            )
            base_path = os.path.abspath(base_path)  # 轉換為絕對路徑

            print(f"音效檔案搜尋路徑: {base_path}")

            # 定義音效檔案
            sound_files = {
                "normal_hit": "damage4.mp3",  # 普通攻擊擊中敵人音效
                "charged_hit": "damage6.mp3",  # 蓄力攻擊擊中敵人音效
                "clear_screen": "striking.mp3",  # 清屏技能施放音效
            }

            # 載入音效
            for sound_name, filename in sound_files.items():
                file_path = os.path.join(base_path, filename)
                if os.path.exists(file_path):
                    try:
                        sound = pygame.mixer.Sound(file_path)
                        sound.set_volume(self.volume)
                        self.sounds[sound_name] = sound
                        print(f"成功載入音效: {sound_name} ({filename})")
                    except pygame.error as e:
                        print(f"載入音效失敗: {filename} - {e}")
                else:
                    print(f"音效檔案不存在: {file_path}")

        except Exception as e:
            print(f"音效系統初始化失敗: {e}")

    def play_sound(self, sound_name):
        """播放指定音效"""
        if not self.enabled:
            return

        # 確保音效已載入
        self.ensure_loaded()

        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"播放音效失敗: {sound_name} - {e}")
        else:
            print(f"音效不存在: {sound_name}")

    def play_hit_sound(self, is_charged=False):
        """播放攻擊擊中音效"""
        if is_charged:
            self.play_sound("charged_hit")
        else:
            self.play_sound("normal_hit")

    def play_clear_screen_sound(self):
        """播放清屏技能音效"""
        self.play_sound("clear_screen")

    def set_volume(self, volume):
        """設定音量 (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        self.ensure_loaded()
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def set_enabled(self, enabled):
        """啟用/禁用音效"""
        self.enabled = enabled

    def stop_all_sounds(self):
        """停止所有音效"""
        pygame.mixer.stop()

    def get_available_sounds(self):
        """取得已載入的音效列表"""
        self.ensure_loaded()
        return list(self.sounds.keys())


# 建立全域音效管理器實例
sound_manager = SoundManager()
