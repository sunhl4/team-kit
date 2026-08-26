from dataclasses import dataclass


@dataclass(frozen=True)
class JobId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("empty id")


@dataclass(frozen=True)
class DurationNs:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("negative duration")


@dataclass(frozen=True)
class MakespanNs:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("negative makespan")
