from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class MacroProto(Protocol):
    def run(self) -> int:
        ...
