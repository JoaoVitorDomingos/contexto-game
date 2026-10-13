"""Inicialização e ciclo de vida das partidas."""

import tkinter as tk
import threading
from tkinter import messagebox


class GameSessionMixin:
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

    def _finalizar_partida(self):

        self.partida_ativa = False

        self._atualizar_estado_botoes(
            False
        )

        self._mostrar_botao_nova_partida(
            True
        )

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
