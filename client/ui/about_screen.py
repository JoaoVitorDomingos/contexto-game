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


class AboutScreen(tk.Frame):

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
            text="SOBRE O PROJETO",
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
        # CONTEÚDO DO CANVAS
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

        # Atualiza a área de rolagem
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
            text="Sobre",
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
            pady=(0, 35)
        )

        # =========================================================
        # CARD PRINCIPAL
        # =========================================================

        card = tk.Frame(
            conteudo,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=100,
            pady=(0, 25)
        )

        # =========================================================
        # NOME DO JOGO
        # =========================================================

        tk.Label(
            card,
            text=NOME_DO_JOGO,
            font=("Arial", 25, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(
            pady=(30, 5)
        )

        tk.Label(
            card,
            text="Jogo de descoberta semântica",
            font=("Arial", 11),
            bg=PANEL,
            fg=TEXT_MUTED
        ).pack(
            pady=(0, 25)
        )

        # Separador
        tk.Frame(
            card,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=40
        )

        # =========================================================
        # INTEGRANTES
        # =========================================================

        tk.Label(
            card,
            text="INTEGRANTES",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack(
            pady=(25, 10)
        )

        tk.Label(
            card,
            text=(
                f"{NOME_INTEGRANTE_1}\n"
                f"{NOME_INTEGRANTE_2}"
            ),
            font=("Arial", 13),
            bg=PANEL,
            fg=TEXT,
            justify="center"
        ).pack(
            pady=(0, 25)
        )

        # =========================================================
        # DISCIPLINAS
        # =========================================================

        tk.Frame(
            card,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=40
        )

        tk.Label(
            card,
            text="DISCIPLINAS",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack(
            pady=(25, 10)
        )

        tk.Label(
            card,
            text=(
                f"{NOME_DISCIPLINA_1}\n"
                f"{NOME_DISCIPLINA_2}"
            ),
            font=("Arial", 12),
            bg=PANEL,
            fg=TEXT,
            justify="center"
        ).pack(
            pady=(0, 20)
        )

        # =========================================================
        # CURSO
        # =========================================================

        tk.Label(
            card,
            text="CURSO",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack(
            pady=(10, 8)
        )

        tk.Label(
            card,
            text=NOME_CURSO,
            font=("Arial", 12),
            bg=PANEL,
            fg=TEXT,
            justify="center",
            wraplength=750
        ).pack(
            pady=(0, 20)
        )

        # =========================================================
        # UNIVERSIDADE
        # =========================================================

        tk.Frame(
            card,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=40
        )

        tk.Label(
            card,
            text="INSTITUIÇÃO",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack(
            pady=(25, 8)
        )

        tk.Label(
            card,
            text=NOME_UNIVERSIDADE,
            font=("Arial", 13, "bold"),
            bg=PANEL,
            fg=WHITE,
            justify="center",
            wraplength=750
        ).pack(
            pady=(0, 30)
        )

        # =========================================================
        # INFORMAÇÃO ADICIONAL
        # =========================================================

        info = tk.Frame(
            conteudo,
            bg=PANEL_LIGHT,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        info.pack(
            fill="x",
            padx=100,
            pady=(0, 25)
        )

        tk.Label(
            info,
            text="SOBRE O PROJETO",
            font=("Arial", 10, "bold"),
            bg=PANEL_LIGHT,
            fg=PURPLE
        ).pack(
            pady=(18, 8)
        )

        tk.Label(
            info,
            text=(
                "Projeto acadêmico desenvolvido para aplicação dos "
                "conceitos de Inteligência Artificial, Redes de "
                "Computadores e Sistemas Distribuídos."
            ),
            font=("Arial", 11),
            bg=PANEL_LIGHT,
            fg=TEXT,
            justify="center",
            wraplength=750
        ).pack(
            padx=25,
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
            pady=(5, 40)
        )

        # =========================================================
        # RODAPÉ
        # =========================================================

        tk.Label(
            conteudo,
            text=f"{NOME_DO_JOGO} • {NOME_UNIVERSIDADE}",
            font=("Arial", 9),
            bg=BG,
            fg=TEXT_MUTED
        ).pack(
            pady=(0, 25)
        )

        # =========================================================
        # SCROLL COM MOUSE
        # =========================================================

        def scroll_mouse(event):

            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        # Canvas e conteúdo
        canvas.bind(
            "<MouseWheel>",
            scroll_mouse
        )

        conteudo.bind(
            "<MouseWheel>",
            scroll_mouse
        )

        # Permite rolagem ao passar o mouse pelos elementos
        def configurar_scroll(widget):

            widget.bind(
                "<MouseWheel>",
                scroll_mouse
            )

            for filho in widget.winfo_children():
                configurar_scroll(filho)

        configurar_scroll(conteudo)

        # =========================================================
        # HOME / TOPO AO ABRIR
        # =========================================================

        canvas.yview_moveto(0)

    # =============================================================
    # VOLTAR AO MENU
    # =============================================================

    def voltar(self):

        from client.ui.menu import Menu

        self.screen_manager.show(Menu)