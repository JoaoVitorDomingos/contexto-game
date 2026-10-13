"""Painéis de entrada, estatísticas e ações da tela de jogo."""

import tkinter as tk
from client.ui.loading_spinner import LoadingSpinner


class GamePanelsMixin:
    def criar_painel_entrada(self, parent):

        painel = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        painel.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            painel,
            text="SUA TENTATIVA",
            font=("Arial", 10, "bold"),
            bg=self.PANEL,
            fg=self.PURPLE
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 4)
        )

        tk.Label(
            painel,
            text="Digite uma palavra",
            font=("Arial", 18, "bold"),
            bg=self.PANEL,
            fg=self.WHITE
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 14)
        )

        linha = tk.Frame(
            painel,
            bg=self.PANEL
        )

        linha.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        # ------------------------------------------------------
        # CAMPO
        # ------------------------------------------------------

        campo_frame = tk.Frame(
            linha,
            bg=self.BG_DARK
        )

        campo_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.campo_palavra = tk.Entry(
            campo_frame,
            font=("Arial", 16),
            bg=self.BG_DARK,
            fg=self.WHITE,
            insertbackground=self.WHITE,
            relief="flat",
            bd=0
        )

        self.campo_palavra.pack(
            fill="x",
            ipady=13,
            padx=15
        )

        self.campo_palavra.bind(
            "<Return>",
            lambda event: self.enviar_tentativa()
        )

        # ------------------------------------------------------
        # BOTÃO ENVIAR
        # ------------------------------------------------------

        self.botao_enviar = tk.Button(
            linha,
            text="ENVIAR  →",
            width=14,
            font=("Arial", 11, "bold"),
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.BLUE_HOVER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.enviar_tentativa
        )

        self.botao_enviar.pack(
            side="left",
            padx=(12, 0),
            ipady=10
        )

        self.loading_spinner = LoadingSpinner(
            self.botao_enviar,
            "ENVIAR  →",
            "ENVIANDO..."
        )

    def criar_cards(self, parent):

        area = tk.Frame(
            parent,
            bg=self.BG
        )

        area.pack(
            fill="x",
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # CARD POSIÇÃO
        # ------------------------------------------------------

        self.card_posicao = tk.Frame(
            area,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        self.card_posicao.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        tk.Label(
            self.card_posicao,
            text="ÚLTIMA POSIÇÃO",
            font=("Arial", 9, "bold"),
            bg=self.PANEL,
            fg=self.TEXT_MUTED
        ).pack(
            pady=(18, 4)
        )

        self.label_posicao = tk.Label(
            self.card_posicao,
            text="—",
            font=("Arial", 30, "bold"),
            bg=self.PANEL,
            fg=self.BLUE
        )

        self.label_posicao.pack(
            pady=(0, 4)
        )

        tk.Label(
            self.card_posicao,
            text="quanto menor, melhor",
            font=("Arial", 8),
            bg=self.PANEL,
            fg=self.TEXT_MUTED
        ).pack(
            pady=(0, 18)
        )

        # ------------------------------------------------------
        # CARD PROXIMIDADE
        # ------------------------------------------------------

        self.card_proximidade = tk.Frame(
            area,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        self.card_proximidade.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            self.card_proximidade,
            text="PROXIMIDADE",
            font=("Arial", 9, "bold"),
            bg=self.PANEL,
            fg=self.TEXT_MUTED
        ).pack(
            pady=(18, 4)
        )

        self.label_proximidade = tk.Label(
            self.card_proximidade,
            text="—",
            font=("Arial", 30, "bold"),
            bg=self.PANEL,
            fg=self.PURPLE
        )

        self.label_proximidade.pack(
            pady=(0, 4)
        )

        tk.Label(
            self.card_proximidade,
            text="similaridade semântica",
            font=("Arial", 8),
            bg=self.PANEL,
            fg=self.TEXT_MUTED
        ).pack(
            pady=(0, 18)
        )

        # ------------------------------------------------------
        # MENSAGEM
        # ------------------------------------------------------

        self.label_status = tk.Label(
            parent,
            text="Preparando partida...",
            font=("Arial", 10),
            bg=self.BG,
            fg=self.TEXT_MUTED,
            wraplength=700
        )

        self.label_status.pack(
            pady=(0, 5)
        )

        # ------------------------------------------------------
        # DICA
        # ------------------------------------------------------

        self.label_dica = tk.Label(
            parent,
            text="",
            font=("Arial", 10, "bold"),
            bg=self.BG,
            fg=self.PURPLE,
            wraplength=700
        )

        self.label_dica.pack(
            pady=(0, 5)
        )

    def criar_rodape(self):

        rodape = tk.Frame(
            self.container,
            bg=self.BG_DARK,
            height=78
        )

        rodape.pack(
            side="bottom",
            fill="x"
        )

        rodape.pack_propagate(
            False
        )

        area = tk.Frame(
            rodape,
            bg=self.BG_DARK
        )

        area.pack(
            pady=15
        )

        # ------------------------------------------------------
        # DICA
        # ------------------------------------------------------

        self.botao_dica = tk.Button(
            area,
            text="💡  DICA",
            width=14,
            font=("Arial", 10, "bold"),
            bg=self.PURPLE,
            fg=self.WHITE,
            activebackground=self.PURPLE_HOVER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.solicitar_dica
        )

        self.botao_dica.pack(
            side="left",
            padx=5,
            ipady=7
        )

        self.spinner_dica = LoadingSpinner(
            self.botao_dica,
            "💡  DICA",
            "BUSCANDO..."
        )

        # ------------------------------------------------------
        # DESISTIR
        # ------------------------------------------------------

        self.botao_desistir = tk.Button(
            area,
            text="🏳  DESISTIR",
            width=14,
            font=("Arial", 10, "bold"),
            bg=self.RED,
            fg=self.WHITE,
            activebackground=self.RED_HOVER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.desistir
        )

        self.botao_desistir.pack(
            side="left",
            padx=5,
            ipady=7
        )

        self.spinner_desistir = LoadingSpinner(
            self.botao_desistir,
            "🏳  DESISTIR",
            "ENCERRANDO..."
        )

        # ------------------------------------------------------
        # NOVA PARTIDA
        # ------------------------------------------------------

        self.botao_nova_partida = tk.Button(
            area,
            text="↻  NOVA PARTIDA",
            width=16,
            font=("Arial", 10, "bold"),
            bg=self.GREEN,
            fg=self.WHITE,
            activebackground=self.GREEN_HOVER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.nova_partida
        )

        # Fica oculto inicialmente.

        # ------------------------------------------------------
        # MENU
        # ------------------------------------------------------

        self.botao_menu = tk.Button(
            area,
            text="←  MENU",
            width=12,
            font=("Arial", 10, "bold"),
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground=self.BORDER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.voltar_menu
        )

        self.botao_menu.pack(
            side="left",
            padx=5,
            ipady=7
        )
