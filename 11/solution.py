from collections import deque


def parse_key(line: str):
    return line.split(":")[0]


def parse_val(line: str):
    return line.split(":")[1].strip().split(" ")


with open("11/input.txt") as f:
    lines = f.readlines()
    connections = {parse_key(l): parse_val(l) for l in lines}
    count = 0
    frontier = deque()
    frontier.append("you")
    while frontier:
        current = frontier.popleft()
        neighbors = connections.get(current)
        if not neighbors:
            continue
        for n in neighbors:
            frontier.append(n)
            if n == "out":
                count += 1

    print(count)
