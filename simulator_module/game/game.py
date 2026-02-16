from copy import deepcopy
from typing import Self

from simulator_module.game.grid import Grid
from simulator_module.game.player_turn import PlayerTurn
from simulator_module.util.logger import Logger

HEIGHT = 20
WIDTH = 30
MOVES = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class GameState:

    def __init__(self, grid: Grid, heads: list[tuple[int, int]], trails: list[list[tuple[int, int]]],
                 current_player: int | None = None, turn: int = 0, previous: Self = None):
        self._grid = grid
        self._heads = heads
        self._trails = trails
        self._current_player = current_player
        self._turn = turn
        self._previous = previous

    def get_grid(self):
        return self._grid

    def get_heads(self):
        return self._heads

    def get_trail(self, player):
        return self._trails[player]

    def get_current_player(self):
        return self._current_player

    def get_turn(self):
        return self._turn

    def get_alive_players(self):
        return [player for (player, heads) in enumerate(self._heads) if heads != (-1, -1)]

    def get_head(self, player) -> tuple[int, int]:
        return self._heads[player]

    def is_dead(self, player) -> bool:
        return self._heads[player] == (-1, -1)

    def winner(self) -> int:
        alive_players = [p for p, (x, y) in enumerate(self._heads) if (x, y) != (-1, -1)]
        return alive_players[0] if len(alive_players) == 1 else -1

    def move_player(self, player, move: str) -> Self:
        (x, y) = self._heads[player]
        (dx, dy) = MOVES[move]

        next_grid = deepcopy(self._grid)
        next_heads = self._heads[:]
        next_trails = [trail[:] for trail in self._trails]

        if self._grid.is_valid(x + dx, y + dy) and self._grid.get(x + dx, y + dy) == -1:
            next_grid.set(x + dx, y + dy, player)
            next_player_position = (x + dx, y + dy)
            next_heads[player] = next_player_position
            next_trails[player] += [next_player_position]
        else:
            next_heads[player] = (-1, -1)
            next_grid.replace(player, -1)
            next_trails[player] = []

        return GameState(next_grid, next_heads, next_trails, player, self._turn + 1, self)

    def print(self, logger: Logger):
        header = "_| " + " ".join([str(i % 10) for i in range(self._grid.width)])
        logger.log(header)
        for y in range(self._grid.height):
            line = f"{y % 10}|"
            for x in range(self._grid.width):
                value = self._grid.get(x, y)
                cell_str = (
                        ('[' if 0 <= value and self._heads[value] == (x, y) else ' ')
                        +
                        (str(value) if value >= 0 else '.')
                )
                line += cell_str
            logger.log(line)


class Game:
    _nb_players: int
    _initial_coords: list[tuple[int, int]]
    _states: list[GameState]
    _player_death_state_index: list[int]
    _player_turn_by_steps: list[PlayerTurn]
    _player_turn_counters : list[int]

    def __init__(self, initial_coords: list[tuple[int, int]], logger: Logger):
        self.logger = logger
        self._nb_players = len(initial_coords)
        self._initial_coords = initial_coords
        self._player_death_state_index = [-1] * self._nb_players
        self._player_turn_by_steps = [PlayerTurn(-1, -1, 'INIT', 0)]
        self._player_turn_counters = [-1] * self._nb_players

        grid = Grid(WIDTH, HEIGHT)
        heads = [(0, 0)] * self._nb_players
        trails = [[(0, 0)]] * self._nb_players
        for (p, (x, y)) in enumerate(self._initial_coords):
            grid.set(x, y, p)
            heads[p] = (x, y)
            trails[p] = [(x,y)]
        self._states = [GameState(grid, heads, trails)]

    def get_nb_players(self):
        return self._nb_players

    def get_initial_coords(self):
        return self._initial_coords

    def get_states(self):
        return self._states

    def get_last_state(self):
        return self._states[-1]

    def get_player_death_state_index(self, player):
        return self._player_death_state_index[player]

    def get_player_initial_coords(self, player):
        return self._initial_coords[player] if not self._states[-1].is_dead(player) else (-1, -1)

    def move_player(self, player, player_turn: PlayerTurn) -> GameState:
        last_state = self._states[-1]
        next_state = last_state.move_player(player, player_turn.move)
        if not last_state.is_dead(player) and next_state.is_dead(player):
            self._player_death_state_index[player] = len(self._states)
        self._states.append(next_state)
        self._player_turn_counters[player] += 1
        self._player_turn_by_steps.append(player_turn)
        return next_state

    def get_player_turn_at_step(self, step) -> PlayerTurn | None:
        if not 0 <= step < len(self._player_turn_by_steps):
            return None
        return self._player_turn_by_steps[step]
