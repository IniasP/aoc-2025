from dataclasses import dataclass


def is_valid(n) -> bool:
    s = str(n)
    size = len(s)
    if size % 2 != 0:
        return True
    split_in_two = s[: size // 2], s[size // 2 :]
    if split_in_two[0] == split_in_two[1]:
        print(f"{n} is invalid because of split {split_in_two}")
        return False
    return True


def is_valid_2(n) -> bool:
    s = str(n)
    size = len(s)
    for group_size in range(1, size // 2 + 1):
        if size % group_size == 0:
            groups = [s[i : i + group_size] for i in range(0, len(s), group_size)]
            if all(g == groups[0] for g in groups):
                print(f"{n} is invalid because of group size {group_size}")
                return False
    return True


@dataclass
class Range:
    start: int
    end: int

    @staticmethod
    def parse(s: str) -> "Range":
        parts = s.split("-")
        return Range(int(parts[0]), int(parts[1]))

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    def all(self) -> list[int]:
        return list(range(self.start, self.end + 1))

    def count_invalid(self) -> int:
        invalid = 0
        for n in self.all():
            if not is_valid(n):
                invalid += 1
        return invalid


with open("02/input.txt") as f:
    line = f.readlines()[0].strip()

    ranges = line.split(",")

    range_objs = list(map(Range.parse, ranges))

    all_ids = [n for r in range_objs for n in r.all()]
    all_invalid_ids_1 = list(filter(lambda x: not is_valid(x), all_ids))
    all_invalid_ids_2 = list(filter(lambda x: not is_valid_2(x), all_ids))

    print(f"Part 1: sum of invalid ids is {sum(all_invalid_ids_1)}")
    print(f"Part 2: sum of invalid ids is {sum(all_invalid_ids_2)}")
