import ray

# Initialize Ray
ray.init(ignore_reinit_error=True)

@ray.remote
def inc(i):
    return i + 1

@ray.remote
def dec(i):
    return i - 1

@ray.remote
def add(a, b):
    return a + b

# Define the initial input
x = 1

# Build the computational graph by defining dependencies
# These will execute in parallel since they have no dependencies on each other
y_1 = inc.remote(x)
y_2 = dec.remote(x)

# Add the two results together once both tasks complete
total = add.remote(y_1, y_2)

# Get the result
result = ray.get(total)
print("Result:", result)

# Shut down Ray
ray.shutdown()