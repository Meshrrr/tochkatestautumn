import sys
import heapq
from typing import List, Tuple, Dict


def solve(lines: List[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    ROOM_POSITIONS = [2, 4, 6, 8]
    FORBIDDEN_STOPS = [2, 4, 6, 8]
    ENERGY_COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    TARGET_ROOMS = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    def parse_input(lines: List[str]) -> Tuple[Tuple[str, ...], Tuple[Tuple[str, ...], ...]]:
        room_depth = len(lines) - 3
        hallway = tuple('.' for _ in range(11))
        rooms = []

        for room_idx in range(4):
            room = []
            for depth in range(room_depth):
                char = lines[2 + depth][3 + room_idx * 2]
                room.append(char)
            rooms.append(tuple(room))

        return hallway, tuple(rooms)

    def is_goal_state(rooms: Tuple[Tuple[str, ...], ...], room_depth: int) -> bool:
        target_types = ['A', 'B', 'C', 'D']
        for room_idx, expected_type in enumerate(target_types):
            room = rooms[room_idx]
            if len(room) != room_depth or any(obj != expected_type for obj in room):
                return False
        return True

    def can_enter_room(rooms: Tuple[Tuple[str, ...], ...], room_idx: int, obj_type: str) -> bool:
        room = rooms[room_idx]
        return all(obj == '.' or obj == obj_type for obj in room)

    def is_path_clear(hallway: Tuple[str, ...], start: int, end: int) -> bool:
        if start == end:
            return True
        step = 1 if end > start else -1
        for pos in range(start + step, end + step, step):
            if hallway[pos] != '.':
                return False
        return True

    def get_valid_moves(hallway: Tuple[str, ...], rooms: Tuple[Tuple[str, ...], ...]) -> List[Tuple]:
        moves = []
        room_depth = len(rooms[0])

        for hall_pos in range(11):
            if hallway[hall_pos] != '.':
                obj_type = hallway[hall_pos]
                target_room = TARGET_ROOMS[obj_type]
                room_hall_pos = ROOM_POSITIONS[target_room]

                if (can_enter_room(rooms, target_room, obj_type) and
                        is_path_clear(hallway, hall_pos, room_hall_pos)):

                    for depth in range(room_depth - 1, -1, -1):
                        if rooms[target_room][depth] == '.':
                            steps = abs(hall_pos - room_hall_pos) + depth + 1
                            moves.append(('hall_to_room', hall_pos, target_room, depth, steps, obj_type))
                            break

        for room_idx in range(4):
            room = rooms[room_idx]

            top_depth = -1
            for depth in range(room_depth):
                if room[depth] != '.':
                    top_depth = depth
                    break

            if top_depth == -1:
                continue

            obj_type = room[top_depth]
            room_hall_pos = ROOM_POSITIONS[room_idx]

            if (TARGET_ROOMS[obj_type] == room_idx and
                    all(room[d] == obj_type for d in range(top_depth, room_depth))):
                continue

            for target_pos in range(room_hall_pos - 1, -1, -1):
                if target_pos in FORBIDDEN_STOPS:
                    continue
                if hallway[target_pos] != '.':
                    break
                steps = abs(room_hall_pos - target_pos) + top_depth + 1
                moves.append(('room_to_hall', room_idx, top_depth, target_pos, steps, obj_type))

            for target_pos in range(room_hall_pos + 1, 11):
                if target_pos in FORBIDDEN_STOPS:
                    continue
                if hallway[target_pos] != '.':
                    break
                steps = abs(room_hall_pos - target_pos) + top_depth + 1
                moves.append(('room_to_hall', room_idx, top_depth, target_pos, steps, obj_type))

        return moves

    def apply_move(hallway: Tuple[str, ...], rooms: Tuple[Tuple[str, ...], ...], move: Tuple) -> Tuple[
        Tuple[str, ...], Tuple[Tuple[str, ...], ...], int]:
        move_type, *args = move

        if move_type == 'hall_to_room':
            hall_pos, room_idx, depth, steps, obj_type = args

            new_hallway_list = list(hallway)
            new_hallway_list[hall_pos] = '.'
            new_hallway = tuple(new_hallway_list)

            new_rooms_list = [list(room) for room in rooms]
            new_rooms_list[room_idx][depth] = obj_type
            new_rooms = tuple(tuple(room) for room in new_rooms_list)

            energy = steps * ENERGY_COSTS[obj_type]

            return new_hallway, new_rooms, energy

        else:
            room_idx, depth, hall_pos, steps, obj_type = args

            new_hallway_list = list(hallway)
            new_hallway_list[hall_pos] = obj_type
            new_hallway = tuple(new_hallway_list)

            new_rooms_list = [list(room) for room in rooms]
            new_rooms_list[room_idx][depth] = '.'
            new_rooms = tuple(tuple(room) for room in new_rooms_list)

            energy = steps * ENERGY_COSTS[obj_type]

            return new_hallway, new_rooms, energy

    initial_hallway, initial_rooms = parse_input(lines)
    room_depth = len(initial_rooms[0])

    queue = [(0, initial_hallway, initial_rooms)]
    min_energy = {(initial_hallway, initial_rooms): 0}

    while queue:
        current_energy, current_hallway, current_rooms = heapq.heappop(queue)

        if current_energy > min_energy.get((current_hallway, current_rooms), float('inf')):
            continue

        if is_goal_state(current_rooms, room_depth):
            return current_energy

        for move in get_valid_moves(current_hallway, current_rooms):
            new_hallway, new_rooms, move_energy = apply_move(current_hallway, current_rooms, move)
            total_energy = current_energy + move_energy

            state_key = (new_hallway, new_rooms)
            if total_energy < min_energy.get(state_key, float('inf')):
                min_energy[state_key] = total_energy
                heapq.heappush(queue, (total_energy, new_hallway, new_rooms))

    return -1


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)

#reshenie

if __name__ == "__main__":
    main()