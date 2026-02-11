import sys

class Logger:

    def __init__(self, log_filename=None):
        self._log_file = None
        if log_filename:
            self._log_file = open(log_filename, "w")


    def log(self, *args):
        print(*args, file=sys.stderr)
        if self._log_file:
            print(*args, file=self._log_file)
            self._log_file.flush()

    def close(self):
        if self._log_file:
            self._log_file.close()
