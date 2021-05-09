from utils import *
import curses


class Menu:
    def __init__(self, screen, title, choices: list[(str, object)] = [], vertical = True):
        self.screen = screen
        self.title = title
        self.vertical = vertical
        self.choices = choices
        self.selection = 0
        self.highlighted = 0
        self.curVisible = True

    def get_text_of(self, idx):
        try:
            return self.choices[idx][0]
        except:
            return -1

    def get_selection_text(self):
        return self.choices[self.selection][0]
    def get_highlighted_text(self):
        return self.choices[self.highlighted][0]

    def highlight_prev(self):
        self.highlighted = self.highlighted - 1 if self.highlighted > 0 else len(self.choices) - 1
    def highlight_next(self):
        self.highlighted = self.highlighted + 1 if self.highlighted < len(self.choices) - 1 else 0
    
    def input(self, key):
        if self.vertical:
            if key in { curses.KEY_UP, 65 }:
                self.highlight_prev()
            elif key in { curses.KEY_DOWN, 66 }:
                self.highlight_next()
        else:
            if key in { curses.KEY_LEFT, 68 }:
                self.highlight_prev()
            elif key in { curses.KEY_RIGHT, 67 }:
                self.highlight_next()

        if key in { curses.KEY_ENTER, 10, 13 }:
            self.selection = self.highlighted
            return True
        return False

    def refresh(self):
        self.screen.clear()
        place_str(self.screen, 0, 0, self.title, True, False)
        xCoord = 0
        for indx in range(len(self.choices)):
            if self.vertical:
                place_str(self.screen, 1+indx, 0, self.choices[indx][0], False, self.curVisible and indx == self.highlighted)
            else:
                place_str(self.screen, 1, xCoord, self.choices[indx][0], False, self.curVisible and indx == self.highlighted)
                xCoord += len(self.choices[indx][0]) + 3

        self.screen.refresh()
        
    
    def loop(self):
        while True:
            self.refresh()

            key = self.screen.getch()
            if self.input(key):
                return self.choices[self.selection][1]

