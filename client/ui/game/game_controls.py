"""Estados dos controles e navegação da tela."""

import tkinter as tk


class GameControlsMixin:
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

    def _atualizar_estado_botoes(
        self,
        ativo
    ):
        """Atualiza o estado visual dos controles da partida."""

        estado = (
            "normal"
            if ativo
            else "disabled"
        )

        self.campo_palavra.config(
            state=estado
        )

        self.botao_enviar.config(
            state=estado,
            bg=self.BLUE if ativo else self.BORDER,
            fg=self.WHITE if ativo else self.TEXT_MUTED,
            activebackground=(
                self.BLUE_HOVER
                if ativo
                else self.BORDER
            )
        )

        self.botao_dica.config(
            state=estado,
            bg=self.PURPLE if ativo else self.BORDER,
            fg=self.WHITE if ativo else self.TEXT_MUTED,
            activebackground=(
                self.PURPLE_HOVER
                if ativo
                else self.BORDER
            )
        )

        self.botao_desistir.config(
            state=estado,
            bg=self.RED if ativo else self.BORDER,
            fg=self.WHITE if ativo else self.TEXT_MUTED,
            activebackground=(
                self.RED_HOVER
                if ativo
                else self.BORDER
            )
        )

        cursor = "hand2" if ativo else "arrow"

        for botao in (
            self.botao_enviar,
            self.botao_dica,
            self.botao_desistir
        ):
            botao.config(
                cursor=cursor
            )

    def _bloquear_acoes(self):
        """Bloqueia todas as ações enquanto uma comunicação está em andamento."""

        self.campo_palavra.config(
            state="disabled"
        )

        for botao in (
            self.botao_enviar,
            self.botao_dica,
            self.botao_desistir
        ):
            botao.config(
                state="disabled",
                bg=self.BORDER,
                fg=self.TEXT_MUTED,
                activebackground=self.BORDER,
                activeforeground=self.TEXT_MUTED,
                cursor="arrow"
            )

    def _liberar_acoes(self):
        """Libera novamente as ações quando a comunicação termina."""

        self._atualizar_estado_botoes(
            self.partida_ativa
        )

        cursor = "hand2" if self.partida_ativa else "arrow"

        for botao in (
            self.botao_enviar,
            self.botao_dica,
            self.botao_desistir
        ):
            botao.config(
                cursor=cursor
            )

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
