if __name__ == "__main__":
    n_vertices_str, n_edges_str = input().split()
    n_vertices, n_edges = int(n_vertices_str), int(n_edges_str)
    planet_sets = list()
    planet_to_set_index = dict()
    for i in range(n_vertices):
        planet = input()
        planet_sets.append({planet})
        planet_to_set_index[planet] = i
    edges_unused = dict()
    weights = list()
    for _ in range(n_edges):
        x, y, w_str = input().split()
        w = int(w_str)
        if w not in edges_unused:
            edges_unused[w] = set()
            weights.append(w)
        edges_unused[w].add((x, y))
    weights.sort()
    # run Kruskal's algorithm
    total_weight = 0
    while len(planet_sets) > 1:
        for w in weights:
            added_edge = False
            for x, y in edges_unused[w]:
                x_set_index = planet_to_set_index[x]
                x_set = planet_sets[x_set_index]
                y_set_index = planet_to_set_index[y]
                y_set = planet_sets[y_set_index]
                if x_set_index != y_set_index:
                    # they're in different sets
                    first_shifted = min(x_set_index, y_set_index)
                    second_shifted = max(x_set_index, y_set_index)
                    if x_set_index > y_set_index:
                        planet_sets.pop(x_set_index)
                        planet_sets.pop(y_set_index)
                    else:
                        planet_sets.pop(y_set_index)
                        planet_sets.pop(x_set_index)
                    # adjust other things that got shifted
                    for i in range(first_shifted, second_shifted - 1):
                        for planet in planet_sets[i]:
                            planet_to_set_index[planet] -= 1
                    for i in range(second_shifted - 1, len(planet_sets)):
                        for planet in planet_sets[i]:
                            planet_to_set_index[planet] -= 2
                    new_index = len(planet_sets)
                    new_set = x_set.union(y_set)
                    planet_sets.append(new_set)

                    for planet in new_set:
                        planet_to_set_index[planet] = new_index
                    total_weight += w
                    added_edge = True
                    break
            if added_edge:
                break
    print(total_weight)
