import os
import queue
import threading
from subprocess import Popen, PIPE
from typing import IO, AnyStr

from pexpect import fdpexpect

from simulator_module.util.logger import Logger

class LogAppender:
    def __init__(self, stderr: IO[AnyStr], logger: Logger):
        self._stderr = stderr
        self._logs = queue.Queue()
        self._logger = logger

    def start(self):
        threading.Thread(target=self._read_logs, daemon=True).start()

    def _read_logs(self):
        self._logger.log("Reading logs...")
        for line in iter(self._stderr.readline, ""):
            self._logs.put(line.rstrip())
        self._logger.log("Stopped reading logs")

    def retrieve_logs(self) -> list[str]:
        logs = []
        while not self._logs.empty():
            logs.append(self._logs.get(block=False))
        return logs

class AI:
    _path: str
    _process: Popen
    _stdout: fdpexpect.fdspawn
    _stdin: fdpexpect.fdspawn

    _initial_coords: tuple[int, int]
    _player_id: int
    _running: bool
    _logs :list[list[str]] = []

    def __init__(self, player_id, path: str, initial_coords: tuple[int, int], log_directory: str, logger: Logger):
        self._player_id = player_id
        self._logger = logger
        self._path = path
        self._initial_coords = initial_coords
        self._log_filename = f'{log_directory}/{self.get_name()}.log'
        self._log_file = open(self._log_filename, 'wb')

        self._process = Popen(['python', path], stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)
        self._stdout = fdpexpect.fdspawn(self._process.stdout)
        self._stdin = fdpexpect.fdspawn(self._process.stdin)
        self.log_appender = LogAppender(self._process.stderr, self._logger)
        self.log_appender.start()

        self._running = True

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
        return f"{self._player_id}_{self._path.split('/')[-1].split('.')[0]}"

    def _read_logs(self):
        self._logs.append(self.log_appender.retrieve_logs())

    def _write_logs(self, turn):
        logs = self._logs[turn]
        self._log_file.write(f"=== Logs at turn {turn} ===\n".encode('utf-8'))
        self._log_file.write(os.linesep.join(logs).encode('utf-8'))
        self._log_file.flush()

    def get_logs_at_turn(self, turn: int) -> list[str] | None:
        if not 0 <= turn < len(self._logs):
            return None
        return self._logs[turn]
