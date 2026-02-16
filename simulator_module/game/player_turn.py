from dataclasses import dataclass


@dataclass
class PlayerTurn:
    player_id: int
    turn: int
    move: str
    duration: float