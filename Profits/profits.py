LIMIT = 5000


# didn't finish coding
if __name__ == "__main__":
    # get input
    n_months = int(input())
    n_stocks = int(input())
    stock_histories = dict()
    for _ in range(n_stocks):
        stock_name = input()
        stock_values = input().split()
        stock_histories[stock_name] = [int(c) for c in stock_values]
    # solve
    for i in range(n_months):
        these_stock_values = {stock: stock_histories[stock][i] for stock in stock_histories}
        max_purchase_count = {stock: LIMIT // cost for stock, cost in these_stock_values.items()}
    # print the answer
    # print(f"Max: {}")
    # print(f"Min: {}")
