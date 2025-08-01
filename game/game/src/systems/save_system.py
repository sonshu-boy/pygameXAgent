"""
遊戲存檔系統
用於保存關卡進度和解鎖狀態
"""

import json
import os
from constants import *


class SaveSystem:
    def __init__(self):
        self.save_file = "game_save.json"
        self.default_save_data = {
            "unlocked_levels": [LEVEL_1],  # 預設解鎖第一關
            "completed_levels": [],
            "player_stats": {
                "total_playtime": 0,
                "total_enemies_defeated": 0,
                "best_times": {},
            },
        }
        self.save_data = self._load_save_data()

    def _load_save_data(self):
        """載入存檔資料"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 確保存檔結構完整
                    for key in self.default_save_data:
                        if key not in data:
                            data[key] = self.default_save_data[key]
                    return data
            else:
                # 如果沒有存檔文件，返回預設存檔並創建文件
                default_data = self.default_save_data.copy()
                self.save_data = default_data  # 臨時設定以便保存
                self._save_data()
                return default_data
        except (json.JSONDecodeError, IOError):
            # 存檔損壞時使用預設值
            default_data = self.default_save_data.copy()
            self.save_data = default_data  # 臨時設定以便保存
            self._save_data()
            return default_data

    def _save_data(self):
        """保存存檔資料"""
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(self.save_data, f, ensure_ascii=False, indent=2)
        except IOError:
            print("警告：無法保存遊戲進度")

    def is_level_unlocked(self, level_number):
        """檢查關卡是否已解鎖"""
        return level_number in self.save_data["unlocked_levels"]

    def is_level_completed(self, level_number):
        """檢查關卡是否已完成"""
        return level_number in self.save_data["completed_levels"]

    def unlock_level(self, level_number):
        """解鎖關卡"""
        if level_number not in self.save_data["unlocked_levels"]:
            self.save_data["unlocked_levels"].append(level_number)
            self.save_data["unlocked_levels"].sort()
            self._save_data()

    def complete_level(self, level_number, completion_time=None, player_health=None):
        """標記關卡完成"""
        # 標記完成
        if level_number not in self.save_data["completed_levels"]:
            self.save_data["completed_levels"].append(level_number)

        # 記錄最佳時間
        if completion_time:
            current_best = self.save_data["player_stats"]["best_times"].get(
                str(level_number)
            )
            if current_best is None or completion_time < current_best:
                self.save_data["player_stats"]["best_times"][
                    str(level_number)
                ] = completion_time

        # 特殊解鎖邏輯
        if level_number == LEVEL_2:
            # 第二關完成後的解鎖邏輯
            if player_health == 3:  # 滿血完成第二關
                self.unlock_level(LEVEL_2_5)  # 解鎖隱藏關卡
            self.unlock_level(LEVEL_3)  # 總是解鎖第三關
        elif level_number == LEVEL_2_5:
            # 完成隱藏關卡後解鎖第三關（如果還沒解鎖）
            self.unlock_level(LEVEL_3)
        else:
            # 其他關卡的標準解鎖邏輯
            next_level = level_number + 1
            if next_level <= LEVEL_3:
                self.unlock_level(next_level)

        self._save_data()

    def unlock_level_2_5(self):
        """特殊方法：解鎖隱藏關卡 2.5"""
        self.unlock_level(LEVEL_2_5)

    def get_unlocked_levels(self):
        """獲取已解鎖的關卡列表"""
        return self.save_data["unlocked_levels"].copy()

    def get_completed_levels(self):
        """獲取已完成的關卡列表"""
        return self.save_data["completed_levels"].copy()

    def get_best_time(self, level_number):
        """獲取關卡最佳時間"""
        return self.save_data["player_stats"]["best_times"].get(str(level_number))

    def reset_save_data(self):
        """重置存檔資料"""
        self.save_data = self.default_save_data.copy()
        self._save_data()

    def add_enemy_defeat(self):
        """增加擊敗敵人計數"""
        self.save_data["player_stats"]["total_enemies_defeated"] += 1
        # 不每次都保存，只在關卡結束時保存

    def add_playtime(self, time_ms):
        """增加遊戲時間"""
        self.save_data["player_stats"]["total_playtime"] += time_ms
        # 不每次都保存，只在關卡結束時保存


# 全域存檔系統實例
save_system = SaveSystem()
