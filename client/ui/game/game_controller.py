"""Agrega os comportamentos do controlador da partida em módulos especializados."""

from client.ui.game.game_session import GameSessionMixin
from client.ui.game.game_attempts import GameAttemptsMixin
from client.ui.game.game_hints import GameHintsMixin
from client.ui.game.game_surrender import GameSurrenderMixin
from client.ui.game.game_controls import GameControlsMixin


class GameControllerMixin(
    GameSessionMixin,
    GameAttemptsMixin,
    GameHintsMixin,
    GameSurrenderMixin,
    GameControlsMixin,
):
    """Combina os fluxos de jogo usados por GameScreen."""
    pass
