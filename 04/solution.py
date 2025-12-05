from dataclasses import dataclass


@dataclass
class Floor:
    rolls: list[list[bool]]

    @staticmethod
    def parse(lines: list[str]):
        return Floor([[c == "@" for c in row.strip()] for row in lines])

    def count(self):
        x_max = len(self.rolls)
        y_max = len(self.rolls[0])
        accessible_count = 0
        accessible_map = [[False for _ in range(y_max)] for _ in range(x_max)]
        for x in range(x_max):
            for y in range(y_max):
                val = self.rolls[x][y]
                if not val:
                    continue
                surrounding_roll_count = 0
                for x_offset in (-1, 0, 1):
                    for y_offset in (-1, 0, 1):
                        if x_offset == 0 and y_offset == 0:
                            continue
                        adj_x = x + x_offset
                        adj_y = y + y_offset
                        if adj_x < 0 or adj_y < 0 or adj_x >= x_max or adj_y >= y_max:
                            continue
                        if self.rolls[adj_x][adj_y]:
                            surrounding_roll_count += 1
                print(f"Surrounding roll count at ({x},{y}) is {surrounding_roll_count}")
                if surrounding_roll_count < 4:
                    accessible_count += 1
                    accessible_map[x][y] = True
                else:
                    accessible_map[x][y] = False
        for x in range(x_max):
            for y in range(y_max):
                print("x" if accessible_map[x][y] else ".", end="")
            print()
        return accessible_count


with open("04/input.txt", encoding="utf-8") as f:
    floor = Floor.parse(f.readlines())
    print(floor.count())
