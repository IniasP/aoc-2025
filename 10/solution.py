from dataclasses import dataclass
import numpy as np
import scipy


def parse_nums(csv: str):
    return [int(s) for s in csv.strip().split(",")]


@dataclass
class Machine:
    indicator_goal: list[bool]
    buttons: list[list[int]]
    joltages_goal: list[int]

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
        joltages_str = ",".join(str(n) for n in self.joltages_goal)
        wirings_str = " ".join(
            f"({','.join(str(n) for n in wiring)})" for wiring in self.buttons
        )
        return f"[{indic}] {wirings_str} {{{joltages_str}}}"


def press_toggle(indicators: list[bool], button: list[int]):
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
                press_toggle(indicators, button)
            if indicators == machine.indicator_goal:
                return d
        d += 1


def solve_part2(machine: Machine) -> int:
    """
    The only thing that counts is the number of presses for each button.

    Each button can be translated to a matrix containing increments:
    From the example, machine 1 has buttons
    [0, 0, 0, 1] [0, 1, 0, 1] [0, 0, 1, 0] [0, 0, 1, 1] [1, 0, 1, 0] [1, 1, 0, 0]
    and goal [3, 5, 4, 7]

    Which can be written as a system of linear equations in matrix multiplication form:

    A               x      b
    [0 0 0 0 1 1]   [n1]   [3]
    [0 1 0 0 0 1]   [n2]   [5]
    [0 0 1 1 1 0] x [n3] = [4]
    [1 1 0 1 0 0]   [n4]   [7]
                    [n5]
                    [n6]

    The coefficients of the objective function are all 1's,
    since we're optimizing the unweighted sum of the button presses.
    """
    at = np.array(
        [
            [1 if i in b else 0 for i in range(len(machine.joltages_goal))]
            for b in machine.buttons
        ]
    )
    a = np.transpose(at)
    b = np.array(machine.joltages_goal)
    # objective function coefficients
    c = np.array([1] * len(machine.buttons))
    # apply what they call "data science" 🤠
    res = scipy.optimize.linprog(c, A_eq=a, b_eq=b, integrality=1)
    print(res.x)
    return sum(res.x)


with open("10/input.txt") as f:
    machines = [Machine.parse(l) for l in f.readlines()]
    part1_sols = [solve_part1(m) for m in machines]
    print(f"Part 1: {sum(part1_sols)}")
    part2_sols = [solve_part2(m) for m in machines]
    print(f"Part 2: {sum(part2_sols)}")
