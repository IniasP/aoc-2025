from dataclasses import dataclass


def parse_nums(csv: str):
    return [int(s) for s in csv.strip().split(",")]


@dataclass
class Machine:
    indicator_goal: list[bool]
    buttons: list[list[int]]
    joltages: list[int]

    @staticmethod
    def parse(line: str):
        line = line.strip()
        indicators_end = line.index("]")
        indicator_goal = [c == "#" for c in line[1:indicators_end]]
        joltages_start = line.index("{")
        joltages = parse_nums(line[joltages_start + 1 : -1])
        line = line[indicators_end + 1 : joltages_start].strip()
        buttons = []
        while line:
            end = line.index(")")
            segment = line[1:end]
            buttons.append(parse_nums(segment))
            line = line[end + 2 :]
        return Machine(indicator_goal, buttons, joltages)

    def __str__(self) -> str:
        indic = "".join("#" if i else "." for i in self.indicator_goal)
        joltages_str = ",".join(str(n) for n in self.joltages)
        wirings_str = " ".join(
            f"({','.join(str(n) for n in wiring)})" for wiring in self.buttons
        )
        return f"[{indic}] {wirings_str} {{{joltages_str}}}"


def press(indicators: list[bool], button: list[int]):
    for i in button:
        indicators[i] = not indicators[i]


def all_sequences(num_options: int, depth: int) -> list[list[int]]:
    # naive implementation, could use cycle detection or something
    choices: list[list[int]] = [[]]
    for _ in range(depth):
        new_choices = []
        for choice in range(num_options):
            for existing_seq in choices:
                new_seq = existing_seq.copy()
                new_seq.append(choice)
                new_choices.append(new_seq)
        choices = new_choices
    return choices


def solve_part1(machine: Machine) -> int:
    d = 1
    while True:
        options_indices = all_sequences(len(machine.buttons), d)
        for option in options_indices:
            indicators = [False] * len(machine.indicator_goal)
            for button in (machine.buttons[i] for i in option):
                press(indicators, button)
            if indicators == machine.indicator_goal:
                print(d)
                return d
        d += 1


with open("10/input.txt") as f:
    machines = [Machine.parse(l) for l in f.readlines()]
    part1_sols = [solve_part1(m) for m in machines]
    print(f"Part 1: {sum(part1_sols)}")
