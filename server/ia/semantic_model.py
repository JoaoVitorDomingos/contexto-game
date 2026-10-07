import spacy


class SemanticModel:
    MODEL_NAME = "pt_core_news_md"

    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

        try:
            self.nlp = spacy.load(self.MODEL_NAME)
        except OSError as exc:
            raise RuntimeError(
                "Modelo spaCy não instalado.\n\n"
                "Execute:\n"
                "python -m spacy download pt_core_news_md"
            ) from exc

        self.vectors = {}

        self._prepare_vectors()

    def _prepare_vectors(self):
        quantidade_com_vetor = 0
        quantidade_sem_vetor = 0

        for palavra in self.vocabulary:
            palavra = palavra.strip().lower()

            if not palavra:
                continue

            lexeme = self.nlp.vocab[palavra]

            if not lexeme.has_vector:
                quantidade_sem_vetor += 1
                continue

            vector = lexeme.vector

            if vector is None:
                quantidade_sem_vetor += 1
                continue

            norm = float((vector @ vector) ** 0.5)

            if norm <= 0:
                quantidade_sem_vetor += 1
                continue

            self.vectors[palavra] = vector.copy()
            quantidade_com_vetor += 1

        print()
        print("=" * 60)
        print("MODELO SEMÂNTICO")
        print("=" * 60)
        print(f"Palavras com vetor: {quantidade_com_vetor}")
        print(f"Palavras sem vetor: {quantidade_sem_vetor}")
        print("=" * 60)
        print()

        if not self.vectors:
            raise RuntimeError(
                "Nenhuma palavra do vocabulário possui vetor "
                "semântico válido."
            )

    def similarity(self, word_a, word_b):
        """
        Calcula a similaridade de cosseno entre duas palavras.

        Retorna um valor entre -1 e 1.
        """

        vector_a = self.vectors.get(word_a)
        vector_b = self.vectors.get(word_b)

        if vector_a is None or vector_b is None:
            return None

        norm_a = float((vector_a @ vector_a) ** 0.5)
        norm_b = float((vector_b @ vector_b) ** 0.5)

        if norm_a == 0 or norm_b == 0:
            return None

        produto = float(vector_a @ vector_b)

        similaridade = produto / (norm_a * norm_b)

        return float(similaridade)

    def calcular_proximidade(self, similaridade):
        """
        Converte a similaridade para a proximidade utilizada pelo jogo.

        Neste projeto, a proximidade mantém o próprio valor da
        similaridade.

        Valores <= 0 são considerados inválidos.
        """

        if similaridade is None:
            return 0.0

        similaridade = float(similaridade)

        if similaridade <= 0:
            return 0.0

        return similaridade

    def build_ranking(self, secret_word):
        """
        Cria o ranking das palavras em relação à palavra secreta.

        Somente palavras com similaridade estritamente maior que zero
        entram no ranking.
        """

        if secret_word not in self.vectors:
            raise ValueError(
                f"A palavra secreta '{secret_word}' "
                "não possui vetor semântico."
            )

        secret_vector = self.vectors[secret_word]

        secret_norm = float(
            (secret_vector @ secret_vector) ** 0.5
        )

        if secret_norm == 0:
            raise ValueError(
                f"A palavra secreta '{secret_word}' "
                "possui vetor inválido."
            )

        scores = []

        for palavra, vector in self.vectors.items():

            # A palavra secreta não entra como tentativa.
            if palavra == secret_word:
                continue

            norm = float((vector @ vector) ** 0.5)

            if norm == 0:
                continue

            produto = float(secret_vector @ vector)

            similaridade = produto / (secret_norm * norm)

            # -------------------------------------------------
            # REGRA DO JOGO:
            # somente similaridades ESTRITAMENTE positivas
            # entram no ranking.
            #
            # Exemplos aceitos:
            #   0.7
            #   0.01
            #   0.000001
            #   0.0000001
            #
            # Exemplos descartados:
            #   0
            #   -0.001
            #   -0.5
            # -------------------------------------------------
            if similaridade <= 0:
                continue

            # Evita valores praticamente idênticos ao vetor
            # da palavra secreta.
            if similaridade >= 0.999999:
                continue

            scores.append(
                (palavra, similaridade)
            )

        # Maior similaridade primeiro.
        scores.sort(
            key=lambda item: item[1],
            reverse=True
        )

        ranking = {}

        for posicao, (palavra, similaridade) in enumerate(
            scores,
            start=2
        ):
            ranking[palavra] = {
                "posicao": posicao,
                "similaridade": float(similaridade),
                "proximidade": float(
                    self.calcular_proximidade(similaridade)
                )
            }

        print()
        print("=" * 60)
        print("RANKING SEMÂNTICO")
        print("=" * 60)
        print(f"Palavra secreta: {secret_word}")
        print(f"Palavras no ranking: {len(ranking)}")
        print("=" * 60)

        for palavra, dados in list(ranking.items())[:10]:
            print(
                f"#{dados['posicao']:04d} "
                f"{palavra:<20} "
                f"similaridade = "
                f"{dados['similaridade']:.10f}"
            )

        print("=" * 60)
        print()

        return ranking