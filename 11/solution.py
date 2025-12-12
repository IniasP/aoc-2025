def parse_key(line: str):
    return line.split(":")[0]


def parse_val(line: str):
    return line.split(":")[1].strip().split(" ")


def count_paths(connections: dict[str, list[str]], start: str, goal: str) -> int:
    return do_count_paths(connections, start, goal, {})


def do_count_paths(
    connections: dict[str, list[str]],
    start: str,
    goal: str,
    memo: dict[str, int],
) -> int:
    if start in memo:
        return memo[start]
    if start == goal:
        return 1
    neighbors = connections.get(start)
    if not neighbors:
        return 0
    count = sum(do_count_paths(connections, n, goal, memo) for n in neighbors)
    memo[start] = count
    return count


with open("11/input.txt") as f:
    lines = f.readlines()
    connections = {parse_key(l): parse_val(l) for l in lines}
    print(f"Part 1: {count_paths(connections, "you", "out")}")

    def cp(start, end):
        return count_paths(connections, start, end)

    part_2 = (
        cp("svr", "fft") * cp("fft", "dac") * cp("dac", "out")
        + cp( "svr", "dac") * cp("dac", "fft") * cp("fft", "out")
    )
    print(f"Part 2: {part_2}")
