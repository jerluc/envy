import os
import subprocess
import sys

from blessed import Terminal  # type: ignore
from threading import Thread


class ShellMacro:
    """
    A ShellMacro is a macro that executes a command, either using an executable file path or a valid
    shell expression
    """

    def __init__(self, cmd: str, spawn_subshell: bool = True):
        if spawn_subshell:
            self._cmd = [os.environ["SHELL"], "-c", cmd]
        else:
            self._cmd = [cmd]
        self._out = Terminal(stream=sys.__stdout__)
        self._err = Terminal(stream=sys.__stderr__)

    def _stdout(self, stream):
        while True:
            out = stream.readline().decode("utf-8")
            if out:
                self._out.stream.write(self._out.green(out))
            else:
                break

    def _stderr(self, stream):
        while True:
            out = stream.readline().decode("utf-8")
            if out:
                self._err.stream.write(self._err.red(out))
            else:
                break

    def run(self) -> int:
        """
        Runs the shell command in a subprocess, and concurrently streams stdout/stderr to this
        process
        """
        p = subprocess.Popen(
            self._cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout_thread = Thread(target=self._stdout, args=(p.stdout,))
        stderr_thread = Thread(target=self._stderr, args=(p.stderr,))
        stdout_thread.start()
        stderr_thread.start()
        p.poll()
        stdout_thread.join()
        stderr_thread.join()

        return p.returncode
