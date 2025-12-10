from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int

    @staticmethod
    def parse(s: str):
        (x, y) = (int(c) for c in s.strip().split(","))
        return Coordinates(x, y)


@dataclass
class Edge:
    c1: Coordinates
    c2: Coordinates

    def is_vertical(self):
        return self.c1.x == self.c2.x

    def is_horizontal(self):
        return self.c1.y == self.c2.y


def intersects_hor_ver(horizontal: Edge, vertical: Edge):
    hor_y = horizontal.c1.y
    ver_y_from = min(vertical.c1.y, vertical.c2.y)
    ver_y_to = max(vertical.c1.y, vertical.c2.y)
    ver_x = vertical.c1.x
    hor_x_from = min(horizontal.c1.x, horizontal.c2.x)
    hor_x_to = max(horizontal.c1.x, horizontal.c2.x)
    return ver_y_from < hor_y < ver_y_to and hor_x_from < ver_x < hor_x_to


def intersects(edge1: Edge, edge2: Edge):
    if edge1.is_horizontal():
        if edge2.is_horizontal():
            return False
        return intersects_hor_ver(edge1, edge2)
    if edge2.is_horizontal():
        return intersects_hor_ver(edge2, edge1)
    return False


def is_allowed(coord: Coordinates, reds_set: set[Coordinates]):
    if coord in reds_set:
        return True
    x = coord.x
    y = coord.y
    top_left = False
    top_right = False
    bottom_left = False
    bottom_right = False
    for red in reds_set:
        if red.x <= x and red.y >= y:
            top_left = True
        if red.x >= x and red.y >= y:
            top_right = True
        if red.x <= x and red.y <= y:
            bottom_left = True
        if red.x >= x and red.y <= y:
            bottom_right = True
        if top_left and top_right and bottom_left and bottom_right:
            return True
    return False


@dataclass
class Rectangle:
    c1: Coordinates
    c2: Coordinates

    def area(self):
        return (abs((self.c1.x - self.c2.x)) + 1) * (abs(self.c1.y - self.c2.y) + 1)

    def bottom_left(self):
        return Coordinates(min(self.c1.x, self.c2.x), min(self.c1.y, self.c2.y))

    def bottom_right(self):
        return Coordinates(max(self.c1.x, self.c2.x), min(self.c1.y, self.c2.y))

    def top_left(self):
        return Coordinates(min(self.c1.x, self.c2.x), max(self.c1.y, self.c2.y))

    def top_right(self):
        return Coordinates(max(self.c1.x, self.c2.x), max(self.c1.y, self.c2.y))

    def corners(self):
        return (
            self.bottom_left(),
            self.bottom_right(),
            self.top_left(),
            self.top_right(),
        )

    def sides(self):
        return (
            Edge(self.bottom_left(), self.bottom_right()),
            Edge(self.bottom_left(), self.top_right()),
            Edge(self.top_left(), self.top_right()),
            Edge(self.bottom_right(), self.top_right()),
        )


def all_rectangles(coordinates: list[Coordinates]):
    rectangles = [
        Rectangle(c1, c2)
        for i, c1 in enumerate(coordinates[:-1])
        for c2 in coordinates[i + 1 :]
    ]
    return rectangles


def is_covered(rect: Rectangle, reds_set: set[Coordinates]):
    edges = [Edge(c1, c2) for c1, c2 in zip(reds, reds[1:] + reds[:1])]
    for c in rect.corners():
        if not is_allowed(c, reds_set):
            return False
    for e in edges:
        for s in rect.sides():
            if intersects(e, s):
                return False
    return True


with open("09/input.txt") as f:
    reds = [Coordinates.parse(l) for l in f.readlines()]
    all_rects = all_rectangles(reds)
    all_rects.sort(key=lambda p: p.area(), reverse=True)
    first = all_rects[0]
    print(f"Part 1: {first} with area {first.area()}")

    first = next(r for r in all_rects if is_covered(r, set(reds)))
    print(f"Part 2: {first} with area {first.area()}")
