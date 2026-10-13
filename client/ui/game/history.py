"""Construção do painel de histórico da partida."""

import tkinter as tk
from tkinter import ttk


class GameHistoryMixin:
    def criar_historico(self, parent):

        cabecalho = tk.Frame(
            parent,
            bg=self.PANEL
        )

        cabecalho.pack(
            fill="x",
            padx=22,
            pady=(20, 10)
        )

        tk.Label(
            cabecalho,
            text="HISTÓRICO",
            font=("Arial", 10, "bold"),
            bg=self.PANEL,
            fg=self.PURPLE
        ).pack(
            anchor="w"
        )

        tk.Label(
            cabecalho,
            text="Suas palavras e posições no ranking",
            font=("Arial", 12, "bold"),
            bg=self.PANEL,
            fg=self.WHITE
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ------------------------------------------------------
        # TABELA
        # ------------------------------------------------------

        area = tk.Frame(
            parent,
            bg=self.PANEL
        )

        area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        colunas = (
            "ordem",
            "palavra",
            "posicao",
            "proximidade"
        )

        self.tabela = ttk.Treeview(
            area,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        self.tabela.heading(
            "ordem",
            text="#"
        )

        self.tabela.heading(
            "palavra",
            text="PALAVRA"
        )

        self.tabela.heading(
            "posicao",
            text="POSIÇÃO"
        )

        self.tabela.heading(
            "proximidade",
            text="PROXIMIDADE"
        )

        self.tabela.column(
            "ordem",
            width=55,
            minwidth=45,
            anchor="center"
        )

        self.tabela.column(
            "palavra",
            width=180,
            minwidth=120,
            anchor="center"
        )

        self.tabela.column(
            "posicao",
            width=120,
            minwidth=90,
            anchor="center"
        )

        self.tabela.column(
            "proximidade",
            width=130,
            minwidth=100,
            anchor="center"
        )

        # ------------------------------------------------------
        # ESTILOS
        # ------------------------------------------------------

        style = ttk.Style()

        try:

            style.theme_use(
                "clam"
            )

        except tk.TclError:

            pass

        style.configure(
            "Treeview",
            background=self.BG_DARK,
            foreground=self.TEXT,
            fieldbackground=self.BG_DARK,
            rowheight=38,
            borderwidth=0,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.PANEL_LIGHT,
            foreground=self.WHITE,
            relief="flat",
            font=("Arial", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    "#334155"
                )
            ],
            foreground=[
                (
                    "selected",
                    self.WHITE
                )
            ]
        )

        # Tentativas
        self.tabela.tag_configure(
            "tentativa",
            background=self.BG_DARK,
            foreground=self.TEXT
        )

        # Dicas
        self.tabela.tag_configure(
            "dica",
            background="#281b45",
            foreground="#c4b5fd"
        )

        # Vitória
        self.tabela.tag_configure(
            "vitoria",
            background="#123524",
            foreground="#86efac"
        )

        # ------------------------------------------------------
        # SCROLL
        # ------------------------------------------------------

        barra = ttk.Scrollbar(
            area,
            orient="vertical",
            command=self.tabela.yview
        )

        self.tabela.configure(
            yscrollcommand=barra.set
        )

        self.tabela.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )
