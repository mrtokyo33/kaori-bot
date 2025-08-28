from dataclasses import dataclass

@dataclass(frozen=True)
class HelloRequestDTO:
    username: str