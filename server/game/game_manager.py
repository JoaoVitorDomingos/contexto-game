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

        self._cache_rankings = {}

        self._carregar_ia()

    def _carregar_ia(self):

        print()
        print("=" * 60)
        print("CARREGANDO IA")
        print("=" * 60)

        loader = BookLoader()

        livro = loader.load()

        if not livro:
            raise RuntimeError(
                "Não foi possível carregar o livro utilizado pelo jogo."
            )

        print(
            f"Livro carregado: {len(livro)} caracteres"
        )

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

        print("=" * 60)
        print("IA CARREGADA")
        print("=" * 60)
        print()

    def iniciar_partida(self):

        if not self.vocabulario:
            return {
                "sucesso": False,
                "mensagem": "O vocabulário do jogo está vazio."
            }

        self.palavra_secreta = random.choice(
            self.vocabulario
        )

        print()
        print(
            f"[PARTIDA] Palavra secreta: "
            f"{self.palavra_secreta}"
        )

        if self.palavra_secreta in self._cache_rankings:

            print(
                "[PARTIDA] Ranking encontrado no cache."
            )

            self.ranking = self._cache_rankings[
                self.palavra_secreta
            ]

        else:

            print(
                "[PARTIDA] Calculando ranking..."
            )

            ranking = (
                self.semantic_model.build_ranking(
                    self.palavra_secreta
                )
            )

            self._cache_rankings[
                self.palavra_secreta
            ] = ranking

            self.ranking = ranking

            print(
                "[PARTIDA] Ranking calculado e "
                "armazenado no cache."
            )

        self.tentativas = []
        self.historico = []

        self.partida_ativa = True

        print(
            f"[PARTIDA] Ranking disponível com "
            f"{len(self.ranking)} palavras."
        )

        return {
            "sucesso": True,
            "mensagem": "Partida iniciada com sucesso."
        }

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

        palavra = palavra.strip().lower()

        palavra = self._normalizar_palavra(
            palavra
        )

        if not palavra:
            return {
                "sucesso": False,
                "mensagem": "Digite uma palavra válida."
            }

        for tentativa in self.tentativas:

            if tentativa["palavra"] == palavra:

                return {
                    "sucesso": False,
                    "mensagem": "Você já tentou essa palavra."
                }

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

        posicao = dados.get(
            "posicao"
        )

        similaridade = dados.get(
            "similaridade"
        )

        proximidade = dados.get(
            "proximidade"
        )

        if proximidade is None:
            return {
                "sucesso": False,
                "mensagem": (
                    "A palavra não possui uma "
                    "proximidade semântica válida."
                )
            }

        if float(proximidade) <= 0:
            return {
                "sucesso": False,
                "mensagem": (
                    "A palavra possui similaridade "
                    "semântica não positiva."
                )
            }

        registro = {
            "ordem": len(self.historico) + 1,
            "palavra": palavra,
            "posicao": posicao,
            "similaridade": float(similaridade),
            "proximidade": float(proximidade),
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
            "proximidade": float(proximidade),
            "similaridade": float(similaridade),
            "mensagem": "Tentativa registrada."
        }

    def obter_historico(self):
        return sorted(
            self.historico,
            key=lambda registro: registro["proximidade"],
            reverse=True
        )

    def solicitar_dica(self):

        if not self.partida_ativa:

            return {
                "sucesso": False,
                "mensagem": "Não há uma partida ativa."
            }

        palavras_usadas = {
            registro["palavra"]
            for registro in self.historico
            if registro.get("palavra")
        }

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

        if melhor_posicao is None:

            total_palavras = len(
                self.ranking
            )

            if total_palavras == 0:

                return {
                    "sucesso": False,
                    "mensagem": "O ranking está vazio."
                }

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

                proximidade = dados.get(
                    "proximidade"
                )

                if proximidade is None:
                    continue

                if float(proximidade) <= 0:
                    continue

                if inicio <= posicao <= fim:

                    candidatos.append(
                        (palavra, dados)
                    )

        else:

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

                if palavra == self.palavra_secreta:
                    continue

                if palavra in palavras_usadas:
                    continue

                if posicao >= melhor_posicao:
                    continue

                proximidade = dados.get(
                    "proximidade"
                )

                if proximidade is None:
                    continue

                if float(proximidade) <= 0:
                    continue

                if inicio <= posicao <= fim:

                    candidatos.append(
                        (palavra, dados)
                    )

        if not candidatos:

            if melhor_posicao is not None:

                for palavra, dados in self.ranking.items():

                    posicao = dados["posicao"]

                    if palavra == self.palavra_secreta:
                        continue

                    if palavra in palavras_usadas:
                        continue

                    if posicao >= melhor_posicao:
                        continue

                    proximidade = dados.get(
                        "proximidade"
                    )

                    if proximidade is None:
                        continue

                    if float(proximidade) <= 0:
                        continue

                    candidatos.append(
                        (palavra, dados)
                    )

            else:

                for palavra, dados in self.ranking.items():

                    if palavra == self.palavra_secreta:
                        continue

                    if palavra in palavras_usadas:
                        continue

                    proximidade = dados.get(
                        "proximidade"
                    )

                    if proximidade is None:
                        continue

                    if float(proximidade) <= 0:
                        continue

                    candidatos.append(
                        (palavra, dados)
                    )

        if not candidatos:

            return {
                "sucesso": False,
                "mensagem": (
                    "Não há mais palavras disponíveis "
                    "para fornecer uma dica melhor."
                )
            }

        palavra, dados = random.choice(
            candidatos
        )

        posicao = dados["posicao"]

        similaridade = dados.get(
            "similaridade"
        )

        proximidade = dados.get(
            "proximidade"
        )

        if proximidade is None or float(proximidade) <= 0:

            return {
                "sucesso": False,
                "mensagem": (
                    "A dica selecionada não possui "
                    "proximidade positiva."
                )
            }

        registro = {
            "ordem": len(self.historico) + 1,
            "palavra": palavra,
            "posicao": posicao,
            "similaridade": float(similaridade),
            "proximidade": float(proximidade),
            "tipo": "dica"
        }

        self.historico.append(
            registro
        )

        print(
            f"[DICA] {palavra} "
            f"| posição: {posicao} "
            f"| proximidade: {float(proximidade):.10f}"
        )

        return {
            "sucesso": True,
            "palavra": palavra,
            "posicao": posicao,
            "proximidade": float(proximidade),
            "similaridade": float(similaridade),
            "mensagem": "Dica encontrada."
        }

    def desistir(self):

        if not self.partida_ativa:

            return {
                "sucesso": False,
                "mensagem": "Não há uma partida ativa."
            }

        self.partida_ativa = False

        palavra_secreta = (
            self.palavra_secreta
        )

        ranking_ordenado = sorted(
            self.ranking.items(),
            key=lambda item: item[1]["posicao"]
        )

        palavras_proximas = []

        for palavra, dados in ranking_ordenado[:30]:

            proximidade = dados.get(
                "proximidade"
            )

            similaridade = dados.get(
                "similaridade"
            )

            if proximidade is None:
                continue

            if float(proximidade) <= 0:
                continue

            palavras_proximas.append({

                "palavra": palavra,

                "posicao": dados["posicao"],

                "similaridade": float(
                    similaridade
                ),

                "proximidade": float(
                    proximidade
                )
            })

        print()
        print(
            "[DESISTÊNCIA] "
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
