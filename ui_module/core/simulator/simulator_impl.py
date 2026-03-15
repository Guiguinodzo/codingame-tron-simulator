from instruction_parser_module import parser
from simulator_module.config import Config
from simulator_module.simulator import Simulation
from ui_module.core.simulator.simulator_interface import SimulatorInterface, OutputBoard, OutputPlayer, InputPlayer, \
    StepDetails


class Simulator(SimulatorInterface):

    simulation: Simulation

    _running: bool
    _step_details: list[StepDetails|None]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_to_simulator_player_mapping = {}
        self.simulator_to_ui_player_mapping = {}
        self._running = False
        self._step_details = []

    def _start_simulation(self, players: list[InputPlayer]):
        self._running = True
        self.ui_to_simulator_player_mapping = {}
        self.simulator_to_ui_player_mapping = {}
        config = {
            "ais": []
        }
        for index, player in enumerate(players):
            player_config : dict = {
                "program_path": player.ai_path
            }
            if not player.random_pos:
                player_config['initial_coords'] = player.starting_pos

            config["ais"].append(player_config)
            self._map_user(player.id, index)

        self.simulation = Simulation(Config(config), self._keep_log_files)
        self.simulation.start(lambda turn, _, _2 : self.advancement.emit(turn/9.5))
        self._compute_all_step_details()
        self._running = False
        self.finished.emit()

    def _map_user(self, player_ui_id: int, player_simulator_id: int):
        self.ui_to_simulator_player_mapping[player_ui_id] = player_simulator_id
        self.simulator_to_ui_player_mapping[player_simulator_id] = player_ui_id

    def get_total_step_number(self) -> int:
        if self._running:
            return 0
        return len(self.simulation.game.get_states())

    def get_board_at(self, step: int) -> OutputBoard | None:
        if self._running:
            return None
        state_at_step = self.simulation.game.get_states()[step]
        output_board = OutputBoard()
        for player_ui_id, player_id in self.ui_to_simulator_player_mapping.items():
            head = state_at_step.get_head(player_id)
            trail = state_at_step.get_trail(player_id)
            output_board.players.append(OutputPlayer(player_ui_id, head, trail))

        return output_board

    def get_step_details(self, step: int) -> StepDetails | None:
        if self._running or step >= self.get_total_step_number():
            return None
        else:
            return self._step_details[step]

    def _compute_all_step_details(self):
        if not self._running:
            return
        for step in range(len(self.simulation.game.get_states())):
            step_details = self._compute_step_details(step)
            self._step_details.append(step_details)

    def _compute_step_details(self, step: int) -> StepDetails:
        player_turn = self.simulation.game.get_player_turn_at_step(step)
        player_ui_id = self.simulator_to_ui_player_mapping.get(player_turn.player_id)
        raw_logs = self.simulation.get_logs_at(step, player_turn.player_id)
        instructions = parser.parse_logs(raw_logs)
        logs = parser.filter_logs(raw_logs)

        step_details = StepDetails(step, player_turn.turn, player_ui_id, player_turn.duration, player_turn.move, logs,
                                   instructions)
        return step_details

    def get_player_stdout_at(self, step: int, player_id: int) -> str:
        return f"Not implemented yet: get_player_stdout_at({step}, {player_id})"

    def get_player_stderr_at(self, step: int, player_id: int) -> list[str]:
        if self._running:
            return []
        player_simulator_id = self.ui_to_simulator_player_mapping.get(player_id)
        return self.simulation.get_logs_at(step, player_simulator_id)

    def get_winner(self) -> int:    # return winner's player_id
        if self._running:
            return -1
        winner_id = self.simulation.game.get_winner()
        if winner_id == -1:
            return -1
        else:
            return self.simulator_to_ui_player_mapping.get(winner_id)

    def get_player_death_step(self, player_id: int) -> int:
        if self._running:
            return -1
        player_simulator_id = self.ui_to_simulator_player_mapping.get(player_id)
        if player_simulator_id is None:
            return -1

        return self.simulation.game.get_player_death_state_index(player_simulator_id)
