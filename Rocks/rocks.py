LEFT = 0
CENTER = 1
RIGHT = 2


if __name__ == "__main__":
    # get input
    n_days = int(input())
    left_drill_amounts = list()
    for _ in range(n_days):
        left_drill_amounts.append(int(input()))
    right_drill_amounts = list()
    for _ in range(n_days):
        right_drill_amounts.append(int(input()))
    # figure out the best path
    previous_options = [left_drill_amounts[0], 0, right_drill_amounts[0]]
    for i in range(1, n_days):
        next_left = left_drill_amounts[i] + max(previous_options[LEFT], previous_options[CENTER])
        next_center = max(previous_options)
        next_right = right_drill_amounts[i] + max(previous_options[CENTER], previous_options[RIGHT])
        previous_options = [next_left, next_center, next_right]
    print(max(previous_options))
