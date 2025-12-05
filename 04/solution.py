from dataclasses import dataclass
from operator import xor

@dataclass
class Floor:
    grid: list[list[bool]]

    def flat(self) -> list[bool]:
        return [tile for row in self.grid for tile in row]

    def count_true(self):
        return sum(1 for t in self.flat() if t)

    def at(self, x, y) -> bool:
        return self.grid[x][y]

    def x_max(self):
        return len(self.grid)

    def y_max(self):
        return len(self.grid[0])

    def neighbor_coords(self, x, y):
        return [
            (adj_x, adj_y)
            for x_offset in (-1, 0, 1)
            for y_offset in (-1, 0, 1)
            if (
                not (x_offset == 0 and y_offset == 0)
                and (adj_x := x + x_offset) >= 0
                and adj_x < self.x_max()
                and (adj_y := y + y_offset) >= 0
                and (adj_y < self.y_max())
            )
        ]

    def all_coords(self):
        return [(x, y) for x in range(self.x_max()) for y in range(self.y_max())]

    def map(self, f):
        return Floor(
            [
                [f(self.at(x, y), x, y) for y in range(self.y_max())]
                for x in range(self.x_max())
            ]
        )

    def neighbor_count(self, x, y):
        return sum(1 for (nx, ny) in self.neighbor_coords(x, y) if self.at(nx, ny))

    def merge(self, other, f):
        return self.map(lambda val, x, y: f(val, other.at(x, y)))

    def __str__(self) -> str:
        return "\n".join(
            ["".join(["x" if t else "." for t in row]) for row in self.grid]
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.grid == self.grid


def parse(lines: list[str]):
    return Floor([[c == "@" for c in row.strip()] for row in lines])


def removable(floor, x, y):
    return floor.at(x, y) and floor.neighbor_count(x, y) < 4

with open("04/input.txt", encoding="utf-8") as f:
    floor = parse(f.readlines())

    # part 1
    accessible_floor = floor.map(lambda _, x, y: removable(floor, x, y))
    print(accessible_floor)
    print(f"Part 1: {accessible_floor.count_true()}")

    # part 2
    total_removed = 0
    while True:
        removable_rolls = floor.map(lambda _, x, y: removable(floor, x, y))
        cleaned_floor = floor.merge(removable_rolls, xor)
        if floor == cleaned_floor:
            break
        num_removed = removable_rolls.count_true()
        print(f"Removed {num_removed} rolls")
        total_removed += num_removed
        floor = cleaned_floor
        print(floor)

    print(f"Removed a total of {total_removed} rolls")
