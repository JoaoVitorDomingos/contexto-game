import tkinter as tk


class HelpScreen(tk.Frame):

    def __init__(self, root, screen_manager):
        super().__init__(root)

        self.screen_manager = screen_manager
        self.criar_interface()

    def criar_interface(self):

        # Canvas para permitir rolagem
        canvas = tk.Canvas(
            self,
            highlightthickness=0
        )

        # Barra de rolagem
        scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=canvas.yview
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

        # Frame que ficará dentro do Canvas
        conteudo = tk.Frame(canvas)

        canvas_window = canvas.create_window(
            (0, 0),
            window=conteudo,
            anchor="n"
        )

        # Atualiza a região de rolagem
        def atualizar_scroll(event):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        conteudo.bind(
            "<Configure>",
            atualizar_scroll
        )

        # Faz o conteúdo ocupar a largura do Canvas
        def ajustar_largura(event):
            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            ajustar_largura
        )

        # Função de scroll
        def scroll_mouse(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        # Registra o scroll nos elementos da tela
        widgets_scroll = [
            canvas,
            conteudo
        ]

        for widget in widgets_scroll:
            widget.bind(
                "<MouseWheel>",
                scroll_mouse
            )

        # Título
        titulo = tk.Label(
            conteudo,
            text="Ajuda",
            font=("Arial", 28, "bold")
        )

        titulo.pack(
            pady=(50, 30)
        )

        # Instruções
        instrucoes = tk.Label(
            conteudo,
            text=(
                "Como jogar\n\n"
                "O objetivo é descobrir a palavra secreta.\n\n"

                "Digite uma palavra e envie sua tentativa.\n"
                "O sistema informará a posição dessa palavra\n"
                "no ranking de proximidade em relação à resposta.\n\n"

                "Quanto mais próxima a posição estiver de 1,\n"
                "maior é a proximidade da palavra secreta.\n\n"

                "Você pode realizar quantas tentativas quiser.\n"
                "O jogo não possui limite de tempo.\n\n"

                "Dicas\n"
                "Solicite uma dica para receber uma palavra\n"
                "semanticamente mais próxima da resposta,\n"
                "sem revelar diretamente a palavra secreta.\n\n"

                "Desistência\n"
                "Ao desistir, a palavra secreta será revelada\n"
                "junto com as palavras mais próximas da solução."
            ),
            font=("Arial", 13),
            justify="center"
        )

        instrucoes.pack(
            pady=20
        )

        # Botão voltar
        botao_voltar = tk.Button(
            conteudo,
            text="Voltar",
            width=25,
            height=2,
            command=self.voltar
        )

        botao_voltar.pack(
            pady=30
        )

        # Scroll também funciona sobre os widgets internos
        titulo.bind(
            "<MouseWheel>",
            scroll_mouse
        )

        instrucoes.bind(
            "<MouseWheel>",
            scroll_mouse
        )

        botao_voltar.bind(
            "<MouseWheel>",
            scroll_mouse
        )

    def voltar(self):
        from client.ui.menu import Menu

        self.screen_manager.show(Menu)
