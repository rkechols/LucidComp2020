import math
from typing import List


EMPTY = "empty"


def get_child_left_index(parent_index: int) -> int:
    return parent_index * 2


def get_child_right_index(parent_index: int) -> int:
    return 1 + parent_index * 2


def get_parent_index(child_index: int) -> int:
    return child_index // 2


def explore(tree: List[List[str]], current_level: int, current_index: int):
    if current_level == len(tree) - 1:
        # we hit the bottom
        return
    this_num = int(tree[current_level][current_index])
    next_level = current_level + 1
    left_index = get_child_left_index(current_index)
    left_str = tree[next_level][left_index]
    right_index = get_child_right_index(current_index)
    right_str = tree[next_level][right_index]
    if left_str != EMPTY:
        left = int(left_str)
        if left > this_num:
            # found it!
            print(f"Swap nodes {this_num} and {left}")
            exit()
        explore(tree, next_level, left_index)
    if right_str != EMPTY:
        right = int(right_str)
        if right < this_num:
            # found it!
            print(f"Swap nodes {right} and {this_num}")
            exit()
        explore(tree, next_level, right_index)
    return


def get_in_order(tree: List[List[str]], current_level: int, current_index: int) -> List[int]:
    this_value_str = tree[current_level][current_index]
    if this_value_str == EMPTY:
        return list()
    this_value_list = [int(this_value_str)]
    if current_level == len(tree) - 1:
        # we hit the bottom
        return this_value_list
    left_list = get_in_order(tree, current_level + 1, get_child_left_index(current_index))
    right_list = get_in_order(tree, current_level + 1, get_child_right_index(current_index))
    return left_list + this_value_list + right_list


if __name__ == "__main__":
    # read input
    n_nodes = int(input())
    levels = int(math.log2(n_nodes + 1))
    tree_ = list()
    for level_number in range(levels):
        level = list()
        for _ in range(int(math.pow(2, level_number))):
            level.append(input())
        tree_.append(level)
    # get in-order traversal
    in_order = get_in_order(tree_, 0, 0)
    left_to_swap_index = None
    right_to_swap_index = None
    for i in range(len(in_order) - 1):
        if in_order[i] > in_order[i + 1]:
            if left_to_swap_index is None:
                left_to_swap_index = i
            else:
                right_to_swap_index = i + 1
    if left_to_swap_index is None:
        raise RuntimeError("No solution found!")
    if right_to_swap_index is None:
        right_to_swap_index = left_to_swap_index + 1
    print(f"Swap nodes {in_order[right_to_swap_index]} and {in_order[left_to_swap_index]}")
