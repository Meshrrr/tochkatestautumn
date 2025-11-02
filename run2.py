import sys
from collections import deque, defaultdict
from typing import List, Tuple, Set


def solve(edges: List[Tuple[str, str]]) -> List[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    result = []

    #Строим граф из рёбер
    graph = defaultdict(list)
    gateways = set()
    nodes = set()

    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)

        nodes.add(node1)
        nodes.add(node2)

        if node1.isupper():
            gateways.add(node1)
        if node2.isupper():
            gateways.add(node2)

    virus_position = "a"

    while True:
        threatened_gateways = find_threatened_gateways(graph, virus_position, gateways)

        if not threatened_gateways:
            break

        edge_to_cut = select_edge_to_cut(graph, threatened_gateways, virus_position)

        result.append(edge_to_cut)

        gate, node = edge_to_cut.split('-')
        graph[gate].remove(node)
        graph[node].remove(gate)

        virus_position = move_virus(graph, virus_position, gateways)

        if virus_position in gateways:
            break

    return result


def find_threatened_gateways(graph, virus_position, gateways):

    threatened = []

    for gateway in sorted(gateways):  # Сортируем для детерминированности
        if has_path(graph, virus_position, gateway):
            threatened.append(gateway)

    return threatened


def has_path(graph, start, end):
    if start == end:
        return True

    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor == end:
                return True
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def select_edge_to_cut(graph, threatened_gateways, virus_position):
    candidate_edges = []

    for gateway in threatened_gateways:
        for node in sorted(graph[gateway]):
            candidate = f"{gateway}-{node}"
            candidate_edges.append(candidate)

    for candidate in candidate_edges:
        gate, node = candidate.split('-')
        if node == virus_position:
            return candidate

    return min(candidate_edges)


def move_virus(graph, current_position, gateways):

    reachable_gateways = []

    for gateway in sorted(gateways):
        distance, path = bfs_shortest_path(graph, current_position, gateway)
        if distance != -1:
            reachable_gateways.append((distance, gateway, path))

    if not reachable_gateways:
        return current_position

    min_distance = min(dist for dist, _, _ in reachable_gateways)

    # Среди шлюзов с минимальным расстоянием выбираем лексикографически меньший
    candidate_gateways = [gw for dist, gw, path in reachable_gateways if dist == min_distance]
    target_gateway = min(candidate_gateways)

    _, _, path_to_target = next((dist, gw, path) for dist, gw, path in reachable_gateways if gw == target_gateway)

    if len(path_to_target) > 1:
        return path_to_target[1]
    else:
        return current_position


def bfs_shortest_path(graph, start, end):
    if start == end:
        return 0, [start]

    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        for neighbor in sorted(graph[current]):
            if neighbor == end:
                return len(path), path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return -1, []


def main():
    # Чтение входных данных
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:  # Если найден дефис
                edges.append((node1, node2))

    result = solve(edges)

    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()