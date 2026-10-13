"""Componentes de carregamento da tela de jogo."""

import tkinter as tk
from client.ui.loading_spinner import LoadingSpinner
from shared.constants import NOME_DO_JOGO


class GameLoadingMixin:
    def criar_loading_partida(self):

        self.loading_partida_frame = tk.Frame(
            self,
            bg=self.BG_DARK
        )

        self.loading_partida_frame.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        conteudo = tk.Frame(
            self.loading_partida_frame,
            bg=self.BG_DARK
        )

        conteudo.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            conteudo,
            text=NOME_DO_JOGO,
            font=("Arial", 32, "bold"),
            bg=self.BG_DARK,
            fg=self.WHITE
        ).pack(
            pady=(0, 15)
        )

        self.label_loading_partida = tk.Label(
            conteudo,
            text="◐ INICIANDO...",
            font=("Arial", 18, "bold"),
            bg=self.BG_DARK,
            fg=self.PURPLE
        )

        self.label_loading_partida.pack(
            pady=8
        )

        tk.Label(
            conteudo,
            text="Preparando uma nova partida...",
            font=("Arial", 11),
            bg=self.BG_DARK,
            fg=self.TEXT_MUTED
        ).pack()

        self.spinner_partida = LoadingSpinner(
            self.label_loading_partida,
            "◐ INICIANDO...",
            "INICIANDO..."
        )

    def _mostrar_loading_partida(self, mostrar):

        if mostrar:

            self.loading_partida_frame.place(
                relx=0,
                rely=0,
                relwidth=1,
                relheight=1
            )

            self.loading_partida_frame.lift()

            self.spinner_partida.start()

        else:

            self.spinner_partida.stop()

            self.loading_partida_frame.place_forget()
