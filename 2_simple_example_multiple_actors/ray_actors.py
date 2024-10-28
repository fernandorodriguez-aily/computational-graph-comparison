import ray

# Initialize Ray
ray.init(ignore_reinit_error=True)

# Define the Increment actor
@ray.remote
class IncrementActor:
    def compute(self, i):
        return i + 1

# Define the Decrement actor
@ray.remote
class DecrementActor:
    def compute(self, i):
        return i - 1

# Define the Add actor
@ray.remote
class AddActor:
    def compute(self, a, b):
        return a + b

# Instantiate actors
inc_actor = IncrementActor.remote()
dec_actor = DecrementActor.remote()
add_actor = AddActor.remote()

# Define the initial input
x = 1

# Use actors to perform the computations
y_1_future = inc_actor.compute.remote(x)  # Increment actor
y_2_future = dec_actor.compute.remote(x)  # Decrement actor

# Add the two results together using the Add actor
total_future = add_actor.compute.remote(y_1_future, y_2_future)

# Get the final result
result = ray.get(total_future)
print("Result:", result)

# Shut down Ray
ray.shutdown()