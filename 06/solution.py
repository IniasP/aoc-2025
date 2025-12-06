from operator import mul, add
from functools import reduce


def transpose(t: list[list]):
    return [[t[x][y] for x in range(len(t))] for y in range(len(t[0]))]


def parse_operator(operator):
    if operator == "+":
        return add
    if operator == "*":
        return mul
    raise ValueError(f"{operator} is not an operator")


def calc(nums: list[int], op: str):
    op_f = parse_operator(op)
    return reduce(op_f, nums)


def part1(lines):
    problems = transpose([line.strip().split() for line in lines])
    sums = [calc([int(n) for n in r[:-1]], r[-1]) for r in problems]
    print(f"Part 1: {sum(sums)}")


def calc_problems_part2(problems: list[str]):
    """
    Problems looks like
    ['4', '431', '623+', '', '175', '581', '32*', '', '8', '248', '369+', '', '356', '24', '1  *']
    """
    all = []
    current = []
    operator = "+"
    for item in problems:
        if item == "":
            all.append(calc(current, operator))
            current.clear()
        elif item[-1] in ("*", "+"):
            current.append(int(item[:-1]))
            operator = item[-1]
        else:
            current.append(int(item))
    all.append(calc(current, operator))
    return all


def part2(lines):
    tx = transpose([list(s.removesuffix("\n")) for s in lines])
    tx_lines = ["".join(l).strip() for l in tx]
    tx_lines.reverse()
    problems = [txl.strip() for txl in tx_lines]
    sols = calc_problems_part2(problems)
    print(f"Part 2: {sum(sols)}")


with open("06/input.txt") as f:
    lines = f.readlines()
    part1(lines)
    part2(lines)
