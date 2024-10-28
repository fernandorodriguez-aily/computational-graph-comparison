from dask import delayed
import dask

class IncrementActor:

    name = "Increment"

    @delayed
    def compute(self, i):
        return delayed(lambda x: x + 1)(i)

class DecrementActor:

    name = "Decrement"

    @delayed
    def compute(self, i):
        return delayed(lambda x: x - 1)(i)

class AddActor:

    name = "Add"

    @delayed
    def compute(self, a, b):
        return delayed(lambda x, y: x + y)(a, b)

# Instantiate actors
inc_actor = IncrementActor()
dec_actor = DecrementActor()
add_actor = AddActor()

# Define the initial input
x = 1

# Use actors to perform the computations
y_1 = inc_actor.compute(x, dask_key_name=inc_actor.name)  # Increment actor
y_2 = dec_actor.compute(x, dask_key_name=dec_actor.name) # Decrement actor

# Add the two results together using the Add actor
total = add_actor.compute(y_1, y_2, dask_key_name=add_actor.name)

# Visualize the computational graph
total.visualize(rankdir='LR', filename="dask_actors.png")

# Compute the result
result = total.compute()
print("Result:", result)