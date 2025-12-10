from dataclasses import dataclass


@dataclass
class Task:
    id: int
    description: str
    done: int = 0
