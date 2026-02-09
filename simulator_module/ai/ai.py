from subprocess import Popen, PIPE

import pexpect
from pexpect import fdpexpect

from simulator_module.util.logger import Logger


class AI:
    _path: str
    _process: Popen
    _stdout: fdpexpect.fdspawn
    _stdin: fdpexpect.fdspawn

    _initial_coords: tuple[int, int]
    _player_id: int
    _running: bool
    _logs :list[str] = []

    def __init__(self, player_id, path: str, initial_coords: tuple[int, int], log_directory: str, logger: Logger):
        self._player_id = player_id
        self._logger = logger
        self._path = path
        self._initial_coords = initial_coords
        self._enabled = self._initial_coords != (-1, -1)
        self._log_filename = f'{log_directory}/{self.get_name()}.log'
        self._log_file = open(self._log_filename, 'wb')

        if self._enabled:
            self._process = Popen(['python', path], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            self._stdout = fdpexpect.fdspawn(self._process.stdout)
            self._stdin = fdpexpect.fdspawn(self._process.stdin)
            self.stderr = fdpexpect.fdspawn(self._process.stderr)

            self._running = True
        else: # disabled ai
            self._running = False

    def write_settings(self, nb_players):
        if not self._running:
            self._logger.log(f"Cannot write settings because AI {self._player_id} is not running")
            return

        self._logger.log(f"Game settings input: {nb_players} {self._player_id}")
        self._stdin.write(f"{nb_players} {self._player_id}\n")
        self._stdin.flush()

    def write_player_info(self, p, x0, y0, x1, y1):
        if not self._running:
            self._logger.log(f"Cannot write player info because AI {self._player_id} is not running")
            return
        self._logger.log(f"Input for p={p} : {x0} {y0} {x1} {y1}")
        self._stdin.write(f"{x0} {y0} {x1} {y1}\n")
        self._stdin.flush()

    def read_move(self):
        if not self._running:
            self._logger.log(f"Cannot read move because AI {self._player_id} is not running, defaults to DOWN")
            return 'DOWN'

        moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index = self._stdout.expect(moves, timeout=None)
        self._read_logs()
        self._write_logs(len(self._logs)-1)
        return moves[index]

    def stop(self):
        if not self._running:
            return
        self._process.kill()
        self._process.wait()
        self._log_file.close()
        self._running = False

    def get_name(self):
        return f"{self._player_id}_{self._path.split('/')[-1].split('.')[0]}" if self._enabled else f"{self._player_id}_disabled"

    def _read_logs(self):
        self._logger.log("Reading logs")

        buffer = b''
        while True:
            try:
                buffer += self.stderr.read_nonblocking(timeout=0) # poll
            except pexpect.TIMEOUT:
                self._logger.log("Finished reading logs")
                break

        self._logs.append(buffer.decode('utf-8'))

    def _write_logs(self, turn):
        logs = self._logs[turn]
        self._log_file.write(f"=== Logs at turn {turn} ===\n".encode('utf-8'))
        self._log_file.write(logs.encode('utf-8'))

    def get_logs_at_turn(self, turn: int) -> str | None:
        if not 0 <= turn < len(self._logs):
            return None
        return self._logs[turn]

