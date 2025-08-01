"""
遊戲狀態管理系統
"""

from constants import *
from states.menu import MainMenu
from states.game_level import GameLevel
from states.instructions import InstructionsScreen
from states.level_select import LevelSelectScreen


class GameStateManager:
    def __init__(self):
        self.current_state = MENU_STATE
        self.states = {
            MENU_STATE: MainMenu(self),
            INSTRUCTIONS_STATE: InstructionsScreen(self),
            LEVEL_SELECT_STATE: LevelSelectScreen(self),
        }
        self.current_level = None

    def change_state(self, new_state):
        """切換遊戲狀態"""
        self.current_state = new_state

    def start_level(self, level_number):
        """開始指定關卡"""
        self.current_level = GameLevel(self, level_number)
        self.states[GAME_STATE] = self.current_level
        self.change_state(GAME_STATE)

    def return_to_menu(self):
        """返回主選單"""
        self.current_level = None
        if GAME_STATE in self.states:
            del self.states[GAME_STATE]
        self.change_state(MENU_STATE)

    def handle_event(self, event):
        """處理事件"""
        if self.current_state in self.states:
            self.states[self.current_state].handle_event(event)

    def update(self):
        """更新當前狀態"""
        if self.current_state in self.states:
            self.states[self.current_state].update()

    def draw(self, screen):
        """繪製當前狀態"""
        if self.current_state in self.states:
            self.states[self.current_state].draw(screen)
