import math
from collections import defaultdict

import spacy


class SemanticModel:
    """Usa embeddings pré-treinados do spaCy e similaridade por cosseno."""

    MODEL_NAME = "pt_core_news_md"

    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        try:
            self.nlp = spacy.load(self.MODEL_NAME)
        except OSError as exc:
            raise RuntimeError(
                "Modelo spaCy não instalado. Execute: "
                "python -m spacy download pt_core_news_md"
            ) from exc

        self.vectors = {}
        self._prepare_vectors()

    def _prepare_vectors(self):
        docs = list(self.nlp.pipe(self.vocabulary, batch_size=256))
        for word, doc in zip(self.vocabulary, docs):
            vector = doc.vector
            norm = float((vector @ vector) ** 0.5)
            if norm > 0:
                self.vectors[word] = vector

        if not self.vectors:
            raise RuntimeError(
                "O modelo spaCy carregado não possui vetores de palavras. "
                "Use o modelo pt_core_news_md."
            )

    def similarity(self, word_a, word_b):
        vector_a = self.vectors.get(word_a)
        vector_b = self.vectors.get(word_b)
        if vector_a is None or vector_b is None:
            return None

        norm_a = float((vector_a @ vector_a) ** 0.5)
        norm_b = float((vector_b @ vector_b) ** 0.5)
        if norm_a == 0 or norm_b == 0:
            return None

        return float((vector_a @ vector_b) / (norm_a * norm_b))

    def build_ranking(self, secret_word):
        if secret_word not in self.vectors:
            raise ValueError("A palavra secreta não possui embedding.")

        secret_vector = self.vectors[secret_word]
        secret_norm = float((secret_vector @ secret_vector) ** 0.5)

        scores = []
        for word, vector in self.vectors.items():
            norm = float((vector @ vector) ** 0.5)
            if norm == 0 or secret_norm == 0:
                continue
            score = float((secret_vector @ vector) / (secret_norm * norm))
            # Cosseno varia teoricamente de -1 a 1; mantemos o valor real.
            scores.append((word, score))

        scores.sort(key=lambda item: item[1], reverse=True)
        return {
            word: {"posicao": index, "similaridade": score}
            for index, (word, score) in enumerate(scores, start=1)
        }
