import tkinter as tk

from shared.constants import NOME_DO_JOGO


class Menu(tk.Frame):
    def __init__(self, root, screen_manager):
        super().__init__(root, bg="#f5f7fb")

        self.screen_manager = screen_manager
        self.root = root
        self.root.title(NOME_DO_JOGO)
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.resizable(False, False)

        self.criar_interface()

    def criar_interface(self):
        tk.Label(
            self,
            text=NOME_DO_JOGO,
            font=("Arial", 40, "bold"),
            bg="#f5f7fb",
            fg="#1f2937"
        ).pack(pady=(85, 8))

        tk.Label(
            self,
            text="Descubra a palavra. Siga o contexto.",
            font=("Arial", 13),
            bg="#f5f7fb",
            fg="#6b7280"
        ).pack(pady=(0, 35))

        botoes = tk.Frame(self, bg="#f5f7fb")
        botoes.pack()

        self._botao(botoes, "Iniciar jogo",
                    self.iniciar_jogo, 0, 0, principal=True)
        self._botao(botoes, "Ajuda", self.abrir_ajuda, 1, 0)
        self._botao(botoes, "Sobre", self.abrir_sobre, 2, 0)
        self._botao(botoes, "Sair", self.sair, 3, 0)

    def _botao(self, parent, texto, comando, linha, coluna, principal=False):
        kwargs = {
            "text": texto,
            "width": 25,
            "height": 2,
            "font": ("Arial", 11, "bold" if principal else "normal"),
            "command": comando,
            "relief": "flat",
            "cursor": "hand2"
        }
        if principal:
            kwargs.update({"bg": "#2563eb", "fg": "white",
                          "activebackground": "#1d4ed8", "activeforeground": "white"})
        else:
            kwargs.update({"bg": "#ffffff", "fg": "#374151",
                          "activebackground": "#e5e7eb"})

        botao = tk.Button(parent, **kwargs)
        botao.grid(row=linha, column=coluna, pady=6)

    def iniciar_jogo(self):
        from client.ui.game_screen import GameScreen
        self.screen_manager.show(GameScreen)

    def abrir_ajuda(self):
        from client.ui.help_screen import HelpScreen
        self.screen_manager.show(HelpScreen)

    def abrir_sobre(self):
        from client.ui.about_screen import AboutScreen
        self.screen_manager.show(AboutScreen)

    def sair(self):
        self.screen_manager.root.destroy()
