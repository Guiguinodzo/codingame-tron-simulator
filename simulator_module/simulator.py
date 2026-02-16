import json
import os
import sys
import time
import traceback
from typing import Callable

from simulator_module.ai.ai import AI
from simulator_module.config import Config
from simulator_module.game.game import Game
from simulator_module.util.logger import Logger

HEIGHT = 20
WIDTH = 30

class Simulation:

    def __init__(self, config: Config, keep_log_files, logger = None):
        self._config = config
        log_directory = None
        if keep_log_files:
            log_directory = f'logs/run_{time.strftime("%Y%m%d-%H%M%S")}'
            os.makedirs(log_directory, exist_ok=True)

        if logger:
            self._logger = logger
        elif keep_log_files:
            self._logger = Logger(f'{log_directory}/simulator.log')
        else:
            self._logger = Logger()
            self._logger.log(f"Logs won't be kept.")

        self._logger.log(f"Config: {config}")

        self.ais: list[AI] = []
        heads = []
        for (player, ai_config) in enumerate(config.ais):
            self._logger.log(ai_config.program_path)
            self.ais.append(AI(player, ai_config.program_path, ai_config.initial_coords, log_directory, self._logger))
            heads.append(ai_config.initial_coords)

        self.game = Game(heads, self._logger)

    def start(self, progress_callback: Callable[[int, int, str],None] = None):
        self._logger.log("Starting simulation")
        turn = 0
        if progress_callback:
            progress_callback(turn, -1, "start")

        while self.game.get_last_state().winner() == -1:
            for player in range(self.game.get_nb_players()):
                if self.game.get_last_state().winner() != -1:
                    continue

                if self.game.get_last_state().is_dead(player):
                    self.ais[player].stop()
                    turn +=1
                    if progress_callback:
                        progress_callback(turn, player, "death")
                    continue

                players_info = []
                for p in range(self.game.get_nb_players()):
                    (x1, y1) = self.game.get_last_state().get_head(p)
                    (x0, y0) = self.game.get_player_initial_coords(p)
                    players_info.append((x0, y0, x1, y1))

                player_move, elapsed_time = self.ais[player].ask(self.game.get_nb_players(), players_info)
                self._logger.log(f"Player move: {player_move} - Elasped time: {elapsed_time*1000:.3f}")
                self.game.move_player(player, player_move)

                turn += 1
                if progress_callback:
                    progress_callback(turn, player, player_move)

        turn = 950 # max turn is 950
        if progress_callback:
            progress_callback(turn, self.game.get_last_state().winner(), "win")
        self.stop()

    def stop(self):
        for ai in self.ais:
            ai.stop()

    def print_all_states(self):
        for state in self.game.get_states():
            self._logger.log(f"Turn: {state.get_turn()}  - Player: #{state.get_current_player()}")
            state.print(self._logger)

    def get_logs_at(self, step, player_id):
        player_of_turn, turn = self.game.get_player_and_turn_at_step(step)
        if player_of_turn != player_id:
            return None
        return self.ais[player_id].get_logs_at_turn(turn)


def progress_function(logger) -> Callable[[int, int, str],None]:
    return lambda turn, player, move : logger.log(f"Progress {turn} / 950 = {turn/9.5:.2f}% : player #{player} -> {move}")


def main():

    simulation: Simulation|None = None
    exit_code = 0

    log_directory = f'logs/run_{time.strftime("%Y%m%d-%H%M%S")}'
    os.makedirs(log_directory, exist_ok=True)
    logger = Logger(f'{log_directory}/simulator.log')

    try:
        args = sys.argv[1:]

        config = Config({
            "ais": [
            ]
        })
        if len(args) > 0:
            config_file_path = args[0]
            with open(config_file_path, 'r') as config_file:
                json_config = json.load(config_file)
                config = Config(json_config)

        logger.log(f"Config: {config}")

        simulation = Simulation(config, logger)
        simulation.start(progress_function(logger))

        input("Press any key to print all states...")
        simulation.print_all_states()

    except Exception:
        logger.log(traceback.format_exc())
        exit_code=1
    finally:
        if simulation:
            simulation.stop()
        logger.close()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
