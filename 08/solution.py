from dataclasses import dataclass
from math import sqrt
from functools import reduce
from operator import mul


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int
    z: int

    @staticmethod
    def parse(s: str):
        (x, y, z) = (int(c) for c in s.strip().split(","))
        return Coordinates(x, y, z)

    def distance(self, other):
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


def union(sets: list[set]):
    result = set()
    for s in sets:
        result = result.union(s)
    return result


def find_circuit(coord: Coordinates, circuits: list[set[Coordinates]]):
    return next((i, circuit) for i, circuit in enumerate(circuits) if coord in circuit)


def connect(c1: Coordinates, c2: Coordinates, circuits: list[set[Coordinates]]):
    (c1_circuit_i, c1_circuit) = find_circuit(c1, circuits)
    if c2 in c1_circuit:
        return
    circuits.pop(c1_circuit_i)
    (c2_circuit_i, c2_circuit) = find_circuit(c2, circuits)
    circuits.pop(c2_circuit_i)
    circuits.append(c1_circuit.union(c2_circuit))


def pairs_by_distance(coordinates: list[Coordinates]):
    pairs = [
        (c1, c2, c1.distance(c2))
        for i, c1 in enumerate(coordinates[:-1])
        for c2 in coordinates[i + 1 :]
    ]
    pairs.sort(key=lambda p: p[2])
    return pairs


with open("08/input.txt") as f:
    all_coordinates = [Coordinates.parse(l) for l in f.readlines()]
    current_circuits: list[set[Coordinates]] = [{c} for c in all_coordinates]
    sorted_pairs = pairs_by_distance(all_coordinates)
    for i, (c1, c2, d) in enumerate(sorted_pairs):
        connect(c1, c2, current_circuits)
        if i == 999:
            current_circuits.sort(key=len, reverse=True)
            print(f"Part 1: {reduce(mul, [len(c) for c in current_circuits[:3]], 1)}")
        if len(current_circuits) == 1:
            print(f"Part 2: {c1.x * c2.x}")
            break
