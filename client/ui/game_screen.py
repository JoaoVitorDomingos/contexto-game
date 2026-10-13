import tkinter as tk

from client.ui.game.layout import GameLayoutMixin
from client.ui.game.panels import GamePanelsMixin
from client.ui.game.history import GameHistoryMixin
from client.ui.game.loading import GameLoadingMixin
from client.ui.game.game_controller import GameControllerMixin
from client.ui.game.game_over_dialog import GameOverDialog
from client.network.rpc_client import RPCClient


class GameScreen(
    GameLayoutMixin,
    GamePanelsMixin,
    GameHistoryMixin,
    GameLoadingMixin,
    GameControllerMixin,
    tk.Frame,
):
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

    def _mostrar_desistencia(self, palavra, palavras_proximas):
        GameOverDialog(
            self,
            palavra,
            palavras_proximas,
            self,
        )

    def destroy(self):

        try:

            self.winfo_toplevel().unbind(
                "<Escape>"
            )

        except tk.TclError:

            pass

        super().destroy()
