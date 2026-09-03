import tkinter as tk

from client.ui.menu import Menu
from client.ui.screen_manager import ScreenManager


def main():
    root = tk.Tk()

    screen_manager = ScreenManager(root)
    screen_manager.show(Menu)

    root.mainloop()


if __name__ == "__main__":
    main()