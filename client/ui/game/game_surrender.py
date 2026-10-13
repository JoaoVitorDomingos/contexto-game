"""Desistência e resultado da partida."""

import threading
from tkinter import messagebox


class GameSurrenderMixin:
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
        self._bloquear_acoes()

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

            self._liberar_acoes()

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

            self._liberar_acoes()

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

    def _mostrar_vitoria(self, palavra):

        messagebox.showinfo(
            "🎉 Parabéns!",
            "Você encontrou a palavra secreta!\n\n"
            f"Palavra: {palavra}"
        )
