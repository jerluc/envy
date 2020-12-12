from pydantic import PyObject


class PyMacro:
    """
    A PyMacro is a kind of macro that executes a Python function
    """

    def __init__(self, pyobj: PyObject):
        self._pyobj = pyobj

    def run(self) -> int:
        """
        Runs a Python function
        """
        assert callable(self._pyobj)
        self._pyobj()
        return 0
