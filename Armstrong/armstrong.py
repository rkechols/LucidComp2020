import re
from typing import List, Set


TARGET = "Neil Armstrong"


class Graph:
    def __init__(self, vertices: Set[str]):
        self.n = len(vertices)
        self.neighbors = dict()
        for v in vertices:
            self.neighbors[v] = set()

    def add_edge(self, start: str, end: str):
        if start not in self.neighbors:
            raise ValueError("Starting vertex not found")
        if end not in self.neighbors:
            raise ValueError("Ending vertex not found")
        self.neighbors[start].add(end)

    def bfs(self, start: str, end: str) -> List[str]:
        # check validity
        if start not in self.neighbors:
            raise ValueError("Starting vertex not found")
        if end not in self.neighbors:
            raise ValueError("Ending vertex not found")
        # start the BFS
        q = [start]
        visited = {v: False for v in self.neighbors}
        previous = {start: None}
        while len(q) > 0:
            current = q.pop(0)
            if visited[current]:
                # already got to this one by some other path
                continue
            visited[current] = True
            for next_v in self.neighbors[current]:
                if visited[next_v]:
                    # already got to this one by some other path
                    continue
                q.append(next_v)
                previous[next_v] = current
                if next_v == end:
                    # we found it! now trace back to the start
                    answer = list()
                    this_v = end
                    while this_v is not None:
                        answer.append(this_v)
                        this_v = previous[this_v]
                    return answer
        # ran out of things in the queue, no solution
        raise RuntimeError("No solution found!")


if __name__ == "__main__":
    # read input
    source_name = input().strip()
    n_pairs = int(input())
    edge_re = re.compile(r"(.*)->(.*)")
    edge_list = list()
    all_names = set()
    for _ in range(n_pairs):
        line = input()
        re_match = edge_re.match(line)
        child = re_match.group(1).strip()
        parent = re_match.group(2).strip()
        edge_list.append((child, parent))
        all_names.add(child)
        all_names.add(parent)

    g = Graph(all_names)
    for child, parent in edge_list:
        g.add_edge(child, parent)

    answer_list = g.bfs(source_name, TARGET)
    for name in answer_list:
        print(name)
