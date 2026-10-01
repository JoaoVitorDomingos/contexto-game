import random
import unicodedata

from server.ia.book_loader import BookLoader
from server.ia.text_processor import TextProcessor
from server.ia.semantic_model import SemanticModel


class GameManager:

    def __init__(self):
        self.palavra_secreta = None

        self.tentativas = []
        self.historico = []

        self.partida_ativa = False

        self.ranking = {}
        self.vocabulario = []

        self.semantic_model = None

        self._carregar_ia()

    # ============================================================
    # CARREGAR IA
    # ============================================================

    def _carregar_ia(self):

        print("\n================================")
        print("CARREGANDO IA")
        print("================================")

        # --------------------------------------------------------
        # Carrega o livro
        # --------------------------------------------------------

        loader = BookLoader()

        # O BookLoader do projeto possui o método load()
        livro = loader.load()

        if not livro:
            raise RuntimeError(
                "Não foi possível carregar o livro utilizado pelo jogo."
            )

        print(
            f"Livro carregado: {len(livro)} caracteres"
        )

        # --------------------------------------------------------
        # Processa o texto
        # --------------------------------------------------------

        processor = TextProcessor(
            min_frequency=2
        )

        resultado = processor.process(
            livro
        )

        if not resultado:
            raise RuntimeError(
                "Não foi possível processar o livro."
            )

        vocabulario = resultado.get(
            "vocabulario",
            []
        )

        if not vocabulario:
            raise RuntimeError(
                "O processamento não gerou um vocabulário válido."
            )

        print(
            f"Vocabulário encontrado: "
            f"{len(vocabulario)} palavras"
        )

        # --------------------------------------------------------
        # Carrega modelo semântico
        # --------------------------------------------------------

        self.semantic_model = SemanticModel(
            vocabulario
        )

        # Usa somente palavras que possuem vetor
        self.vocabulario = sorted(
            self.semantic_model.vectors.keys()
        )

        if not self.vocabulario:
            raise RuntimeError(
                "Nenhuma palavra com vetor semântico foi encontrada."
            )

        print(
            f"Vocabulário final da IA: "
            f"{len(self.vocabulario)} palavras"
        )

        print("================================")
        print("IA CARREGADA")
        print("================================\n")

    # ============================================================
    # INICIAR PARTIDA
    # ============================================================

    def iniciar_partida(self):

        if not self.vocabulario:
            return {
                "sucesso": False,
                "mensagem": "O vocabulário do jogo está vazio."
            }

        # --------------------------------------------------------
        # Escolhe uma palavra secreta aleatória
        # --------------------------------------------------------

        self.palavra_secreta = random.choice(
            self.vocabulario
        )

        print(
            f"\n[PARTIDA] Palavra secreta: "
            f"{self.palavra_secreta}"
        )

        # --------------------------------------------------------
        # Cria o ranking da palavra secreta
        # --------------------------------------------------------

        self.ranking = (
            self.semantic_model.build_ranking(
                self.palavra_secreta
            )
        )

        # --------------------------------------------------------
        # Limpa dados da partida anterior
        # --------------------------------------------------------

        self.tentativas = []
        self.historico = []

        self.partida_ativa = True

        print(
            f"[PARTIDA] Ranking criado com "
            f"{len(self.ranking)} palavras."
        )

        return {
            "sucesso": True,
            "mensagem": "Partida iniciada com sucesso."
        }

    # ============================================================
    # TENTAR PALAVRA
    # ============================================================

    def tentar_palavra(self, palavra):

        if not self.partida_ativa:
            return {
                "sucesso": False,
                "mensagem": "Não há uma partida ativa."
            }

        if not palavra:
            return {
                "sucesso": False,
                "mensagem": "Digite uma palavra."
            }

        # --------------------------------------------------------
        # Normalização
        # --------------------------------------------------------

        palavra = palavra.strip().lower()

        palavra = self._normalizar_palavra(
            palavra
        )

        if not palavra:
            return {
                "sucesso": False,
                "mensagem": "Digite uma palavra válida."
            }

        # --------------------------------------------------------
        # Verifica se a palavra já foi tentada
        # --------------------------------------------------------

        for tentativa in self.tentativas:

            if tentativa["palavra"] == palavra:

                return {
                    "sucesso": False,
                    "mensagem": "Você já tentou essa palavra."
                }

        # --------------------------------------------------------
        # Verifica se acertou a palavra secreta
        # --------------------------------------------------------

        if palavra == self.palavra_secreta:

            registro = {
                "ordem": len(self.historico) + 1,
                "palavra": palavra,
                "posicao": 0,
                "similaridade": 1.0,
                "proximidade": 1.0,
                "tipo": "tentativa"
            }

            self.tentativas.append(
                registro
            )

            self.historico.append(
                registro
            )

            self.partida_ativa = False

            return {
                "sucesso": True,
                "acertou": True,
                "palavra": palavra,
                "posicao": 0,
                "proximidade": 1.0,
                "similaridade": 1.0,
                "mensagem": (
                    "Parabéns! "
                    "Você encontrou a palavra secreta."
                )
            }

        # --------------------------------------------------------
        # Procura palavra no ranking
        # --------------------------------------------------------

        dados = self.ranking.get(
            palavra
        )

        if dados is None:

            return {
                "sucesso": False,
                "mensagem": (
                    "Essa palavra não está disponível "
                    "no vocabulário do jogo."
                )
            }

        posicao = dados["posicao"]
        similaridade = dados["similaridade"]

        # --------------------------------------------------------
        # Registra tentativa
        # --------------------------------------------------------

        registro = {
            "ordem": len(self.historico) + 1,
            "palavra": palavra,
            "posicao": posicao,
            "similaridade": float(
                similaridade
            ),
            "proximidade": float(
                similaridade
            ),
            "tipo": "tentativa"
        }

        self.tentativas.append(
            registro
        )

        self.historico.append(
            registro
        )

        return {
            "sucesso": True,
            "acertou": False,
            "palavra": palavra,
            "posicao": posicao,
            "proximidade": float(
                similaridade
            ),
            "similaridade": float(
                similaridade
            ),
            "mensagem": "Tentativa registrada."
        }

    # ============================================================
    # OBTER HISTÓRICO
    # ============================================================

    def obter_historico(self):

        return list(
            self.historico
        )

    # ============================================================
    # SOLICITAR DICA
    # ============================================================

    def solicitar_dica(self):

        if not self.partida_ativa:

            return {
                "sucesso": False,
                "mensagem": "Não há uma partida ativa."
            }

        # --------------------------------------------------------
        # Palavras que já apareceram no histórico
        # --------------------------------------------------------

        palavras_usadas = {
            registro["palavra"]
            for registro in self.historico
            if registro.get("palavra")
        }

        # --------------------------------------------------------
        # Descobre a melhor posição alcançada
        #
        # Quanto MENOR o número, mais próxima está a palavra.
        #
        # Exemplo:
        #
        # tentativa = 2000
        # dica      = 1800
        # tentativa = 2500
        #
        # melhor posição = 1800
        #
        # A próxima dica precisa ser < 1800.
        # --------------------------------------------------------

        posicoes_validas = []

        for registro in self.historico:

            posicao = registro.get(
                "posicao"
            )

            if posicao is None:
                continue

            # Posição 0 significa que encontrou a secreta
            if posicao <= 0:
                continue

            posicoes_validas.append(
                posicao
            )

        if posicoes_validas:

            melhor_posicao = min(
                posicoes_validas
            )

        else:

            melhor_posicao = None

        # ========================================================
        # PRIMEIRA DICA
        # ========================================================

        if melhor_posicao is None:

            total_palavras = len(
                self.ranking
            )

            if total_palavras == 0:

                return {
                    "sucesso": False,
                    "mensagem": "O ranking está vazio."
                }

            # ----------------------------------------------------
            # Primeira dica:
            #
            # Não entrega imediatamente uma palavra do topo.
            #
            # Exemplo:
            # 5000 palavras
            #
            # primeira dica aproximadamente na região de 1000.
            # ----------------------------------------------------

            inicio = max(
                50,
                total_palavras // 5
            )

            intervalo = max(
                100,
                total_palavras // 20
            )

            fim = min(
                total_palavras,
                inicio + intervalo
            )

            candidatos = []

            for palavra, dados in self.ranking.items():

                posicao = dados["posicao"]

                # Nunca revela a palavra secreta
                if palavra == self.palavra_secreta:
                    continue

                # Nunca repete palavra
                if palavra in palavras_usadas:
                    continue

                if inicio <= posicao <= fim:

                    candidatos.append(
                        (palavra, dados)
                    )

        # ========================================================
        # DICAS SEGUINTES
        # ========================================================

        else:

            # ----------------------------------------------------
            # A nova dica precisa obrigatoriamente ser melhor.
            #
            # Exemplo:
            #
            # melhor posição = 2000
            #
            # próxima dica:
            # 1999, 1900, 1800...
            #
            # Nunca:
            # 2001, 2200...
            # ----------------------------------------------------

            limite_superior = (
                melhor_posicao - 1
            )

            if limite_superior < 1:

                return {
                    "sucesso": False,
                    "mensagem": (
                        "Não há uma posição melhor disponível "
                        "para fornecer uma nova dica."
                    )
                }

            # ----------------------------------------------------
            # Define uma faixa próxima da posição atual.
            #
            # Exemplo:
            #
            # melhor = 2000
            #
            # candidatos:
            # 1900 até 1999
            #
            # Se escolher 1940:
            #
            # próxima faixa:
            # 1840 até 1939
            # ----------------------------------------------------

            intervalo = max(
                100,
                len(self.ranking) // 20
            )

            inicio = max(
                1,
                limite_superior - intervalo + 1
            )

            fim = limite_superior

            candidatos = []

            for palavra, dados in self.ranking.items():

                posicao = dados["posicao"]

                # Nunca revela a palavra secreta
                if palavra == self.palavra_secreta:
                    continue

                # Nunca repete palavra
                if palavra in palavras_usadas:
                    continue

                # Precisa ser melhor que a melhor posição
                if posicao >= melhor_posicao:
                    continue

                if inicio <= posicao <= fim:

                    candidatos.append(
                        (palavra, dados)
                    )

        # ========================================================
        # SE NÃO ENCONTROU CANDIDATOS NA FAIXA
        # ========================================================

        if not candidatos:

            # ----------------------------------------------------
            # Se já existe uma melhor posição, procura qualquer
            # palavra ainda melhor.
            # ----------------------------------------------------

            if melhor_posicao is not None:

                for palavra, dados in self.ranking.items():

                    posicao = dados["posicao"]

                    if palavra == self.palavra_secreta:
                        continue

                    if palavra in palavras_usadas:
                        continue

                    if posicao >= melhor_posicao:
                        continue

                    candidatos.append(
                        (palavra, dados)
                    )

            # ----------------------------------------------------
            # Se for a primeira dica, procura qualquer palavra
            # disponível.
            # ----------------------------------------------------

            else:

                for palavra, dados in self.ranking.items():

                    if palavra == self.palavra_secreta:
                        continue

                    if palavra in palavras_usadas:
                        continue

                    candidatos.append(
                        (palavra, dados)
                    )

        # ========================================================
        # NENHUM CANDIDATO
        # ========================================================

        if not candidatos:

            return {
                "sucesso": False,
                "mensagem": (
                    "Não há mais palavras disponíveis "
                    "para fornecer uma dica melhor."
                )
            }

        # ========================================================
        # ESCOLHE A DICA
        # ========================================================

        palavra, dados = random.choice(
            candidatos
        )

        posicao = dados["posicao"]
        similaridade = dados["similaridade"]

        # ========================================================
        # REGISTRA DICA NO HISTÓRICO
        # ========================================================

        registro = {
            "ordem": len(self.historico) + 1,
            "palavra": palavra,
            "posicao": posicao,
            "similaridade": float(
                similaridade
            ),
            "proximidade": float(
                similaridade
            ),
            "tipo": "dica"
        }

        self.historico.append(
            registro
        )

        print(
            f"[DICA] {palavra} "
            f"| posição: {posicao} "
            f"| proximidade: "
            f"{similaridade:.6f}"
        )

        # ========================================================
        # RETORNO PARA O CLIENTE
        # ========================================================

        return {
            "sucesso": True,
            "palavra": palavra,
            "posicao": posicao,
            "proximidade": float(
                similaridade
            ),
            "similaridade": float(
                similaridade
            ),
            "mensagem": "Dica encontrada."
        }

    # ============================================================
    # DESISTIR
    # ============================================================

    def desistir(self):

        if not self.partida_ativa:

            return {
                "sucesso": False,
                "mensagem": "Não há uma partida ativa."
            }

        # --------------------------------------------------------
        # Encerra a partida
        # --------------------------------------------------------

        self.partida_ativa = False

        palavra_secreta = (
            self.palavra_secreta
        )

        # --------------------------------------------------------
        # Ordena o ranking
        #
        # 1 = mais próxima
        # --------------------------------------------------------

        ranking_ordenado = sorted(
            self.ranking.items(),
            key=lambda item: item[1]["posicao"]
        )

        # --------------------------------------------------------
        # Pega as 30 palavras mais próximas
        # --------------------------------------------------------

        palavras_proximas = []

        for palavra, dados in ranking_ordenado[:30]:

            palavras_proximas.append({

                "palavra": palavra,

                "posicao": dados["posicao"],

                "similaridade": float(
                    dados["similaridade"]
                ),

                "proximidade": float(
                    dados["similaridade"]
                )
            })

        print(
            f"\n[DESISTÊNCIA] "
            f"Palavra secreta: "
            f"{palavra_secreta}"
        )

        return {

            "sucesso": True,

            "palavra_secreta": (
                palavra_secreta
            ),

            "palavras_proximas": (
                palavras_proximas
            ),

            "mensagem": "Partida encerrada."
        }

    # ============================================================
    # NORMALIZAÇÃO
    # ============================================================

    def _normalizar_palavra(
        self,
        palavra
    ):

        palavra = unicodedata.normalize(
            "NFD",
            palavra
        )

        palavra = "".join(
            caractere
            for caractere in palavra
            if unicodedata.category(
                caractere
            ) != "Mn"
        )

        return palavra.lower().strip()