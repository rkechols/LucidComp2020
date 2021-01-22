if __name__ == "__main__":
    max_rockets = -1
    n_part_types = int(input())
    for _ in range(n_part_types):
        line = input()
        part_required_str, part_have_str = line.split()
        part_required = int(part_required_str)
        part_have = int(part_have_str)
        this_number_of_rockets = part_have // part_required
        if max_rockets == -1 or max_rockets > this_number_of_rockets:
            max_rockets = this_number_of_rockets
    print(max_rockets)
