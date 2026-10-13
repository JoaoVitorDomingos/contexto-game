"""Estrutura geral e cabeçalho da tela de jogo."""

import tkinter as tk
from shared.constants import NOME_DO_JOGO


class GameLayoutMixin:
    def criar_interface(self):

        # ------------------------------------------------------
        # CONTAINER PRINCIPAL
        # ------------------------------------------------------

        self.container = tk.Frame(
            self,
            bg=self.BG
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # CABEÇALHO
        # ------------------------------------------------------

        self.criar_cabecalho()

        # ------------------------------------------------------
        # CONTEÚDO
        # ------------------------------------------------------

        conteudo = tk.Frame(
            self.container,
            bg=self.BG
        )

        conteudo.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=(10, 20)
        )

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        titulo = tk.Label(
            conteudo,
            text="Descubra a palavra secreta",
            font=("Arial", 24, "bold"),
            bg=self.BG,
            fg=self.WHITE
        )

        titulo.pack(
            pady=(0, 4)
        )

        subtitulo = tk.Label(
            conteudo,
            text=(
                "Quanto menor a posição no ranking, "
                "mais próxima sua palavra está da resposta."
            ),
            font=("Arial", 11),
            bg=self.BG,
            fg=self.TEXT_MUTED
        )

        subtitulo.pack(
            pady=(0, 18)
        )

        # ------------------------------------------------------
        # ÁREA PRINCIPAL
        # ------------------------------------------------------

        area_principal = tk.Frame(
            conteudo,
            bg=self.BG
        )

        area_principal.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # PAINEL ESQUERDO
        # ------------------------------------------------------

        painel_esquerdo = tk.Frame(
            area_principal,
            bg=self.BG
        )

        painel_esquerdo.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )

        self.criar_painel_entrada(
            painel_esquerdo
        )

        self.criar_cards(
            painel_esquerdo
        )

        # ------------------------------------------------------
        # PAINEL DIREITO
        # ------------------------------------------------------

        painel_direito = tk.Frame(
            area_principal,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        painel_direito.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(12, 0)
        )

        self.criar_historico(
            painel_direito
        )

        # ------------------------------------------------------
        # RODAPÉ
        # ------------------------------------------------------

        self.criar_rodape()

        # Estado inicial
        self._atualizar_estado_botoes(
            False
        )

    def criar_cabecalho(self):

        cabecalho = tk.Frame(
            self.container,
            bg=self.BG_DARK,
            height=80
        )

        cabecalho.pack(
            fill="x"
        )

        cabecalho.pack_propagate(
            False
        )

        # ------------------------------------------------------
        # ESQUERDA
        # ------------------------------------------------------

        esquerda = tk.Frame(
            cabecalho,
            bg=self.BG_DARK
        )

        esquerda.pack(
            side="left",
            padx=45
        )

        tk.Label(
            esquerda,
            text=NOME_DO_JOGO,
            font=("Arial", 25, "bold"),
            bg=self.BG_DARK,
            fg=self.WHITE
        ).pack(
            side="left"
        )

        tk.Label(
            esquerda,
            text="  •  JOGO SEMÂNTICO",
            font=("Arial", 9, "bold"),
            bg=self.BG_DARK,
            fg=self.PURPLE
        ).pack(
            side="left",
            pady=8
        )

        # ------------------------------------------------------
        # DIREITA
        # ------------------------------------------------------

        direita = tk.Frame(
            cabecalho,
            bg=self.BG_DARK
        )

        direita.pack(
            side="right",
            padx=45
        )

        self.label_status_conexao = tk.Label(
            direita,
            text="●  Conectando...",
            font=("Arial", 10, "bold"),
            bg=self.BG_DARK,
            fg="#f59e0b"
        )

        self.label_status_conexao.pack(
            side="left",
            padx=(0, 20)
        )

        tk.Label(
            direita,
            text="ESC  Tela cheia",
            font=("Arial", 9),
            bg=self.BG_DARK,
            fg=self.TEXT_MUTED
        ).pack(
            side="left"
        )
