NO = "no"
YES = "yes"
UNSURE = "unsure"


if __name__ == "__main__":
    n_issues = int(input())
    issue_points = dict()
    issue_order = list()
    for _ in range(n_issues):
        issue = input()
        issue_points[issue] = 0
        issue_order.append(issue)
    n_polls = int(input())
    for _ in range(n_polls):
        for _ in range(n_issues):
            line = input()
            issue, vote = line.split()
            if vote == YES:
                issue_points[issue] += 1
            elif vote == NO:
                issue_points[issue] -= 2
    for issue in issue_order:
        if issue_points[issue] < 0:
            print(f"{issue} no")
        elif issue_points[issue] > 0:
            print(f"{issue} yes")
        else:  # issue_points[issue] == 0:
            print(f"{issue} abstain")
