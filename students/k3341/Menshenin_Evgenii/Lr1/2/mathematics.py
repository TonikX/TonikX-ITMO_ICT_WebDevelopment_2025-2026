import dataclasses


@dataclasses.dataclass
class Math:
    a: int
    b: int
    h: int

    def do_math(self) -> float:
        return (self.a + self.b) / self.h


def parse_math(string: str) -> Math:
    split_string = string.split(",")
    return Math(int(split_string[0]), int(split_string[1]), int(split_string[2]))


def decode_math(math: Math) -> str:
    return f"{math.a},{math.b},{math.h}"
