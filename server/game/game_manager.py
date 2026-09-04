from shared.constants import PALAVRA_SECRETA_TESTE


class GameManager:

    def __init__(self):
        self.palavra_secreta = None
        self.tentativas = []
        self.partida_ativa = False

    def iniciar_partida(self):
        """
        Inicia uma nova partida.
        """

        # TODO: substituir pela seleção aleatória da palavra secreta
        # usando o vocabulário gerado a partir do livro.
        self.palavra_secreta = PALAVRA_SECRETA_TESTE

        self.tentativas = []
        self.partida_ativa = True

        return {
            "sucesso": True,
            "mensagem": "Partida iniciada.",
        }

    def tentar_palavra(self, palavra):
        """
        Processa uma tentativa do jogador.
        """

        if not self.partida_ativa:
            return {
                "sucesso": False,
                "mensagem": "Não existe uma partida ativa.",
            }

        palavra = palavra.strip().lower()

        if not palavra:
            return {
                "sucesso": False,
                "mensagem": "Digite uma palavra.",
            }

        if palavra in self.tentativas:
            return {
                "sucesso": False,
                "mensagem": "Essa palavra já foi tentada.",
            }

        # TODO: substituir pela busca da palavra no ranking
        # calculado através da similaridade semântica.
        posicao = self._obter_posicao_teste(palavra)

        tentativa = {
            "palavra": palavra,
            "posicao": posicao,
        }

        self.tentativas.append(tentativa)

        acertou = palavra == self.palavra_secreta

        if acertou:
            self.partida_ativa = False

        return {
            "sucesso": True,
            "palavra": palavra,
            "posicao": posicao,
            "acertou": acertou,
            "partida_ativa": self.partida_ativa,
        }

    def obter_historico(self):
        """
        Retorna o histórico das tentativas realizadas.
        """

        return self.tentativas.copy()

    def desistir(self):
        """
        Encerra a partida e revela a palavra secreta.
        """

        if not self.partida_ativa:
            return {
                "sucesso": False,
                "mensagem": "Não existe uma partida ativa.",
            }

        self.partida_ativa = False

        return {
            "sucesso": True,
            "mensagem": "Partida encerrada.",
            "palavra_secreta": self.palavra_secreta,
        }

    def _obter_posicao_teste(self, palavra):
        """
        Retorna uma posição fictícia para permitir
        os testes enquanto a IA não estiver implementada.
        """

        # TODO: substituir pelo cálculo real da posição
        # da palavra no ranking de similaridade.

        if palavra == self.palavra_secreta:
            return 1

        return 50