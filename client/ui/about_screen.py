import tkinter as tk

from shared.constants import (
    NOME_DO_JOGO,
    NOME_INTEGRANTE_1,
    NOME_INTEGRANTE_2,
    NOME_DISCIPLINA_1,
    NOME_DISCIPLINA_2,
    NOME_CURSO,
    NOME_UNIVERSIDADE
)


class AboutScreen(tk.Frame):
    def __init__(self, root, screen_manager):
        super().__init__(root)

        self.screen_manager = screen_manager

        self.criar_interface()

    def criar_interface(self):
        titulo = tk.Label(
            self,
            text="Sobre",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=(50, 30))

        nome_jogo = tk.Label(
            self,
            text=NOME_DO_JOGO,
            font=("Arial", 20, "bold")
        )
        nome_jogo.pack(pady=10)

        integrantes = tk.Label(
            self,
            text=(
                "Integrantes:\n\n"
                f"{NOME_INTEGRANTE_1}\n"
                f"{NOME_INTEGRANTE_2}"
            ),
            font=("Arial", 14),
            justify="center"
        )
        integrantes.pack(pady=20)

        disciplinas = tk.Label(
            self,
            text=(
                f"Disciplinas:\n\n"
                f"{NOME_DISCIPLINA_1}\n"
                f"{NOME_DISCIPLINA_2}\n\n"
                f"{NOME_CURSO}\n"
                f"{NOME_UNIVERSIDADE}"
            ),
            font=("Arial", 13),
            justify="center"
        )
        disciplinas.pack(pady=20)

        botao_voltar = tk.Button(
            self,
            text="Voltar",
            width=25,
            height=2,
            command=self.voltar
        )
        botao_voltar.pack(pady=30)

    def voltar(self):
        from client.ui.menu import Menu

        self.screen_manager.show(Menu)