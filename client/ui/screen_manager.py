class ScreenManager:
    def __init__(self, root):
        self.root = root
        self.current_screen = None

    def show(self, screen_class):
        if self.current_screen is not None:
            self.current_screen.destroy()

        self.current_screen = screen_class(
            self.root,
            self
        )

        self.current_screen.pack(
            fill="both",
            expand=True
        )