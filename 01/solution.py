from dataclasses import dataclass
from typing import Literal


@dataclass
class Line:
    direction: Literal["L"] | Literal["R"]
    value: int

    def __str__(self):
        return f"{self.direction}{self.value}"


def parse_line(line):
    dir = line[0]
    val = int(line[1:])
    return Line(dir, val)


def parse() -> list[Line]:
    with open("01/input.txt") as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def apply(dial, line: Line):
    step = 1 if line.direction == "R" else -1
    count_0 = 0
    # the actual caveman solution
    for _ in range(line.value):
        dial = (dial + step) % 100
        if dial == 0:
            count_0 += 1
    return (dial, count_0)


lines = parse()
dial = 50
times_passed_0 = 0
positions = [dial]
for line in lines:
    (new_dial, line_0_count) = apply(dial, line)
    times_passed_0 += line_0_count
    print(f"Passed 0 {line_0_count} times going {line} on {dial}.")
    dial = new_dial
    positions.append(dial)
    print(f"After {line}, dial is at {dial}.")
times_0 = len(list(filter(lambda x: x == 0, positions)))
print(f"Dial has been at 0 a total of {times_0} times.")
print(f"Dial passed 0 a total of {times_passed_0} times.")
