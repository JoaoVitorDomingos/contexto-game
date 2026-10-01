import tkinter as tk

from shared.constants import NOME_DO_JOGO


class Menu(tk.Frame):

    # ==========================================================
    # CORES
    # ==========================================================

    BG = "#0f172a"
    BG_DARK = "#0b1120"
    PANEL = "#1e293b"
    PANEL_LIGHT = "#263449"

    WHITE = "#f8fafc"
    TEXT = "#e2e8f0"
    TEXT_MUTED = "#94a3b8"

    BLUE = "#3b82f6"
    BLUE_HOVER = "#2563eb"

    PURPLE = "#8b5cf6"
    PURPLE_HOVER = "#7c3aed"

    RED = "#ef4444"
    RED_HOVER = "#dc2626"

    BORDER = "#334155"

    def __init__(
        self,
        root,
        screen_manager
    ):

        super().__init__(
            root,
            bg=self.BG
        )

        self.screen_manager = screen_manager
        self.root = root

        self.root.title(
            NOME_DO_JOGO
        )

        # ------------------------------------------------------
        # Janela em tela cheia
        # ------------------------------------------------------

        self.root.attributes(
            "-fullscreen",
            True
        )

        # Permite sair da tela cheia com ESC
        self.root.bind(
            "<Escape>",
            self.alternar_tela_cheia
        )

        self.criar_interface()

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def criar_interface(self):

        # ------------------------------------------------------
        # CONTAINER
        # ------------------------------------------------------

        container = tk.Frame(
            self,
            bg=self.BG
        )

        container.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # TOPO
        # ------------------------------------------------------

        topo = tk.Frame(
            container,
            bg=self.BG_DARK,
            height=65
        )

        topo.pack(
            fill="x"
        )

        topo.pack_propagate(
            False
        )

        tk.Label(
            topo,
            text=NOME_DO_JOGO,
            font=("Arial", 14, "bold"),
            bg=self.BG_DARK,
            fg=self.WHITE
        ).pack(
            side="left",
            padx=35
        )

        tk.Label(
            topo,
            text="JOGO DE DESCOBERTA SEMÂNTICA",
            font=("Arial", 9, "bold"),
            bg=self.BG_DARK,
            fg=self.TEXT_MUTED
        ).pack(
            side="left"
        )

        # ------------------------------------------------------
        # ÁREA CENTRAL
        # ------------------------------------------------------

        centro = tk.Frame(
            container,
            bg=self.BG
        )

        centro.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # CONTEÚDO CENTRAL
        # ------------------------------------------------------

        conteudo = tk.Frame(
            centro,
            bg=self.BG
        )

        conteudo.place(
            relx=0.5,
            rely=0.48,
            anchor="center"
        )

        # ------------------------------------------------------
        # PEQUENO TÍTULO
        # ------------------------------------------------------

        tk.Label(
            conteudo,
            text="BEM-VINDO AO",
            font=("Arial", 11, "bold"),
            bg=self.BG,
            fg=self.PURPLE
        ).pack(
            pady=(0, 5)
        )

        # ------------------------------------------------------
        # NOME DO JOGO
        # ------------------------------------------------------

        tk.Label(
            conteudo,
            text=NOME_DO_JOGO,
            font=("Arial", 52, "bold"),
            bg=self.BG,
            fg=self.WHITE
        ).pack(
            pady=(0, 8)
        )

        # ------------------------------------------------------
        # LINHA DECORATIVA
        # ------------------------------------------------------

        linha = tk.Frame(
            conteudo,
            bg=self.PURPLE,
            height=3,
            width=80
        )

        linha.pack(
            pady=(0, 15)
        )

        linha.pack_propagate(
            False
        )

        # ------------------------------------------------------
        # SUBTÍTULO
        # ------------------------------------------------------

        tk.Label(
            conteudo,
            text="Descubra a palavra. Siga o contexto.",
            font=("Arial", 16),
            bg=self.BG,
            fg=self.TEXT
        ).pack()

        tk.Label(
            conteudo,
            text=(
                "Encontre a palavra secreta usando "
                "proximidade e contexto semântico."
            ),
            font=("Arial", 10),
            bg=self.BG,
            fg=self.TEXT_MUTED
        ).pack(
            pady=(6, 28)
        )

        # ------------------------------------------------------
        # BOTÃO PRINCIPAL
        # ------------------------------------------------------

        self.botao_iniciar = tk.Button(
            conteudo,
            text="▶   INICIAR JOGO",
            width=25,
            font=("Arial", 12, "bold"),
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.BLUE_HOVER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.iniciar_jogo
        )

        self.botao_iniciar.pack(
            ipady=12,
            pady=(0, 12)
        )

        # ------------------------------------------------------
        # OUTROS BOTÕES
        # ------------------------------------------------------

        botoes_secundarios = tk.Frame(
            conteudo,
            bg=self.BG
        )

        botoes_secundarios.pack()

        self._criar_botao_secundario(
            botoes_secundarios,
            "▣   AJUDA",
            self.abrir_ajuda
        ).pack(
            side="left",
            padx=5
        )

        self._criar_botao_secundario(
            botoes_secundarios,
            "ⓘ   SOBRE",
            self.abrir_sobre
        ).pack(
            side="left",
            padx=5
        )

        self._criar_botao_secundario(
            botoes_secundarios,
            "✕   SAIR",
            self.sair,
            vermelho=True
        ).pack(
            side="left",
            padx=5
        )

        # ------------------------------------------------------
        # RODAPÉ
        # ------------------------------------------------------

        rodape = tk.Frame(
            container,
            bg=self.BG_DARK,
            height=50
        )

        rodape.pack(
            fill="x",
            side="bottom"
        )

        rodape.pack_propagate(
            False
        )

        tk.Label(
            rodape,
            text="PONTEXTO  •  UNESPAR",
            font=("Arial", 9, "bold"),
            bg=self.BG_DARK,
            fg=self.TEXT_MUTED
        ).pack(
            side="left",
            padx=35
        )

        tk.Label(
            rodape,
            text="Descubra. Compare. Encontre.",
            font=("Arial", 9),
            bg=self.BG_DARK,
            fg=self.TEXT_MUTED
        ).pack(
            side="right",
            padx=35
        )

    # ==========================================================
    # BOTÃO SECUNDÁRIO
    # ==========================================================

    def _criar_botao_secundario(
        self,
        parent,
        texto,
        comando,
        vermelho=False
    ):

        if vermelho:

            bg = self.PANEL
            hover = self.RED_HOVER
            fg = "#fca5a5"

        else:

            bg = self.PANEL
            hover = self.PANEL_LIGHT
            fg = self.TEXT

        botao = tk.Button(
            parent,
            text=texto,
            width=13,
            font=("Arial", 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=comando
        )

        botao.config(
            padx=5,
            pady=9
        )

        return botao

    # ==========================================================
    # TELA CHEIA
    # ==========================================================

    def alternar_tela_cheia(self, event=None):

        estado_atual = self.root.attributes(
            "-fullscreen"
        )

        self.root.attributes(
            "-fullscreen",
            not estado_atual
        )

    # ==========================================================
    # INICIAR JOGO
    # ==========================================================

    def iniciar_jogo(self):

        from client.ui.game_screen import GameScreen

        self.screen_manager.show(
            GameScreen
        )

    # ==========================================================
    # AJUDA
    # ==========================================================

    def abrir_ajuda(self):

        from client.ui.help_screen import HelpScreen

        self.screen_manager.show(
            HelpScreen
        )

    # ==========================================================
    # SOBRE
    # ==========================================================

    def abrir_sobre(self):

        from client.ui.about_screen import AboutScreen

        self.screen_manager.show(
            AboutScreen
        )

    # ==========================================================
    # SAIR
    # ==========================================================

    def sair(self):

        self.screen_manager.root.destroy()