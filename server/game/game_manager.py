import random

from server.ia.book_loader import BookLoader
from server.ia.text_processor import TextProcessor
from server.ia.semantic_model import SemanticModel


class GameManager:
    def __init__(self):
        self.palavra_secreta = None
        self.tentativas = []
        self.partida_ativa = False
        self.ranking = {}
        self.vocabulario = []
        self.semantic_model = None
        self._carregar_ia()

    def _carregar_ia(self):
        print("Carregando livro e processamento de linguagem natural...")
        texto = BookLoader().load()
        processor = TextProcessor(min_frequency=2)
        resultado = processor.process(texto)

        # Mantemos somente palavras que possuem vetor no modelo.
        self.vocabulario = resultado["vocabulario"]
        print(f"Vocabulário após pré-processamento: {len(self.vocabulario)} palavras")

        self.semantic_model = SemanticModel(self.vocabulario)
        self.vocabulario = sorted(self.semantic_model.vectors.keys())
        print(f"Vocabulário com embeddings: {len(self.vocabulario)} palavras")

    def iniciar_partida(self):
        self.palavra_secreta = random.choice(self.vocabulario)
        self.ranking = self.semantic_model.build_ranking(self.palavra_secreta)
        self.tentativas = []
        self.partida_ativa = True

        return {
            "sucesso": True,
            "mensagem": "Partida iniciada.",
        }

    def tentar_palavra(self, palavra):
        if not self.partida_ativa:
            return {"sucesso": False, "mensagem": "Não existe uma partida ativa."}

        palavra = self.semantic_model.nlp.make_doc(palavra.strip().lower())[0].text
        palavra = self._normalizar_palavra(palavra)

        if not palavra:
            return {"sucesso": False, "mensagem": "Digite uma palavra."}

        if any(t["palavra"] == palavra for t in self.tentativas):
            return {"sucesso": False, "mensagem": "Essa palavra já foi tentada."}

        dados = self.ranking.get(palavra)
        if dados is None:
            return {
                "sucesso": False,
                "mensagem": "Essa palavra não está no vocabulário do livro ou não possui embedding.",
            }

        tentativa = {
            "palavra": palavra,
            "posicao": dados["posicao"],
            "similaridade": round(dados["similaridade"], 6),
            "proximidade": round(dados["similaridade"], 6),
        }
        self.tentativas.append(tentativa)

        acertou = palavra == self.palavra_secreta
        if acertou:
            self.partida_ativa = False

        return {
            "sucesso": True,
            "palavra": palavra,
            "posicao": dados["posicao"],
            "similaridade": round(dados["similaridade"], 6),
            "proximidade": round(dados["similaridade"], 6),
            "acertou": acertou,
            "partida_ativa": self.partida_ativa,
        }

    def obter_historico(self):
        return self.tentativas.copy()

    def solicitar_dica(self):
        if not self.partida_ativa:
            return {"sucesso": False, "mensagem": "Não existe uma partida ativa."}

        melhor_posicao = min(
            (t["posicao"] for t in self.tentativas),
            default=len(self.ranking) + 1,
        )
        tentadas = {t["palavra"] for t in self.tentativas}

        candidatos = sorted(
            self.ranking.items(), key=lambda item: item[1]["posicao"]
        )
        for palavra, dados in candidatos:
            if palavra == self.palavra_secreta or palavra in tentadas:
                continue
            if dados["posicao"] < melhor_posicao:
                return {
                    "sucesso": True,
                    "palavra": palavra,
                    "posicao": dados["posicao"],
                    "similaridade": round(dados["similaridade"], 6),
                    "proximidade": round(dados["similaridade"], 6),
                }

        return {
            "sucesso": False,
            "mensagem": "Não há uma dica disponível melhor que suas tentativas atuais.",
        }

    def desistir(self):
        if not self.partida_ativa:
            return {"sucesso": False, "mensagem": "Não existe uma partida ativa."}

        self.partida_ativa = False
        proximas = [
            {"palavra": palavra, **dados}
            for palavra, dados in sorted(
                self.ranking.items(), key=lambda item: item[1]["posicao"]
            )[:10]
        ]

        return {
            "sucesso": True,
            "mensagem": "Partida encerrada.",
            "palavra_secreta": self.palavra_secreta,
            "palavras_proximas": proximas,
        }

    @staticmethod
    def _normalizar_palavra(palavra):
        import unicodedata
        palavra = unicodedata.normalize("NFD", palavra)
        return "".join(c for c in palavra if unicodedata.category(c) != "Mn")
