import tkinter as tk

from shared.constants import NOME_DO_JOGO


class Menu(tk.Frame):
    def __init__(self, root, screen_manager):
        super().__init__(root)

        self.screen_manager = screen_manager

        self.root = root
        self.root.title(NOME_DO_JOGO)
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.criar_interface()

    def criar_interface(self):
        titulo = tk.Label(
            self,
            text=NOME_DO_JOGO,
            font=("Arial", 32, "bold")
        )
        titulo.pack(pady=(100, 50))

        botao_iniciar = tk.Button(
            self,
            text="Iniciar jogo",
            width=25,
            height=2,
            command=self.iniciar_jogo
        )
        botao_iniciar.pack(pady=10)

        botao_ajuda = tk.Button(
            self,
            text="Ajuda",
            width=25,
            height=2,
            command=self.abrir_ajuda
        )
        botao_ajuda.pack(pady=10)

        botao_sobre = tk.Button(
            self,
            text="Sobre",
            width=25,
            height=2,
            command=self.abrir_sobre
        )
        botao_sobre.pack(pady=10)

        botao_sair = tk.Button(
            self,
            text="Sair",
            width=25,
            height=2,
            command=self.sair
        )
        botao_sair.pack(pady=10)

    def iniciar_jogo(self):
        print("Iniciar jogo")

        from client.ui.game_screen import GameScreen

        self.screen_manager.show(GameScreen)

    def abrir_ajuda(self):
        print("Abrir help")

        from client.ui.help_screen import HelpScreen

        self.screen_manager.show(HelpScreen)

    def abrir_sobre(self):
        print("Abrir sobre")

        from client.ui.about_screen import AboutScreen

        self.screen_manager.show(AboutScreen)

    def sair(self):
        self.screen_manager.root.destroy()
