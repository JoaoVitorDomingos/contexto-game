import tkinter as tk

from shared.constants import NOME_DO_JOGO


# =========================
# CORES
# =========================

BG = "#0f172a"
BG_DARK = "#0b1120"
PANEL = "#1e293b"
PANEL_LIGHT = "#263449"

WHITE = "#f8fafc"
TEXT = "#e2e8f0"
TEXT_MUTED = "#94a3b8"

PURPLE = "#8b5cf6"
PURPLE_HOVER = "#7c3aed"

BORDER = "#334155"


class HelpScreen(tk.Frame):

    def __init__(self, root, screen_manager):

        super().__init__(
            root,
            bg=BG
        )

        self.screen_manager = screen_manager
        self.root = root

        self.criar_interface()

    def criar_interface(self):

        # =========================================================
        # CABEÇALHO
        # =========================================================

        header = tk.Frame(
            self,
            bg=BG_DARK,
            height=90
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text=NOME_DO_JOGO,
            font=("Arial", 20, "bold"),
            bg=BG_DARK,
            fg=WHITE
        ).pack(
            side="left",
            padx=35
        )

        tk.Label(
            header,
            text="COMO JOGAR",
            font=("Arial", 10, "bold"),
            bg=BG_DARK,
            fg=PURPLE
        ).pack(
            side="right",
            padx=35
        )

        # =========================================================
        # ÁREA PRINCIPAL
        # =========================================================

        area = tk.Frame(
            self,
            bg=BG
        )

        area.pack(
            fill="both",
            expand=True
        )

        # =========================================================
        # CANVAS
        # =========================================================

        canvas = tk.Canvas(
            area,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            area,
            orient="vertical",
            command=canvas.yview,
            bg=PANEL,
            troughcolor=BG_DARK,
            activebackground=PURPLE,
            relief="flat"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =========================================================
        # CONTEÚDO
        # =========================================================

        conteudo = tk.Frame(
            canvas,
            bg=BG
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=conteudo,
            anchor="n"
        )

        # Atualiza a região de rolagem
        def atualizar_scroll(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        conteudo.bind(
            "<Configure>",
            atualizar_scroll
        )

        # Faz o conteúdo ocupar toda a largura
        def ajustar_largura(event):

            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            ajustar_largura
        )

        # =========================================================
        # TÍTULO
        # =========================================================

        tk.Label(
            conteudo,
            text="Como jogar?",
            font=("Arial", 30, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            pady=(40, 8)
        )

        # Linha decorativa
        tk.Frame(
            conteudo,
            bg=PURPLE,
            height=4,
            width=80
        ).pack(
            pady=(0, 12)
        )

        tk.Label(
            conteudo,
            text=(
                "Descubra a palavra secreta através "
                "da proximidade semântica."
            ),
            font=("Arial", 12),
            bg=BG,
            fg=TEXT_MUTED
        ).pack(
            pady=(0, 30)
        )

        # =========================================================
        # CARDS DE INSTRUÇÃO
        # =========================================================

        self.criar_card(
            conteudo,
            "01",
            "Faça uma tentativa",
            (
                "Digite uma palavra no campo de tentativa "
                "e clique em \"Enviar tentativa\"."
            )
        )

        self.criar_card(
            conteudo,
            "02",
            "Observe a posição",
            (
                "O jogo informa a posição da sua palavra no "
                "ranking de proximidade em relação à palavra secreta.\n\n"
                "Quanto mais próxima a posição estiver de 1, "
                "mais próxima sua palavra está da solução."
            )
        )

        self.criar_card(
            conteudo,
            "03",
            "Continue tentando",
            (
                "Use as palavras anteriores como referência e tente "
                "encontrar palavras cada vez mais próximas semanticamente "
                "da palavra secreta."
            )
        )

        self.criar_card(
            conteudo,
            "04",
            "Use uma dica",
            (
                "Você pode solicitar uma dica durante a partida.\n\n"
                "A dica apresenta uma palavra semanticamente próxima "
                "da solução, sem revelar diretamente a palavra secreta."
            )
        )

        self.criar_card(
            conteudo,
            "05",
            "Desista quando quiser",
            (
                "Caso queira encerrar a partida, utilize o botão "
                "\"Desistir\".\n\n"
                "A palavra secreta será revelada junto com as "
                "palavras mais próximas da solução."
            )
        )

        # =========================================================
        # DICA EXTRA
        # =========================================================

        observacao = tk.Frame(
            conteudo,
            bg=PANEL_LIGHT,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        observacao.pack(
            fill="x",
            padx=100,
            pady=(15, 25)
        )

        tk.Label(
            observacao,
            text="💡  DICA",
            font=("Arial", 11, "bold"),
            bg=PANEL_LIGHT,
            fg=PURPLE
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 7)
        )

        tk.Label(
            observacao,
            text=(
                "Não procure apenas sinônimos. Pense em palavras "
                "que tenham relação com o mesmo contexto ou assunto."
            ),
            font=("Arial", 11),
            bg=PANEL_LIGHT,
            fg=TEXT,
            justify="left",
            anchor="w",
            wraplength=800
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 18)
        )

        # =========================================================
        # BOTÃO VOLTAR
        # =========================================================

        botao_voltar = tk.Button(
            conteudo,
            text="←  VOLTAR AO MENU",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=WHITE,
            activebackground=PANEL_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=24,
            height=2,
            command=self.voltar
        )

        botao_voltar.pack(
            pady=(5, 25)
        )

        # =========================================================
        # RODAPÉ
        # =========================================================

        tk.Label(
            conteudo,
            text=f"{NOME_DO_JOGO} • UNESPAR",
            font=("Arial", 9),
            bg=BG,
            fg=TEXT_MUTED
        ).pack(
            pady=(0, 35)
        )

        # =========================================================
        # SCROLL COM MOUSE
        # =========================================================

        def scroll_mouse(event):

            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        # Registra o scroll em todos os widgets
        def configurar_scroll(widget):

            widget.bind(
                "<MouseWheel>",
                scroll_mouse
            )

            for filho in widget.winfo_children():
                configurar_scroll(filho)

        canvas.bind(
            "<MouseWheel>",
            scroll_mouse
        )

        configurar_scroll(conteudo)

        # =========================================================
        # COMEÇAR SEMPRE NO TOPO
        # =========================================================

        canvas.yview_moveto(0)

    # =============================================================
    # CRIAR CARD
    # =============================================================

    def criar_card(
        self,
        parent,
        numero,
        titulo,
        texto
    ):

        card = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=100,
            pady=7
        )

        # Número
        numero_label = tk.Label(
            card,
            text=numero,
            font=("Arial", 12, "bold"),
            bg=PURPLE,
            fg=WHITE,
            width=4,
            height=2
        )

        numero_label.pack(
            side="left",
            padx=(18, 15),
            pady=18
        )

        # Área do texto
        area_texto = tk.Frame(
            card,
            bg=PANEL
        )

        area_texto.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 20),
            pady=16
        )

        tk.Label(
            area_texto,
            text=titulo,
            font=("Arial", 13, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        tk.Label(
            area_texto,
            text=texto,
            font=("Arial", 11),
            bg=PANEL,
            fg=TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=750
        ).pack(
            anchor="w"
        )

    # =============================================================
    # VOLTAR AO MENU
    # =============================================================

    def voltar(self):

        from client.ui.menu import Menu

        self.screen_manager.show(Menu)