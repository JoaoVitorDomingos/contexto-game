import tkinter as tk
from tkinter import ttk, messagebox
import threading

from client.network.rpc_client import RPCClient
from client.ui.loading_spinner import LoadingSpinner
from shared.constants import NOME_DO_JOGO


class GameScreen(tk.Frame):
    """
    Tela principal da partida.

    A lógica da partida permanece no servidor.
    O cliente é responsável pela interface
    e pela comunicação através do RPC.
    """

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

    GREEN = "#22c55e"
    GREEN_HOVER = "#16a34a"

    RED = "#ef4444"
    RED_HOVER = "#dc2626"

    BORDER = "#334155"

    # ==========================================================
    # INICIALIZAÇÃO
    # ==========================================================

    def __init__(self, root, screen_manager):

        super().__init__(
            root,
            bg=self.BG
        )

        self.screen_manager = screen_manager
        self.rpc = RPCClient()

        self.partida_ativa = False
        self._criando_partida = False

        self._enviando_tentativa = False
        self._processando_acao = False

        self.tela_cheia = False

        self.criar_interface()
        self.criar_loading_partida()

        # Tela cheia depois que a janela estiver pronta
        self.after(
            100,
            self._ativar_tela_cheia
        )

        # Inicia a partida
        self.after(
            200,
            self.iniciar_partida
        )

        # ESC alterna tela cheia
        self.winfo_toplevel().bind(
            "<Escape>",
            self.alternar_tela_cheia
        )

    # ==========================================================
    # TELA CHEIA
    # ==========================================================

    def _ativar_tela_cheia(self):

        janela = self.winfo_toplevel()

        try:

            janela.attributes(
                "-fullscreen",
                True
            )

            self.tela_cheia = True

        except tk.TclError:

            pass

    def alternar_tela_cheia(self, event=None):

        janela = self.winfo_toplevel()

        self.tela_cheia = not self.tela_cheia

        try:

            janela.attributes(
                "-fullscreen",
                self.tela_cheia
            )

        except tk.TclError:

            pass

    # ==========================================================
    # INTERFACE
    # ==========================================================

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

    # ==========================================================
    # CABEÇALHO
    # ==========================================================

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

    # ==========================================================
    # PAINEL DE ENTRADA
    # ==========================================================

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

    # ==========================================================
    # CARDS
    # ==========================================================

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

    # ==========================================================
    # HISTÓRICO
    # ==========================================================

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

    # ==========================================================
    # RODAPÉ
    # ==========================================================

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

    # ==========================================================
    # INICIAR PARTIDA
    # ==========================================================

    def iniciar_partida(self):

        if self._criando_partida:
            return

        self._criando_partida = True
        self.partida_ativa = False

        self._atualizar_estado_botoes(
            False
        )

        self._mostrar_loading_partida(
            True
        )

        self.label_status_conexao.config(
            text="●  Conectando...",
            fg="#f59e0b"
        )

        thread = threading.Thread(
            target=self._processar_inicio_partida,
            daemon=True
        )

        thread.start()

    def _processar_inicio_partida(self):

        try:

            if not self.rpc.testar_conexao():

                raise ConnectionError(
                    "Não foi possível conectar ao servidor."
                )

            resultado = self.rpc.iniciar_partida()

            if not resultado.get(
                "sucesso",
                False
            ):

                raise RuntimeError(
                    resultado.get(
                        "mensagem",
                        "Não foi possível iniciar a partida."
                    )
                )

            historico = self.rpc.obter_historico()

            self.after(
                0,
                self._finalizar_inicio_partida,
                resultado,
                historico,
                None
            )

        except Exception as erro:

            self.after(
                0,
                self._finalizar_inicio_partida,
                None,
                None,
                erro
            )

    # ==========================================================
    # LOADING DA PARTIDA
    # ==========================================================

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

    # ==========================================================
    # ENVIAR TENTATIVA
    # ==========================================================

    def enviar_tentativa(self):

        if self._enviando_tentativa:
            return

        if not self.partida_ativa:

            self.label_status.config(
                text="Não há uma partida ativa.",
                fg=self.RED
            )

            return

        palavra = self.campo_palavra.get().strip()

        if not palavra:

            self.label_status.config(
                text="Digite uma palavra.",
                fg="#f59e0b"
            )

            self.campo_palavra.focus_set()

            return

        self._enviando_tentativa = True

        self.campo_palavra.config(
            state="disabled"
        )

        self.botao_enviar.config(
            state="disabled"
        )

        self.botao_dica.config(
            state="disabled"
        )

        self.botao_desistir.config(
            state="disabled"
        )

        self.label_status.config(
            text="Enviando tentativa...",
            fg=self.TEXT_MUTED
        )

        self.loading_spinner.start()

        thread = threading.Thread(
            target=self._processar_tentativa,
            args=(palavra,),
            daemon=True
        )

        thread.start()

    def _processar_tentativa(self, palavra):

        try:

            resultado = self.rpc.tentar_palavra(
                palavra
            )

            self.after(
                0,
                self._finalizar_tentativa,
                palavra,
                resultado,
                None
            )

        except Exception as erro:

            self.after(
                0,
                self._finalizar_tentativa,
                palavra,
                None,
                erro
            )

    # ==========================================================
    # FINALIZAR TENTATIVA
    # ==========================================================

    def _finalizar_tentativa(
        self,
        palavra,
        resultado,
        erro
    ):
        """
        Finaliza o processamento da tentativa.

        IMPORTANTE:
        O campo é sempre limpo depois que a tentativa
        termina de ser processada.
        """

        # Para o spinner
        self.loading_spinner.stop()

        # Libera o controle
        self._enviando_tentativa = False

        # ------------------------------------------------------
        # REATIVA O CAMPO PARA PODER ALTERÁ-LO
        # ------------------------------------------------------

        self.campo_palavra.config(
            state="normal"
        )

        # ------------------------------------------------------
        # LIMPA A PALAVRA DIGITADA
        # ------------------------------------------------------

        self.campo_palavra.delete(
            0,
            tk.END
        )

        # ------------------------------------------------------
        # ERRO DE COMUNICAÇÃO
        # ------------------------------------------------------

        if erro is not None:

            self.label_status.config(
                text=f"Erro ao enviar tentativa: {erro}",
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            if self.partida_ativa:

                self.campo_palavra.focus_set()

            return

        # ------------------------------------------------------
        # RESPOSTA INVÁLIDA
        # ------------------------------------------------------

        if resultado is None:

            self.label_status.config(
                text="O servidor não retornou uma resposta.",
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            if self.partida_ativa:

                self.campo_palavra.focus_set()

            return

        try:

            # --------------------------------------------------
            # TENTATIVA RECUSADA
            # --------------------------------------------------

            if not resultado.get(
                "sucesso",
                False
            ):

                self.label_status.config(
                    text=resultado.get(
                        "mensagem",
                        "Tentativa recusada."
                    ),
                    fg="#f59e0b"
                )

                self._atualizar_estado_botoes(
                    self.partida_ativa
                )

                if self.partida_ativa:

                    self.campo_palavra.focus_set()

                return

            # --------------------------------------------------
            # ATUALIZA HISTÓRICO
            # --------------------------------------------------

            self.atualizar_historico()

            # --------------------------------------------------
            # RESULTADO
            # --------------------------------------------------

            posicao = resultado.get(
                "posicao",
                "-"
            )

            proximidade = resultado.get(
                "proximidade",
                resultado.get(
                    "similaridade",
                    "-"
                )
            )

            acertou = resultado.get(
                "acertou",
                False
            )

            self.partida_ativa = not acertou

            # --------------------------------------------------
            # ATUALIZA POSIÇÃO
            # --------------------------------------------------

            if posicao != "-":

                self.label_posicao.config(
                    text=f"#{posicao}"
                )

            # --------------------------------------------------
            # ATUALIZA PROXIMIDADE
            # --------------------------------------------------

            if proximidade != "-":

                try:

                    self.label_proximidade.config(
                        text=f"{float(proximidade):.4f}"
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    self.label_proximidade.config(
                        text=str(proximidade)
                    )

            # --------------------------------------------------
            # ACERTOU
            # --------------------------------------------------

            if acertou:

                self.label_status.config(
                    text="🎉 Você encontrou a palavra secreta!",
                    fg=self.GREEN
                )

                self.label_posicao.config(
                    text="✓",
                    fg=self.GREEN
                )

                self.label_proximidade.config(
                    text="1.0000",
                    fg=self.GREEN
                )

                self._mostrar_vitoria(
                    palavra
                )

                self._finalizar_partida()

            # --------------------------------------------------
            # NÃO ACERTOU
            # --------------------------------------------------

            else:

                self.label_status.config(
                    text=(
                        f'"{palavra}" ficou em #{posicao}  •  '
                        f'Proximidade: {proximidade}'
                    ),
                    fg=self.BLUE
                )

            # --------------------------------------------------
            # ATUALIZA BOTÕES
            # --------------------------------------------------

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            # --------------------------------------------------
            # FOCO NO CAMPO
            # --------------------------------------------------

            if self.partida_ativa:

                self.campo_palavra.focus_set()

        except Exception as erro_processamento:

            self.label_status.config(
                text=(
                    "Erro ao processar resposta: "
                    f"{erro_processamento}"
                ),
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            if self.partida_ativa:

                self.campo_palavra.focus_set()

    # ==========================================================
    # FINALIZAR INÍCIO DA PARTIDA
    # ==========================================================

    def _finalizar_inicio_partida(
        self,
        resultado,
        historico,
        erro
    ):

        self._mostrar_loading_partida(
            False
        )

        self._criando_partida = False

        if erro is not None:

            self.partida_ativa = False

            self._atualizar_estado_botoes(
                False
            )

            self.label_status_conexao.config(
                text="●  Servidor indisponível",
                fg=self.RED
            )

            self.label_status.config(
                text=str(erro),
                fg=self.RED
            )

            messagebox.showerror(
                "Erro de conexão",
                "Não foi possível iniciar a partida.\n\n"
                f"Detalhes: {erro}\n\n"
                "Verifique se o servidor está em execução."
            )

            return

        self.label_status_conexao.config(
            text="●  Servidor conectado",
            fg=self.GREEN
        )

        self.partida_ativa = True

        self.label_status.config(
            text="Partida iniciada. Boa sorte!",
            fg=self.GREEN
        )

        self.label_dica.config(
            text=""
        )

        self._mostrar_botao_nova_partida(
            False
        )

        self._atualizar_estado_botoes(
            True
        )

        self._limpar_cards()

        self._preencher_historico(
            historico
        )

        # Garante campo vazio
        self.campo_palavra.delete(
            0,
            tk.END
        )

        self.campo_palavra.focus_set()

    # ==========================================================
    # HISTÓRICO
    # ==========================================================

    def atualizar_historico(self):

        try:

            historico = self.rpc.obter_historico()

        except Exception as erro:

            self.label_status.config(
                text=f"Erro ao obter histórico: {erro}",
                fg=self.RED
            )

            return

        self._preencher_historico(
            historico
        )

    def _preencher_historico(self, historico):

        # Limpa tabela
        for item in self.tabela.get_children():

            self.tabela.delete(
                item
            )

        # Preenche tabela
        for indice, registro in enumerate(
            historico,
            start=1
        ):

            palavra = registro.get(
                "palavra",
                ""
            )

            posicao = registro.get(
                "posicao",
                "-"
            )

            proximidade = registro.get(
                "proximidade",
                registro.get(
                    "similaridade",
                    "—"
                )
            )

            tipo = registro.get(
                "tipo",
                "tentativa"
            )

            if tipo == "dica":

                tag = "dica"

            elif tipo == "vitoria":

                tag = "vitoria"

            else:

                tag = "tentativa"

            self.tabela.insert(
                "",
                "end",
                values=(
                    indice,
                    palavra,
                    (
                        f"#{posicao}"
                        if posicao != "-"
                        else "-"
                    ),
                    self._formatar_proximidade(
                        proximidade
                    )
                ),
                tags=(tag,)
            )

        # Scroll para o último registro
        itens = self.tabela.get_children()

        if itens:

            self.tabela.see(
                itens[-1]
            )

    # ==========================================================
    # FORMATAR PROXIMIDADE
    # ==========================================================

    def _formatar_proximidade(self, valor):

        try:

            return f"{float(valor):.4f}"

        except (
            ValueError,
            TypeError
        ):

            return str(valor)

    # ==========================================================
    # DICA
    # ==========================================================

    def solicitar_dica(self):

        if (
            not self.partida_ativa
            or self._processando_acao
        ):

            return

        self._processando_acao = True

        self._atualizar_estado_botoes(
            False
        )

        self.spinner_dica.start()

        thread = threading.Thread(
            target=self._processar_dica,
            daemon=True
        )

        thread.start()

    def _processar_dica(self):

        try:

            resultado = self.rpc.solicitar_dica()

            self.after(
                0,
                self._finalizar_dica,
                resultado,
                None
            )

        except Exception as erro:

            self.after(
                0,
                self._finalizar_dica,
                None,
                erro
            )

    def _finalizar_dica(
        self,
        resultado,
        erro
    ):

        self.spinner_dica.stop()

        self._processando_acao = False

        if erro is not None:

            self.label_dica.config(
                text=f"Erro ao solicitar dica: {erro}",
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            return

        if resultado is None:

            self.label_dica.config(
                text="Não foi possível obter uma dica.",
                fg="#f59e0b"
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            return

        if resultado.get(
            "sucesso",
            False
        ):

            dica = (
                resultado.get("dica")
                or resultado.get("palavra")
                or resultado.get(
                    "mensagem",
                    "Dica recebida."
                )
            )

            posicao = resultado.get(
                "posicao"
            )

            proximidade = resultado.get(
                "proximidade",
                resultado.get(
                    "similaridade"
                )
            )

            texto = f"💡 Dica: {dica}"

            if posicao is not None:

                texto += f"  •  #{posicao}"

            if proximidade is not None:

                texto += (
                    "  •  "
                    f"{self._formatar_proximidade(proximidade)}"
                )

            self.label_dica.config(
                text=texto,
                fg=self.PURPLE
            )

            # Atualiza histórico
            self.atualizar_historico()

        else:

            self.label_dica.config(
                text=resultado.get(
                    "mensagem",
                    "Não foi possível obter uma dica."
                ),
                fg="#f59e0b"
            )

        self._atualizar_estado_botoes(
            self.partida_ativa
        )

    # ==========================================================
    # DESISTIR
    # ==========================================================

    def desistir(self):

        if (
            not self.partida_ativa
            or self._processando_acao
        ):

            return

        confirmar = messagebox.askyesno(
            "Desistir da partida",
            "Tem certeza que deseja desistir?\n\n"
            "A palavra secreta será revelada."
        )

        if not confirmar:

            return

        self._processando_acao = True

        self._atualizar_estado_botoes(
            False
        )

        self.spinner_desistir.start()

        thread = threading.Thread(
            target=self._processar_desistencia,
            daemon=True
        )

        thread.start()

    def _processar_desistencia(self):

        try:

            resultado = self.rpc.desistir()

            self.after(
                0,
                self._finalizar_desistencia,
                resultado,
                None
            )

        except Exception as erro:

            self.after(
                0,
                self._finalizar_desistencia,
                None,
                erro
            )

    def _finalizar_desistencia(
        self,
        resultado,
        erro
    ):

        self.spinner_desistir.stop()

        self._processando_acao = False

        if erro is not None:

            self.label_status.config(
                text=f"Erro ao desistir: {erro}",
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            return

        if resultado is None:

            self.label_status.config(
                text="O servidor não retornou uma resposta.",
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            return

        if not resultado.get(
            "sucesso",
            False
        ):

            self.label_status.config(
                text=resultado.get(
                    "mensagem",
                    "Não foi possível desistir."
                ),
                fg=self.RED
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

            return

        self.partida_ativa = False

        palavra = resultado.get(
            "palavra_secreta",
            "não informada"
        )

        palavras_proximas = resultado.get(
            "palavras_proximas",
            []
        )

        self.label_status.config(
            text=f"A palavra secreta era: {palavra}",
            fg=self.RED
        )

        self._finalizar_partida()

        self._mostrar_desistencia(
            palavra,
            palavras_proximas
        )

    # ==========================================================
    # FINALIZAR PARTIDA
    # ==========================================================

    def _finalizar_partida(self):

        self.partida_ativa = False

        self._atualizar_estado_botoes(
            False
        )

        self._mostrar_botao_nova_partida(
            True
        )

    # ==========================================================
    # NOVA PARTIDA
    # ==========================================================

    def nova_partida(self):

        if self._criando_partida:

            return

        # Limpa histórico
        for item in self.tabela.get_children():

            self.tabela.delete(
                item
            )

        # Limpa campo
        self.campo_palavra.config(
            state="normal"
        )

        self.campo_palavra.delete(
            0,
            tk.END
        )

        # Limpa mensagens
        self.label_dica.config(
            text=""
        )

        self.label_status.config(
            text="Iniciando nova partida...",
            fg=self.TEXT_MUTED
        )

        self._limpar_cards()

        self._mostrar_botao_nova_partida(
            False
        )

        self.iniciar_partida()

    # ==========================================================
    # LIMPAR CARDS
    # ==========================================================

    def _limpar_cards(self):

        self.label_posicao.config(
            text="—",
            fg=self.BLUE
        )

        self.label_proximidade.config(
            text="—",
            fg=self.PURPLE
        )

    # ==========================================================
    # MOSTRAR NOVA PARTIDA
    # ==========================================================

    def _mostrar_botao_nova_partida(
        self,
        mostrar
    ):

        if mostrar:

            self.botao_nova_partida.pack(
                side="left",
                padx=5,
                ipady=7,
                before=self.botao_menu
            )

        else:

            self.botao_nova_partida.pack_forget()

    # ==========================================================
    # VITÓRIA
    # ==========================================================

    def _mostrar_vitoria(self, palavra):

        messagebox.showinfo(
            "🎉 Parabéns!",
            "Você encontrou a palavra secreta!\n\n"
            f"Palavra: {palavra}"
        )

    # ==========================================================
    # DESISTÊNCIA
    # ==========================================================

    def _mostrar_desistencia(
        self,
        palavra,
        palavras_proximas
    ):

        janela = tk.Toplevel(
            self
        )

        janela.title(
            "Partida encerrada"
        )

        janela.geometry(
            "780x680"
        )

        janela.minsize(
            650,
            550
        )

        janela.configure(
            bg=self.BG
        )

        janela.transient(
            self.winfo_toplevel()
        )

        janela.grab_set()

        # ------------------------------------------------------
        # CABEÇALHO
        # ------------------------------------------------------

        tk.Label(
            janela,
            text="PARTIDA ENCERRADA",
            font=("Arial", 11, "bold"),
            bg=self.BG,
            fg=self.PURPLE
        ).pack(
            pady=(25, 3)
        )

        tk.Label(
            janela,
            text="Você desistiu da partida",
            font=("Arial", 22, "bold"),
            bg=self.BG,
            fg=self.WHITE
        ).pack()

        # ------------------------------------------------------
        # PALAVRA SECRETA
        # ------------------------------------------------------

        quadro = tk.Frame(
            janela,
            bg="#351827",
            highlightbackground="#7f1d1d",
            highlightthickness=1
        )

        quadro.pack(
            fill="x",
            padx=35,
            pady=20
        )

        tk.Label(
            quadro,
            text="A PALAVRA SECRETA ERA",
            font=("Arial", 9, "bold"),
            bg="#351827",
            fg="#fca5a5"
        ).pack(
            pady=(15, 4)
        )

        tk.Label(
            quadro,
            text=str(palavra).upper(),
            font=("Arial", 28, "bold"),
            bg="#351827",
            fg="#f87171"
        ).pack(
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        tk.Label(
            janela,
            text="30 palavras mais próximas",
            font=("Arial", 14, "bold"),
            bg=self.BG,
            fg=self.WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 10)
        )

        # ------------------------------------------------------
        # TABELA
        # ------------------------------------------------------

        quadro_tabela = tk.Frame(
            janela,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        quadro_tabela.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        colunas = (
            "posicao",
            "palavra",
            "proximidade"
        )

        tabela = ttk.Treeview(
            quadro_tabela,
            columns=colunas,
            show="headings"
        )

        tabela.heading(
            "posicao",
            text="POSIÇÃO"
        )

        tabela.heading(
            "palavra",
            text="PALAVRA"
        )

        tabela.heading(
            "proximidade",
            text="PROXIMIDADE"
        )

        tabela.column(
            "posicao",
            width=120,
            anchor="center"
        )

        tabela.column(
            "palavra",
            width=300,
            anchor="center"
        )

        tabela.column(
            "proximidade",
            width=160,
            anchor="center"
        )

        barra = ttk.Scrollbar(
            quadro_tabela,
            orient="vertical",
            command=tabela.yview
        )

        tabela.configure(
            yscrollcommand=barra.set
        )

        tabela.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        # ------------------------------------------------------
        # DADOS
        # ------------------------------------------------------

        for item in palavras_proximas:

            posicao = item.get(
                "posicao",
                "-"
            )

            proximidade = item.get(
                "proximidade",
                item.get(
                    "similaridade",
                    "-"
                )
            )

            tabela.insert(
                "",
                "end",
                values=(
                    f"#{posicao}",
                    item.get(
                        "palavra",
                        ""
                    ),
                    self._formatar_proximidade(
                        proximidade
                    )
                )
            )

        # ------------------------------------------------------
        # BOTÃO
        # ------------------------------------------------------

        tk.Button(
            janela,
            text="FECHAR",
            width=15,
            font=("Arial", 10, "bold"),
            bg=self.PANEL_LIGHT,
            fg=self.WHITE,
            activebackground=self.BORDER,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=janela.destroy
        ).pack(
            pady=(0, 20),
            ipady=7
        )

    # ==========================================================
    # ESTADO DOS BOTÕES
    # ==========================================================

    def _atualizar_estado_botoes(
        self,
        ativo
    ):

        estado = (
            "normal"
            if ativo
            else "disabled"
        )

        self.campo_palavra.config(
            state=estado
        )

        self.botao_enviar.config(
            state=estado
        )

        self.botao_dica.config(
            state=estado
        )

        self.botao_desistir.config(
            state=estado
        )

    # ==========================================================
    # VOLTAR AO MENU
    # ==========================================================

    def voltar_menu(self):

        try:

            self.winfo_toplevel().attributes(
                "-fullscreen",
                False
            )

        except tk.TclError:

            pass

        from client.ui.menu import Menu

        self.screen_manager.show(
            Menu
        )

    # ==========================================================
    # DESTRUIR
    # ==========================================================

    def destroy(self):

        try:

            self.winfo_toplevel().unbind(
                "<Escape>"
            )

        except tk.TclError:

            pass

        super().destroy()