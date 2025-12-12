from dataclasses import dataclass
from typing import Generator
import numpy as np
from numpy.typing import NDArray


def unique_variants(shape: NDArray):
    all_variants = [shape]
    flipped = np.flip(shape)
    for i in range(3):
        all_variants.append(np.rot90(shape, k=i))
        all_variants.append(np.rot90(flipped, k=i))
    unique_variants: list[NDArray] = []
    for a in all_variants:
        if not any(np.all(a == o) for o in unique_variants):
            unique_variants.append(a)
    return unique_variants


def print_shape(shape: NDArray):
    lst: list[list[bool]] = np.asarray(shape).tolist()
    for row in lst:
        print("".join("#" if b else "." for b in row))
    print()


class Shape:
    shape: NDArray
    unique_variants: list[NDArray]
    area: int

    def __init__(self, shape: NDArray) -> None:
        self.shape = shape
        self.unique_variants = unique_variants(shape)
        self.area = int(np.count_nonzero(shape))


@dataclass
class Region:
    width: int
    length: int
    desired_shape_counts: list[int]

    def as_zeros(self):
        return np.zeros((self.length, self.width), dtype=np.int8)


def split_on_empty_line(lines: list[str]) -> Generator[list[str], None, None]:
    current: list[str] = []
    for l in lines:
        if l:
            current.append(l)
        else:
            yield current
            current = []
    yield current


def parse_shape(lines: list[str]) -> Shape:
    shape = np.array([[c == "#" for c in l] for l in lines[-3:]], dtype=np.int8)
    return Shape(shape)


def parse_region(line: str) -> Region:
    dimensions_str, shapes_str = line.split(": ")
    width, length = [int(s) for s in dimensions_str.split("x")]
    shapes = [int(s) for s in shapes_str.split(" ")]
    return Region(width, length, shapes)


def parse(lines: list[str]) -> tuple[list[Shape], list[Region]]:
    split = list(split_on_empty_line(lines))
    shape_lines = split[:-1]
    region_lines = split[-1]

    shapes = [parse_shape(ls) for ls in shape_lines]
    regions = [parse_region(l) for l in region_lines]
    return shapes, regions


def can_never_fit(region: Region, all_shapes: list[Shape]):
    region_area = region.width * region.length
    min_shape_size = sum(
        all_shapes[i].area * c for i, c in enumerate(region.desired_shape_counts)
    )
    return min_shape_size > region_area


def can_fit_3x3s(region: Region, amount: int):
    total_squares_area = amount * 9
    # defining this correctly doesn't make a difference on the actual input,
    # but it would be incorrect to plainly use the region area
    usable_area_3x3 = region.width // 3 * 3 * region.length // 3 * 3
    return total_squares_area <= usable_area_3x3


def can_fit(region: Region, all_shapes: list[Shape]):
    # all inputs fit into these 2 trivial edge cases
    if can_never_fit(region, all_shapes):
        return False
    if can_fit_3x3s(region, sum(region.desired_shape_counts)):
        return True
    # unreachable on the real input
    return solve_can_fit(region.as_zeros(), region.desired_shape_counts, all_shapes)


def solve_can_fit(field: NDArray, rem_shape_counts: list[int], all_shapes: list[Shape]):
    """
    This function will never be called because the actual input is trolling.
    It is a solution to the general NP-hard problem, and solves the example, but takes very long on even the last example input case.
    """
    x, y = field.shape
    # these are the max translations in x and y that a 3x3 shape can do within the region
    wiggle_x = x - 3
    wiggle_y = y - 3
    if all(c == 0 for c in rem_shape_counts):
        return True
    for shape_i, rem_count in enumerate(rem_shape_counts):
        if rem_count == 0:
            continue
        shape_choice = all_shapes[shape_i]
        for shape_variant in shape_choice.unique_variants:
            for offset_x in range(0, wiggle_x + 1):
                for offset_y in range(0, wiggle_y + 1):
                    shape_positioned = np.pad(
                        shape_variant,
                        (
                            (offset_x, wiggle_x - offset_x),
                            (offset_y, wiggle_y - offset_y),
                        ),
                    )
                    new_field = field + shape_positioned
                    if np.any(new_field > 1):
                        # not a valid position for the shape, it overlaps with existing placements
                        continue
                    new_rem_counts = rem_shape_counts.copy()
                    new_rem_counts[shape_i] -= 1
                    fits = solve_can_fit(new_field, new_rem_counts, all_shapes)
                    if fits:
                        return True
    return False


with open("12/input.txt") as f:
    shapes, regions = parse([l.strip() for l in f.readlines()])
    print(sum(1 if can_fit(region, shapes) else 0 for region in regions))
