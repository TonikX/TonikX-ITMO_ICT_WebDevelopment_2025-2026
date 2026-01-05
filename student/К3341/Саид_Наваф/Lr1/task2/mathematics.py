from dataclasses import dataclass

@dataclass
class Math:
    a: int
    b: int
    h: int

    def do_math(self) -> float:
        return (self.a + self.b) / self.h

def parse_math(s: str) -> Math:
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 3:
        raise ValueError("expected three comma-separated numbers: a,b,h")
    return Math(int(parts[0]), int(parts[1]), int(parts[2]))