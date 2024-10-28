from dask import delayed

@delayed
def inc(i):
    return i + 1

@delayed
def dec(i):
    return i - 1

@delayed
def add(a, b):
    return a + b

x = 1
y_1 = inc(x)
y_2 = dec(x)
total = add(y_1, y_2)

total.visualize(rankdir='LR', filename="dask_functions.png")

result = total.compute()

print("Result:", result)