import tkinter as tk
from tkinter import ttk

from shared.constants import NOME_DO_JOGO


class GameScreen(tk.Frame):
    def __init__(self, root, screen_manager):
        super().__init__(root)

        self.screen_manager = screen_manager

        self.criar_interface()

    def criar_interface(self):
        # =========================
        # TÍTULO
        # =========================

        titulo = tk.Label(
            self,
            text=NOME_DO_JOGO,
            font=("Arial", 28, "bold")
        )

        titulo.pack(pady=(40, 20))

        # =========================
        # CAMPO DE PALAVRA
        # =========================

        self.campo_palavra = tk.Entry(
            self,
            font=("Arial", 14),
            width=30
        )

        self.campo_palavra.pack(pady=10)

        # =========================
        # BOTÃO ENVIAR
        # =========================

        botao_enviar = tk.Button(
            self,
            text="Enviar",
            width=20,
            height=2,
            command=self.enviar_tentativa
        )

        botao_enviar.pack(pady=5)

        # =========================
        # ÁREA DA TABELA
        # =========================

        area_tabela = tk.Frame(self)

        area_tabela.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=20
        )

        # =========================
        # TABELA
        # =========================

        colunas = (
            "palavra",
            "posicao",
            "proximidade"
        )

        self.tabela = ttk.Treeview(
            area_tabela,
            columns=colunas,
            show="headings",
            height=10
        )

        # Cabeçalhos

        self.tabela.heading(
            "palavra",
            text="Palavra"
        )

        self.tabela.heading(
            "posicao",
            text="Posição no ranking"
        )

        self.tabela.heading(
            "proximidade",
            text="Proximidade"
        )

        # Largura das colunas

        self.tabela.column(
            "palavra",
            width=220,
            anchor="center"
        )

        self.tabela.column(
            "posicao",
            width=180,
            anchor="center"
        )

        self.tabela.column(
            "proximidade",
            width=180,
            anchor="center"
        )

        # =========================
        # BARRA DE ROLAGEM
        # =========================

        barra_rolagem = ttk.Scrollbar(
            area_tabela,
            orient="vertical",
            command=self.tabela.yview
        )

        self.tabela.configure(
            yscrollcommand=barra_rolagem.set
        )

        # Tabela

        self.tabela.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollbar

        barra_rolagem.pack(
            side="right",
            fill="y"
        )

        # =========================
        # SCROLL DO MOUSE
        # =========================

        self.tabela.bind(
            "<MouseWheel>",
            self.scroll_mouse
        )

        # =========================
        # DICA
        # =========================

        self.label_dica = tk.Label(
            self,
            text="",
            font=("Arial", 12)
        )

        self.label_dica.pack(
            pady=5
        )

        # =========================
        # BOTÕES
        # =========================

        area_botoes = tk.Frame(self)

        area_botoes.pack(
            pady=10
        )

        botao_dica = tk.Button(
            area_botoes,
            text="Dica",
            width=15,
            command=self.solicitar_dica
        )

        botao_dica.pack(
            side="left",
            padx=5
        )

        botao_desistir = tk.Button(
            area_botoes,
            text="Desistir",
            width=15,
            command=self.desistir
        )

        botao_desistir.pack(
            side="left",
            padx=5
        )

        # =========================
        # STATUS
        # =========================

        self.label_status = tk.Label(
            self,
            text="",
            font=("Arial", 11)
        )

        self.label_status.pack(
            pady=(5, 20)
        )

    # =========================
    # SCROLL DO MOUSE
    # =========================

    def scroll_mouse(self, event):
        self.tabela.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # =========================
    # ENVIAR TENTATIVA
    # =========================

    def enviar_tentativa(self):
        palavra = self.campo_palavra.get().strip()

        if not palavra:
            self.label_status.config(
                text="Digite uma palavra."
            )
            return

        # Simulação temporária

        self.tabela.insert(
            "",
            "end",
            values=(
                palavra,
                "aguardando servidor",
                "aguardando servidor"
            )
        )

        self.campo_palavra.delete(
            0,
            tk.END
        )

        self.label_status.config(
            text=f"Tentativa enviada: {palavra}"
        )

    # =========================
    # SOLICITAR DICA
    # =========================

    def solicitar_dica(self):
        self.label_dica.config(
            text="Dica: aguardando servidor..."
        )

        self.label_status.config(
            text="Solicitação de dica enviada."
        )

    # =========================
    # DESISTIR
    # =========================

    def desistir(self):
        self.label_status.config(
            text="Você desistiu da partida."
        )