from xmlrpc.server import SimpleXMLRPCServer

from shared.constants import SERVIDOR_HOST, SERVIDOR_PORTA


class RPCServer:
    def __init__(self, host=SERVIDOR_HOST, porta=SERVIDOR_PORTA):
        self.host = host
        self.porta = porta

        self.servidor = SimpleXMLRPCServer(
            (self.host, self.porta),
            allow_none=True
        )

        self.registrar_metodos()

    def registrar_metodos(self):
        self.servidor.register_function(
            self.ping,
            "ping"
        )

    def ping(self):
        return True

    def iniciar(self):
        print(
            f"Servidor RPC iniciado em "
            f"http://{self.host}:{self.porta}"
        )

        self.servidor.serve_forever()