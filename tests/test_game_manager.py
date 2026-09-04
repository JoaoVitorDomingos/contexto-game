from server.game.game_manager import GameManager


def main():
    game_manager = GameManager()

    print("=== TESTE DO GAME MANAGER ===")

    # 1. Iniciar partida
    resultado = game_manager.iniciar_partida()

    print("\n1. Iniciar partida:")
    print(resultado)

    # 2. Verificar tentativa incorreta
    resultado = game_manager.tentar_palavra("casa")

    print("\n2. Tentativa: casa")
    print(resultado)

    # 3. Verificar histórico
    resultado = game_manager.obter_historico()

    print("\n3. Histórico:")
    print(resultado)

    # 4. Verificar tentativa repetida
    resultado = game_manager.tentar_palavra("casa")

    print("\n4. Tentativa repetida: casa")
    print(resultado)

    # 5. Verificar tentativa correta
    resultado = game_manager.tentar_palavra("castelo")

    print("\n5. Tentativa correta: castelo")
    print(resultado)

    # 6. Verificar estado após acerto
    resultado = game_manager.obter_historico()

    print("\n6. Histórico final:")
    print(resultado)

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    main()