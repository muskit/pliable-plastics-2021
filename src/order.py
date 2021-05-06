## Order screen. Displays current orders in the DB, as well as allow creating new ones.
import curses

class Order:
    def __init__(self, screen):
        this.screen = screen