import xmlrpc.client

from shared.constants import SERVIDOR_HOST, SERVIDOR_PORTA


class RPCClient:
    def __init__(self, host=SERVIDOR_HOST, porta=SERVIDOR_PORTA):
        self.host = host
        self.porta = porta

        self.url = f"http://{self.host}:{self.porta}"

        self.servidor = xmlrpc.client.ServerProxy(
            self.url,
            allow_none=True
        )

    def testar_conexao(self):
        try:
            return self.servidor.ping()
        except Exception:
            return False