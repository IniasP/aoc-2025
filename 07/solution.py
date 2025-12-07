def trace_part1(beams: list[bool], lines: list[str], split_count: int):
    if not lines:
        return split_count
    next_line, *rest_lines = lines
    next_beams = [False] * len(beams)
    for i, (beam, char) in enumerate(zip(beams, next_line)):
        if beam:
            if char == "^":
                split_count += 1
                next_beams[i - 1] = True
                next_beams[i + 1] = True
            else:
                next_beams[i] = True
    return trace_part1(next_beams, rest_lines, split_count)


def trace_part2(timeline_counts: list[int], lines: list[str]):
    if not lines:
        return sum(timeline_counts)
    next_line, *rest_lines = lines
    for i, char in enumerate(next_line):
        if char == "^":
            count = timeline_counts[i]
            timeline_counts[i - 1] += count
            timeline_counts[i + 1] += count
            timeline_counts[i] = 0
    return trace_part2(timeline_counts, rest_lines)


with open("07/input.txt") as f:
    all_lines = [l.strip() for l in f.readlines()]
    first, *rest = all_lines
    beams_init = [c == "S" for c in first]
    timeline_counts_init = [1 if b else 0 for b in beams_init]
    print("Splits:", trace_part1(beams_init, rest, 0))
    print("Timelines:", trace_part2(timeline_counts_init, rest))
