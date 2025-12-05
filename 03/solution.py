from dataclasses import dataclass


@dataclass
class BatteryBank:
    batteries: list[int]

    @staticmethod
    def parse(line: str) -> "BatteryBank":
        return BatteryBank([int(c) for c in line.strip()])

    def max_n(self, n: int):
        remaining_batteries = self.batteries
        last_digit_pos = 0
        digits = []
        for i in range(n):
            ith_options = remaining_batteries[
                last_digit_pos : len(remaining_batteries) - n + i + 1
            ]
            ith_digit = max(ith_options)
            pos_ith = ith_options.index(ith_digit)
            remaining_batteries = remaining_batteries[pos_ith + 1 :]
            digits.append(ith_digit)
        return int("".join(str(d) for d in digits))

    def __str__(self) -> str:
        return "".join(map(str, self.batteries))


with open("03/input.txt") as f:
    banks = [BatteryBank.parse(l) for l in f.readlines()]
    for b in banks:
        print(b)
        print(f"Part 1: {b.max_n(2)}")
        print(f"Part 2: {b.max_n(12)}")

    total_1 = sum(b.max_n(2) for b in banks)
    total_2 = sum(b.max_n(12) for b in banks)
    print(f"Solution 1: total is {total_1}")
    print(f"Solution 2: total is {total_2}")
