from xmlrpc.server import SimpleXMLRPCServer

from shared.constants import SERVIDOR_HOST, SERVIDOR_PORTA
from server.game.game_manager import GameManager


class RPCServer:

    def __init__(self, host=SERVIDOR_HOST, porta=SERVIDOR_PORTA):
        self.host = host
        self.porta = porta

        self.servidor = SimpleXMLRPCServer(
            (self.host, self.porta),
            allow_none=True
        )

        self.game_manager = GameManager()

        self.registrar_metodos()

    def registrar_metodos(self):
        self.servidor.register_function(
            self.ping,
            "ping"
        )

        self.servidor.register_function(
            self.iniciar_partida,
            "iniciar_partida"
        )

        self.servidor.register_function(
            self.tentar_palavra,
            "tentar_palavra"
        )

        self.servidor.register_function(
            self.obter_historico,
            "obter_historico"
        )

        self.servidor.register_function(
            self.desistir,
            "desistir"
        )

    def ping(self):
        return True

    def iniciar_partida(self):
        return self.game_manager.iniciar_partida()

    def tentar_palavra(self, palavra):
        return self.game_manager.tentar_palavra(palavra)

    def obter_historico(self):
        return self.game_manager.obter_historico()

    def desistir(self):
        return self.game_manager.desistir()

    def iniciar(self):
        print(
            f"Servidor RPC iniciado em "
            f"http://{self.host}:{self.porta}"
        )

        self.servidor.serve_forever()