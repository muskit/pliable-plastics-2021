from utils import *
import curses


class Menu:
    def __init__(self, screen, title, choices: list[(str, object)] = []):
        self.screen = screen
        self.title = title
        self.choices = choices
        self.selection = 0
        self.highlighted = 0

    def get_text_of(self, idx):
        try:
            return self.choices[idx][0]
        except:
            return -1

    def get_selection_text(self):
        return self.choices[self.selection][0]
    
    def input(self, key):
        if key == curses.KEY_UP:
            self.highlighted = self.highlighted - 1 if self.highlighted > 0 else len(self.choices) - 1
        elif key == curses.KEY_DOWN:
            self.highlighted = self.highlighted + 1 if self.highlighted < len(self.choices) - 1 else 0
        elif key in { curses.KEY_ENTER, 10, 13 }:
            self.selection = self.highlighted
            return True
        return False
    
    def loop(self):
        key = -1
        while True:
            self.screen.clear()
            place_str(self.screen, 0, 0, self.title, True, False)
            place_str(self.screen, 1, 0, key, curses.A_DIM)
            for indx in range(len(self.choices)):
                place_str(self.screen, 1+indx, 0, self.choices[indx][0], False, indx == self.highlighted)

            self.screen.refresh()

            key = self.screen.getch()
            if self.input(key):
                return self.choices[self.selection][1]

