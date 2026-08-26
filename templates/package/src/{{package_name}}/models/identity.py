from dataclasses import dataclass


@dataclass(frozen=True)
class PackageId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("empty id")
