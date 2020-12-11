from pydantic import PyObject


class PyMacro:
    def __init__(self, pyobj: PyObject):
        self._pyobj = pyobj

    def run(self) -> int:
        assert callable(self._pyobj)
        self._pyobj()
        return 0
