import xmlrpc.client

from shared.constants import SERVIDOR_HOST, SERVIDOR_PORTA


class RPCClient:
    """Cliente responsável exclusivamente pela comunicação XML-RPC."""

    def __init__(self, host=SERVIDOR_HOST, porta=SERVIDOR_PORTA, timeout=5):
        self.host = host
        self.porta = porta
        self.timeout = timeout
        self.url = f"http://{self.host}:{self.porta}"

        # O timeout é aplicado por requisição quando possível.
        self.servidor = xmlrpc.client.ServerProxy(
            self.url,
            allow_none=True
        )

    def testar_conexao(self):
        try:
            return bool(self.servidor.ping())
        except (OSError, xmlrpc.client.ProtocolError, xmlrpc.client.Fault):
            return False
        except Exception:
            return False

    def iniciar_partida(self):
        return self.servidor.iniciar_partida()

    def tentar_palavra(self, palavra):
        return self.servidor.tentar_palavra(palavra)

    def obter_historico(self):
        return self.servidor.obter_historico()

    def desistir(self):
        return self.servidor.desistir()

    def solicitar_dica(self):
        """Solicita uma dica quando o servidor disponibilizar esse método."""
        try:
            return self.servidor.solicitar_dica()
        except xmlrpc.client.Fault as erro:
            # Mantém o cliente compatível com o servidor atual, que ainda
            # não registra a operação de dica.
            return {
                "sucesso": False,
                "mensagem": "O servidor ainda não disponibiliza dicas."
            }
        except Exception as erro:
            return {
                "sucesso": False,
                "mensagem": f"Não foi possível solicitar a dica: {erro}"
            }
