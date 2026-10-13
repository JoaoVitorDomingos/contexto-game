"""Envio e apresentação das tentativas e do histórico."""

import tkinter as tk
import threading


class GameAttemptsMixin:
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
        self._bloquear_acoes()

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

            self._liberar_acoes()

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

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

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

            self._liberar_acoes()

            if self.partida_ativa:

                self.campo_palavra.focus_set()

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

    def _formatar_proximidade(self, valor):

        try:

            return f"{float(valor):.4f}"

        except (
            ValueError,
            TypeError
        ):

            return str(valor)

    def _limpar_cards(self):

        self.label_posicao.config(
            text="—",
            fg=self.BLUE
        )

        self.label_proximidade.config(
            text="—",
            fg=self.PURPLE
        )
