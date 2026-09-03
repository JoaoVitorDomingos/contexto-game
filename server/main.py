from server.network.rpc_server import RPCServer


def main():
    servidor = RPCServer()
    servidor.iniciar()


if __name__ == "__main__":
    main()