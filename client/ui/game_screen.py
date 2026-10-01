import tkinter as tk
from tkinter import ttk, messagebox

from client.network.rpc_client import RPCClient
from shared.constants import NOME_DO_JOGO


class GameScreen(tk.Frame):
    """
    Tela principal da partida.

    A lógica da partida permanece no servidor.
    O cliente é responsável apenas pela interface
    e pela comunicação através do RPC.
    """

    def __init__(self, root, screen_manager):
        super().__init__(
            root,
            bg="#f5f7fb"
        )

        self.screen_manager = screen_manager
        self.rpc = RPCClient()

        self.partida_ativa = False
        self._criando_partida = False

        self.criar_interface()

        # Inicia a partida depois que a interface estiver pronta
        self.after(100, self.iniciar_partida)

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def criar_interface(self):

        # ------------------------------------------------------
        # CABEÇALHO
        # ------------------------------------------------------

        cabecalho = tk.Frame(
            self,
            bg="#f5f7fb"
        )

        cabecalho.pack(
            fill="x",
            padx=40,
            pady=(25, 10)
        )

        tk.Label(
            cabecalho,
            text=NOME_DO_JOGO,
            font=("Arial", 27, "bold"),
            bg="#f5f7fb",
            fg="#1f2937"
        ).pack(
            side="left"
        )

        self.label_status_conexao = tk.Label(
            cabecalho,
            text="Conectando...",
            font=("Arial", 10, "bold"),
            bg="#f5f7fb",
            fg="#6b7280"
        )

        self.label_status_conexao.pack(
            side="right",
            pady=8
        )

        # ------------------------------------------------------
        # SUBTÍTULO
        # ------------------------------------------------------

        tk.Label(
            self,
            text="Descubra a palavra secreta usando o ranking de proximidade.",
            font=("Arial", 12),
            bg="#f5f7fb",
            fg="#6b7280"
        ).pack(
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # ÁREA INFERIOR FIXA
        #
        # O rodapé é criado ANTES do histórico e usa side="bottom".
        # Dessa forma, Dica/Desistir/Menu permanecem sempre visíveis.
        # ------------------------------------------------------

        rodape = tk.Frame(
            self,
            bg="#f5f7fb"
        )

        rodape.pack(
            side="bottom",
            fill="x",
            padx=55,
            pady=(5, 18)
        )

        # Mensagem de dica
        self.label_dica = tk.Label(
            rodape,
            text="",
            font=("Arial", 11, "bold"),
            bg="#f5f7fb",
            fg="#7c3aed"
        )

        self.label_dica.pack(
            pady=(0, 3)
        )

        # Status da partida
        self.label_status = tk.Label(
            rodape,
            text="Iniciando partida...",
            font=("Arial", 10),
            bg="#f5f7fb",
            fg="#6b7280"
        )

        self.label_status.pack(
            pady=(0, 8)
        )

        # Área dos botões
        area_botoes = tk.Frame(
            rodape,
            bg="#f5f7fb"
        )

        area_botoes.pack()

        # ------------------------------------------------------
        # BOTÃO DICA
        # ------------------------------------------------------

        self.botao_dica = tk.Button(
            area_botoes,
            text="💡 Dica",
            width=15,
            font=("Arial", 10, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.solicitar_dica
        )

        self.botao_dica.pack(
            side="left",
            padx=5,
            ipady=5
        )

        # ------------------------------------------------------
        # BOTÃO DESISTIR
        # ------------------------------------------------------

        self.botao_desistir = tk.Button(
            area_botoes,
            text="Desistir",
            width=15,
            font=("Arial", 10, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.desistir
        )

        self.botao_desistir.pack(
            side="left",
            padx=5,
            ipady=5
        )

        # ------------------------------------------------------
        # BOTÃO NOVA PARTIDA
        # ------------------------------------------------------

        self.botao_nova_partida = tk.Button(
            area_botoes,
            text="Nova partida",
            width=15,
            font=("Arial", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.nova_partida
        )

        # Não aparece inicialmente.
        # Será mostrado quando a partida terminar.

        # ------------------------------------------------------
        # BOTÃO MENU
        # ------------------------------------------------------

        self.botao_menu = tk.Button(
            area_botoes,
            text="Menu",
            width=15,
            font=("Arial", 10),
            bg="#e5e7eb",
            fg="#374151",
            activebackground="#d1d5db",
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            command=self.voltar_menu
        )

        self.botao_menu.pack(
            side="left",
            padx=5,
            ipady=5
        )

        # ------------------------------------------------------
        # ENTRADA DE PALAVRA
        # ------------------------------------------------------

        painel_entrada = tk.Frame(
            self,
            bg="#ffffff",
            bd=1,
            relief="solid"
        )

        painel_entrada.pack(
            fill="x",
            padx=55,
            pady=5
        )

        tk.Label(
            painel_entrada,
            text="Digite uma palavra",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#374151"
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 4)
        )

        linha = tk.Frame(
            painel_entrada,
            bg="#ffffff"
        )

        linha.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        self.campo_palavra = tk.Entry(
            linha,
            font=("Arial", 14),
            relief="solid",
            bd=1
        )

        self.campo_palavra.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        self.campo_palavra.bind(
            "<Return>",
            lambda event: self.enviar_tentativa()
        )

        self.botao_enviar = tk.Button(
            linha,
            text="Enviar",
            width=13,
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.enviar_tentativa
        )

        self.botao_enviar.pack(
            side="left",
            padx=(10, 0),
            ipady=5
        )

        # ------------------------------------------------------
        # HISTÓRICO
        # ------------------------------------------------------

        painel_historico = tk.Frame(
            self,
            bg="#ffffff",
            bd=1,
            relief="solid"
        )

        painel_historico.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=(12, 5)
        )

        tk.Label(
            painel_historico,
            text="Histórico de tentativas",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#374151"
        ).pack(
            anchor="w",
            padx=18,
            pady=(13, 8)
        )

        area_tabela = tk.Frame(
            painel_historico,
            bg="#ffffff"
        )

        area_tabela.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 15)
        )

        colunas = (
            "ordem",
            "palavra",
            "posicao",
            "proximidade"
        )

        self.tabela = ttk.Treeview(
            area_tabela,
            columns=colunas,
            show="headings",
            height=9
        )

        cabecalhos = {
            "ordem": "#",
            "palavra": "Palavra",
            "posicao": "Posição no ranking",
            "proximidade": "Proximidade"
        }

        larguras = {
            "ordem": 55,
            "palavra": 250,
            "posicao": 180,
            "proximidade": 180
        }

        for coluna in colunas:
            self.tabela.heading(
                coluna,
                text=cabecalhos[coluna]
            )

            self.tabela.column(
                coluna,
                width=larguras[coluna],
                anchor="center"
            )

        barra = ttk.Scrollbar(
            area_tabela,
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

        # Estado inicial
        self._atualizar_estado_botoes(False)

    # ==========================================================
    # INICIAR PARTIDA
    # ==========================================================

    def iniciar_partida(self):

        if self._criando_partida:
            return

        self._criando_partida = True

        self.label_status_conexao.config(
            text="Conectando...",
            fg="#d97706"
        )

        try:

            if not self.rpc.testar_conexao():
                raise ConnectionError(
                    "Não foi possível conectar ao servidor."
                )

            self.label_status_conexao.config(
                text="● Servidor conectado",
                fg="#16a34a"
            )

            resultado = self.rpc.iniciar_partida()

            if not resultado.get("sucesso", False):
                raise RuntimeError(
                    resultado.get(
                        "mensagem",
                        "Não foi possível iniciar a partida."
                    )
                )

            self.partida_ativa = True

            self.label_status.config(
                text=resultado.get(
                    "mensagem",
                    "Partida iniciada."
                ),
                fg="#16a34a"
            )

            self.label_dica.config(
                text=""
            )

            self._mostrar_botao_nova_partida(False)

            self._atualizar_estado_botoes(True)

            self.campo_palavra.focus_set()

            self.atualizar_historico()

        except Exception as erro:

            self.partida_ativa = False

            self._atualizar_estado_botoes(False)

            self.label_status_conexao.config(
                text="● Servidor indisponível",
                fg="#dc2626"
            )

            self.label_status.config(
                text=str(erro),
                fg="#dc2626"
            )

            messagebox.showerror(
                "Erro de conexão",
                "Não foi possível iniciar a partida.\n\n"
                f"Detalhes: {erro}\n\n"
                "Verifique se o servidor está em execução."
            )

        finally:
            self._criando_partida = False

    # ==========================================================
    # ENVIAR TENTATIVA
    # ==========================================================

    def enviar_tentativa(self):

        if not self.partida_ativa:

            self.label_status.config(
                text="Não há uma partida ativa.",
                fg="#dc2626"
            )

            return

        palavra = self.campo_palavra.get().strip()

        if not palavra:

            self.label_status.config(
                text="Digite uma palavra.",
                fg="#d97706"
            )

            self.campo_palavra.focus_set()

            return

        self.botao_enviar.config(
            state="disabled"
        )

        try:

            resultado = self.rpc.tentar_palavra(
                palavra
            )

            if not resultado.get("sucesso", False):

                self.label_status.config(
                    text=resultado.get(
                        "mensagem",
                        "Tentativa recusada."
                    ),
                    fg="#d97706"
                )

                return

            self.campo_palavra.delete(
                0,
                tk.END
            )

            self.atualizar_historico()

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

            self.partida_ativa = resultado.get(
                "partida_ativa",
                not acertou
            )

            if acertou:

                self.label_status.config(
                    text=(
                        f"🎉 Parabéns! Você acertou "
                        f"a palavra em #{posicao}!"
                    ),
                    fg="#16a34a"
                )

                self._mostrar_vitoria(
                    palavra
                )

                self._finalizar_partida()

            else:

                self.label_status.config(
                    text=(
                        f"{palavra} ficou na posição "
                        f"#{posicao} | Proximidade: "
                        f"{proximidade}"
                    ),
                    fg="#2563eb"
                )

        except Exception as erro:

            self.label_status.config(
                text=f"Erro ao enviar tentativa: {erro}",
                fg="#dc2626"
            )

        finally:

            self.botao_enviar.config(
                state=(
                    "normal"
                    if self.partida_ativa
                    else "disabled"
                )
            )

            self._atualizar_estado_botoes(
                self.partida_ativa
            )

    # ==========================================================
    # HISTÓRICO
    # ==========================================================

    def atualizar_historico(self):

        try:

            historico = self.rpc.obter_historico()

        except Exception as erro:

            self.label_status.config(
                text=f"Erro ao obter histórico: {erro}",
                fg="#dc2626"
            )

            return

        # Limpa tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Adiciona tentativas
        for indice, tentativa in enumerate(
            historico,
            start=1
        ):

            proximidade = tentativa.get(
                "proximidade",
                tentativa.get(
                    "similaridade",
                    "—"
                )
            )

            self.tabela.insert(
                "",
                "end",
                values=(
                    indice,
                    tentativa.get(
                        "palavra",
                        ""
                    ),
                    tentativa.get(
                        "posicao",
                        "-"
                    ),
                    proximidade
                )
            )

    # ==========================================================
    # DICA
    # ==========================================================

    def solicitar_dica(self):

        if not self.partida_ativa:
            return

        self.botao_dica.config(
            state="disabled"
        )

        try:

            resultado = self.rpc.solicitar_dica()

            if resultado.get(
                "sucesso",
                False
            ):

                dica = resultado.get(
                    "dica"
                ) or resultado.get(
                    "palavra"
                ) or resultado.get(
                    "mensagem",
                    "Dica recebida."
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
                    texto += f" | Posição: #{posicao}"

                if proximidade is not None:
                    texto += (
                        f" | Proximidade: "
                        f"{proximidade}"
                    )

                self.label_dica.config(
                    text=texto,
                    fg="#7c3aed"
                )

            else:

                self.label_dica.config(
                    text=resultado.get(
                        "mensagem",
                        "Não foi possível obter uma dica."
                    ),
                    fg="#d97706"
                )

        except Exception as erro:

            self.label_dica.config(
                text=f"Erro ao solicitar dica: {erro}",
                fg="#dc2626"
            )

        finally:

            if self.partida_ativa:
                self.botao_dica.config(
                    state="normal"
                )

    # ==========================================================
    # DESISTIR
    # ==========================================================

    def desistir(self):

        if not self.partida_ativa:
            return

        confirmar = messagebox.askyesno(
            "Desistir",
            "Tem certeza que deseja desistir da partida?\n\n"
            "A palavra secreta será revelada."
        )

        if not confirmar:
            return

        self.botao_desistir.config(
            state="disabled"
        )

        try:

            resultado = self.rpc.desistir()

            if not resultado.get(
                "sucesso",
                False
            ):

                self.label_status.config(
                    text=resultado.get(
                        "mensagem",
                        "Não foi possível desistir."
                    ),
                    fg="#dc2626"
                )

                return

            self.partida_ativa = False

            palavra = resultado.get(
                "palavra_secreta",
                "não informada"
            )

            self.label_status.config(
                text=(
                    "Partida encerrada. "
                    f"A palavra secreta era: {palavra}"
                ),
                fg="#dc2626"
            )

            self._finalizar_partida()

            self._mostrar_desistencia(
                palavra
            )

        except Exception as erro:

            self.label_status.config(
                text=f"Erro ao desistir: {erro}",
                fg="#dc2626"
            )

        finally:

            self._atualizar_estado_botoes(
                self.partida_ativa
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

        # Limpa tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Limpa campo
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
            fg="#6b7280"
        )

        self._mostrar_botao_nova_partida(
            False
        )

        self.iniciar_partida()

    # ==========================================================
    # MOSTRAR/ESCONDER NOVA PARTIDA
    # ==========================================================

    def _mostrar_botao_nova_partida(
        self,
        mostrar
    ):

        if mostrar:

            self.botao_nova_partida.pack(
                side="left",
                padx=5,
                ipady=5,
                before=self.botao_menu
            )

        else:

            self.botao_nova_partida.pack_forget()

    # ==========================================================
    # MENSAGEM DE VITÓRIA
    # ==========================================================

    def _mostrar_vitoria(
        self,
        palavra
    ):

        messagebox.showinfo(
            "Parabéns!",
            "Você encontrou a palavra secreta!\n\n"
            f"Palavra: {palavra}"
        )

    # ==========================================================
    # MENSAGEM DE DESISTÊNCIA
    # ==========================================================

    def _mostrar_desistencia(
        self,
        palavra
    ):

        messagebox.showinfo(
            "Partida encerrada",
            "A palavra secreta era:\n\n"
            f"{palavra}"
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

        from client.ui.menu import Menu

        self.screen_manager.show(
            Menu
        )

    # ==========================================================
    # DESTRUIR TELA
    # ==========================================================

    def destroy(self):

        # Evita callbacks pendentes
        # interagindo com widgets destruídos.

        super().destroy()
