"""Solicitação e apresentação de dicas."""

import threading


class GameHintsMixin:
    def solicitar_dica(self):

        if (
            not self.partida_ativa
            or self._processando_acao
        ):

            return

        self._processando_acao = True
        self._bloquear_acoes()

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

            self._liberar_acoes()

            return

        if resultado is None:

            self.label_dica.config(
                text="Não foi possível obter uma dica.",
                fg="#f59e0b"
            )

            self._liberar_acoes()

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

        self._liberar_acoes()
