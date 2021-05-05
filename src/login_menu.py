from utils import *
import curses

class Something:
    def __init__(screen):
        self.screen = screen

class Menu:
    def __init__(self, screen, title, choices: list[str] = []):
        self.screen = screen
        self.title = title
        self.choices = choices
        self.selection = 0
        self.highlighted = 0

    def get_text_of(self, idx):
        try:
            return self.choices[idx]
        except:
            return -1

    def get_selection_text(self):
        return self.choices[self.selection]
    
    def input(self, key):
        if key == curses.KEY_UP:
            self.highlighted = self.highlighted - 1 if self.highlighted > 0 else len(self.choices) - 1
        elif key == curses.KEY_DOWN:
            self.highlighted = self.highlighted + 1 if self.highlighted < len(self.choices) - 1 else 0
        elif key == curses.KEY_ENTER or key == 10: # keycode 10 is ENTER in Windows?
            self.selection = self.highlighted
            return True
        return False
    
    def loop(self):
        key = -1
        while True:
            self.screen.clear()
            place_str(self.screen, 0, 0, self.title, True)
            place_str(self.screen, 1, 0, key)
            for indx in range(len(self.choices)):
                place_str(self.screen, 3+indx, 0, self.choices[indx], indx == self.highlighted)

            self.screen.refresh()

            key = self.screen.getch()
            if self.input(key):
                return self.selection

