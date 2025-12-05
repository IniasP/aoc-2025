from dataclasses import dataclass
from functools import reduce


@dataclass
class Range:
    start: int
    end: int

    @staticmethod
    def parse(line: str):
        (start, end) = line.split("-")
        return Range(int(start), int(end))

    def includes(self, v: int):
        return self.start <= v <= self.end

    def overlaps(self, other: "Range") -> bool:
        return self.start <= other.end and self.end >= other.start

    def span(self, other: "Range") -> "Range":
        return Range(min(self.start, other.start), max(self.end, other.end))

    def expand(self, other: "Range"):
        span = self.span(other)
        self.start = span.start
        self.end = span.end

    def size(self):
        return self.end - self.start + 1


def parse(lines: list[str]):
    split_at = lines.index("")
    range_lines = lines[:split_at]
    ingredient_lines = lines[split_at + 1 :]
    return ([Range.parse(l) for l in range_lines], [int(l) for l in ingredient_lines])


def is_fresh(ingredient: int, ranges: list[Range]):
    return any(map(lambda r: r.includes(ingredient), ranges))


def add_range(existing: list[Range], new_range: Range):
    overlapping = next((r for r in existing if r.overlaps(new_range)), None)
    if overlapping:
        overlapping.expand(new_range)
    else:
        existing.append(new_range)


with open("05/input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    (ranges, ingredients) = parse(lines)

    fresh_count = sum(1 for ingredient in ingredients if is_fresh(ingredient, ranges))
    print(f"There are {fresh_count} fresh ingredients.")

    merged_ranges = []
    for r in sorted(ranges, key=lambda r: r.start):
        add_range(merged_ranges, r)

    considered_fresh = sum(r.size() for r in merged_ranges)
    print(f"A total of {considered_fresh} ingredients can be considered fresh.")
