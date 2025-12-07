def trace_part1(beams: list[bool], lines: list[str], width: int, split_count: int):
    if not lines:
        return split_count
    next_line, *rest_lines = lines
    next_beams = [False] * width
    for i, (beam, char) in enumerate(zip(beams, next_line)):
        if beam:
            if char == "^":
                split_count += 1
                next_beams[i-1] = True
                next_beams[i+1] = True
            else:
                next_beams[i] = True
    return trace_part1(next_beams, rest_lines, width, split_count)


with open("07/input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    first, *rest = lines
    beams = [c == "S" for c in first]
    print(trace_part1(beams, rest, len(beams), 0))
