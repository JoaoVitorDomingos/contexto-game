from xmlrpc.client import ServerProxy

from shared.constants import SERVIDOR_HOST, SERVIDOR_PORTA


def main():
    endereco = f"http://{SERVIDOR_HOST}:{SERVIDOR_PORTA}"

    cliente = ServerProxy(
        endereco,
        allow_none=True
    )

    print("=== TESTE DO RPC SERVER ===")

    # 1. Testar conexão
    resultado = cliente.ping()

    print("\n1. Ping:")
    print(resultado)

    # 2. Iniciar partida
    resultado = cliente.iniciar_partida()

    print("\n2. Iniciar partida:")
    print(resultado)

    # 3. Fazer uma tentativa
    resultado = cliente.tentar_palavra("casa")

    print("\n3. Tentativa: casa")
    print(resultado)

    # 4. Consultar histórico
    resultado = cliente.obter_historico()

    print("\n4. Histórico:")
    print(resultado)

    # 5. Tentar a palavra secreta de teste
    resultado = cliente.tentar_palavra("castelo")

    print("\n5. Tentativa: castelo")
    print(resultado)

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    main()