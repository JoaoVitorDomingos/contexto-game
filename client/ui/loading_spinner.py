import tkinter as tk


class LoadingSpinner:
    """Controla uma animação de carregamento em um widget Tkinter."""

    FRAMES = ("◐", "◓", "◑", "◒")
    INTERVALO = 120

    def __init__(
        self,
        widget,
        texto_original,
        mensagem
    ):
        self.widget = widget
        self.texto_original = texto_original
        self.mensagem = mensagem

        self._indice = 0
        self._after_id = None
        self._executando = False

    def start(self):
        """Inicia a animação."""

        if self._executando:
            return

        self._executando = True
        self._indice = 0

        self._animar()

    def _animar(self):

        if not self._executando:
            return

        try:

            frame = self.FRAMES[self._indice]

            self.widget.config(
                text=f"{frame} {self.mensagem}"
            )

            self._indice = (
                self._indice + 1
            ) % len(self.FRAMES)

            self._after_id = self.widget.after(
                self.INTERVALO,
                self._animar
            )

        except tk.TclError:

            self._executando = False
            self._after_id = None

    def stop(self):

        self._executando = False

        if self._after_id is not None:

            try:
                self.widget.after_cancel(
                    self._after_id
                )

            except tk.TclError:
                pass

            self._after_id = None

        try:

            self.widget.config(
                text=self.texto_original
            )

        except tk.TclError:
            pass