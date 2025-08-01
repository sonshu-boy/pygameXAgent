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
            self.bgm_volume = 0.3  # 背景音樂音量
            self.original_bgm_volume = 0.3  # 原始背景音樂音量（用於恢復）
            self.bgm_playing = False  # 背景音樂播放狀態
            SoundManager._initialized = True

    def ensure_loaded(self):
        """確保音效已載入（延遲載入）"""
        if not self.sounds:
            self._load_sounds()

    def _load_sounds(self):
        """載入所有音效檔案"""
        try:
            # 音效檔案路徑 - 相對於 src/systems/ 目錄
            # 從 game/game/src/systems/ 到 assets/sounds/: ../../../assets/sounds
            base_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "assets", "sounds"
            )
            base_path = os.path.abspath(base_path)  # 轉換為絕對路徑

            print(f"音效檔案搜尋路徑: {base_path}")

            # 定義音效檔案
            sound_files = {
                "normal_hit": "damage4.mp3",  # 普通攻擊擊中敵人音效
                "charged_hit": "damage6.mp3",  # 蓄力攻擊擊中敵人音效
                "clear_screen": "striking.mp3",  # 清屏技能施放音效
                "death": "damage2.mp3",  # 死亡音效
                "player_hurt": "defense1.mp3",  # 玩家受傷音效
                "enemy_hurt": "defense1.mp3",  # 敵人受傷音效
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

            # 嘗試載入背景音樂
            self._load_background_music(base_path)

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

    def play_death_sound(self):
        """播放死亡音效"""
        self.play_sound("death")

    def play_player_hurt_sound(self):
        """播放玩家受傷音效"""
        self.play_sound("player_hurt")

    def play_enemy_hurt_sound(self):
        """播放敵人受傷音效"""
        self.play_sound("enemy_hurt")

    def play_hurt_sound(self, is_player=True):
        """播放受傷音效

        Args:
            is_player (bool): True 為玩家受傷，False 為敵人受傷
        """
        if is_player:
            self.play_player_hurt_sound()
        else:
            self.play_enemy_hurt_sound()

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

    def _load_background_music(self, base_path):
        """載入背景音樂"""
        # 按優先級順序嘗試載入背景音樂檔案
        bgm_files = [
            "y2mate.gg - Chess Type Beat Slowed.mp3",  # 主要背景音樂
            "background_music.ogg",
            "background_music.webm",
            "background_music.m4a",
            "background_music_new.m4a",
        ]

        for filename in bgm_files:
            file_path = os.path.join(base_path, filename)
            if os.path.exists(file_path):
                try:
                    pygame.mixer.music.load(file_path)
                    pygame.mixer.music.set_volume(self.bgm_volume)
                    print(f"成功載入背景音樂: {filename}")
                    return
                except pygame.error as e:
                    print(f"載入背景音樂失敗: {filename} - {e}")

        print("未找到可用的背景音樂檔案")

    def play_background_music(self, loops=-1):
        """播放背景音樂"""
        if not self.enabled:
            return

        try:
            pygame.mixer.music.play(loops)
            self.bgm_playing = True
            print("開始播放背景音樂")
        except pygame.error as e:
            print(f"播放背景音樂失敗: {e}")

    def stop_background_music(self):
        """停止背景音樂"""
        pygame.mixer.music.stop()
        self.bgm_playing = False
        print("停止背景音樂")

    def pause_background_music(self):
        """暫停背景音樂"""
        pygame.mixer.music.pause()
        print("暫停背景音樂")

    def resume_background_music(self):
        """恢復背景音樂"""
        pygame.mixer.music.unpause()
        print("恢復背景音樂")

    def is_bgm_playing(self):
        """檢查背景音樂是否正在播放"""
        return self.bgm_playing and pygame.mixer.music.get_busy()

    def set_bgm_volume(self, volume):
        """設定背景音樂音量 (0.0 - 1.0)"""
        self.bgm_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.bgm_volume)

    def reduce_bgm_volume_for_gameplay(self):
        """進入關卡時將背景音樂音量減少50%"""
        # 保存當前音量作為原始音量
        self.original_bgm_volume = self.bgm_volume
        # 將音量減少50%
        new_volume = self.bgm_volume * 0.5
        self.set_bgm_volume(new_volume)
        print(f"關卡模式：背景音樂音量降低至 {int(new_volume * 100)}%")

    def restore_bgm_volume(self):
        """恢復背景音樂的原始音量"""
        self.set_bgm_volume(self.original_bgm_volume)
        print(f"背景音樂音量恢復至 {int(self.original_bgm_volume * 100)}%")


# 建立全域音效管理器實例
sound_manager = SoundManager()
