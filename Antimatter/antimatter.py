from typing import List


ANTIMATTER = "antimatter"


def char_list_to_str(chars: List[str]) -> str:
    return "".join(chars)


# timed out on 2 tests in competition
if __name__ == "__main__":
    s = input()
    n = len(ANTIMATTER)
    out = list()
    for i in range(len(s)):
        out.append(s[i])
        if char_list_to_str(out[-n:]) == ANTIMATTER:
            for _ in range(n):
                out.pop()
    print(char_list_to_str(out))
