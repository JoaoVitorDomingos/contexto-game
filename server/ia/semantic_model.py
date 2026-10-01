import spacy


class SemanticModel:
    """
    Modelo semântico utilizando embeddings pré-treinados
    do spaCy e similaridade por cosseno.
    """

    MODEL_NAME = "pt_core_news_md"

    def __init__(self, vocabulary):

        self.vocabulary = vocabulary

        try:
            self.nlp = spacy.load(
                self.MODEL_NAME
            )

        except OSError as exc:

            raise RuntimeError(
                "Modelo spaCy não instalado.\n\n"
                "Execute:\n"
                "python -m spacy download pt_core_news_md"
            ) from exc

        self.vectors = {}

        self._prepare_vectors()

    # ==========================================================
    # PREPARAR VETORES
    # ==========================================================

    def _prepare_vectors(self):

        quantidade_com_vetor = 0
        quantidade_sem_vetor = 0

        for palavra in self.vocabulary:

            palavra = palavra.strip().lower()

            if not palavra:
                continue

            # Obtém o lexema diretamente do vocabulário
            lexeme = self.nlp.vocab[palavra]

            # Verifica se existe vetor real
            if not lexeme.has_vector:

                quantidade_sem_vetor += 1
                continue

            vector = lexeme.vector

            if vector is None:

                quantidade_sem_vetor += 1
                continue

            # Norma do vetor
            norm = float(
                (vector @ vector) ** 0.5
            )

            # Ignora vetor nulo
            if norm <= 0:

                quantidade_sem_vetor += 1
                continue

            self.vectors[palavra] = vector.copy()

            quantidade_com_vetor += 1

        print()
        print("=" * 60)
        print("MODELO SEMÂNTICO")
        print("=" * 60)

        print(
            f"Palavras com vetor: "
            f"{quantidade_com_vetor}"
        )

        print(
            f"Palavras sem vetor: "
            f"{quantidade_sem_vetor}"
        )

        print("=" * 60)
        print()

        if not self.vectors:

            raise RuntimeError(
                "Nenhuma palavra do vocabulário possui "
                "vetor semântico válido."
            )

    # ==========================================================
    # SIMILARIDADE
    # ==========================================================

    def similarity(
        self,
        word_a,
        word_b
    ):
        """
        Calcula a similaridade de cosseno
        entre duas palavras.
        """

        vector_a = self.vectors.get(
            word_a
        )

        vector_b = self.vectors.get(
            word_b
        )

        if vector_a is None:
            return None

        if vector_b is None:
            return None

        norm_a = float(
            (vector_a @ vector_a) ** 0.5
        )

        norm_b = float(
            (vector_b @ vector_b) ** 0.5
        )

        if norm_a == 0:
            return None

        if norm_b == 0:
            return None

        produto = float(
            vector_a @ vector_b
        )

        similaridade = (
            produto
            / (norm_a * norm_b)
        )

        return float(
            similaridade
        )

    # ==========================================================
    # RANKING
    # ==========================================================

    def build_ranking(
        self,
        secret_word
    ):
        """
        Cria o ranking das palavras pela proximidade
        semântica em relação à palavra secreta.

        A palavra secreta não entra no ranking.

        #1 = palavra mais próxima
        #2 = segunda mais próxima
        #3 = terceira mais próxima
        etc.
        """

        if secret_word not in self.vectors:

            raise ValueError(
                f"A palavra secreta '{secret_word}' "
                "não possui vetor semântico."
            )

        secret_vector = self.vectors[
            secret_word
        ]

        secret_norm = float(
            (secret_vector @ secret_vector) ** 0.5
        )

        if secret_norm == 0:

            raise ValueError(
                "A palavra secreta possui "
                "um vetor inválido."
            )

        scores = []

        # ======================================================
        # CALCULAR SIMILARIDADE
        # ======================================================

        for palavra, vector in self.vectors.items():

            # Nunca colocar a própria secreta
            if palavra == secret_word:
                continue

            norm = float(
                (vector @ vector) ** 0.5
            )

            if norm == 0:
                continue

            produto = float(
                secret_vector @ vector
            )

            similaridade = (
                produto
                / (secret_norm * norm)
            )

            # ==================================================
            # EVITAR VETORES IDENTICOS À SECRETA
            # ==================================================
            #
            # O modelo pt_core_news_md pode possuir várias
            # palavras apontando para o mesmo vetor.
            #
            # Nesse caso a similaridade fica exatamente 1.0.
            #
            # Não vamos considerar essas palavras como
            # verdadeiras "palavras próximas", pois elas
            # possuem exatamente a mesma representação vetorial.
            # ==================================================

            if similaridade >= 0.999999:

                continue

            scores.append(
                (
                    palavra,
                    similaridade
                )
            )

        # ======================================================
        # ORDENAR
        # ======================================================

        scores.sort(
            key=lambda item: item[1],
            reverse=True
        )

        # ======================================================
        # CRIAR RANKING
        # ======================================================

        ranking = {}

        for posicao, (
            palavra,
            similaridade
        ) in enumerate(
            scores,
            start=1
        ):

            ranking[palavra] = {

                "posicao": posicao,

                "similaridade": float(
                    similaridade
                )
            }

        # ======================================================
        # DEBUG NO TERMINAL
        # ======================================================

        print()
        print("=" * 60)

        print(
            f"RANKING DA PALAVRA SECRETA: "
            f"{secret_word}"
        )

        print("=" * 60)

        for palavra, dados in list(
            ranking.items()
        )[:20]:

            print(
                f"#{dados['posicao']:4d} "
                f"{palavra:<20} "
                f"{dados['similaridade']:.6f}"
            )

        print("=" * 60)
        print()

        return ranking