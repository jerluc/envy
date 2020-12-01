import shlex
import subprocess
import sys

from blessed import Terminal
from threading import Thread


class CommandRunner:
    def __init__(self, cmd: str):
        self.cmd = shlex.split(cmd)
        self.term = Terminal()

    def _stdout(self, stream):
        while True:
            out = stream.readline().decode("utf-8")
            if out:
                sys.stdout.write(self.term.green(out))
            else:
                break

    def _stderr(self, stream):
        while True:
            out = stream.readline().decode("utf-8")
            if out:
                sys.stderr.write(self.term.red(out))
            else:
                break

    def run(self) -> int:
        p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_thread = Thread(target=self._stdout, args=(p.stdout,))
        stderr_thread = Thread(target=self._stderr, args=(p.stderr,))
        stdout_thread.start()
        stderr_thread.start()
        p.poll()
        stdout_thread.join()
        stderr_thread.join()

        return p.returncode
