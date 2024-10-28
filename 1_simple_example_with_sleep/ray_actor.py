import time
import ray


# Define an Actor
@ray.remote
class FunctionActor:
    def f(self, x):
        time.sleep(2)  # Simulating a time-consuming operation
        return x + 1


def initialize_ray():
    print("Initialize Ray")
    init_start_time = time.time()
    ray.init()
    init_end_time = time.time()
    print(f"Time taken to initialize Ray: {init_end_time - init_start_time:.6f} seconds")


def single_actor_execution():
    print("\nUsing a Single Actor:")
    function_actor = FunctionActor.remote()
    start_time = time.time()

    # Call the actor method twice
    x = function_actor.f.remote(1)
    y = function_actor.f.remote(2)

    # Get the results
    result_x = ray.get(x)
    result_y = ray.get(y)

    end_time = time.time()
    print(f"Result of f(1): {result_x}")
    print(f"Result of f(2): {result_y}")
    print(f"Time taken for function execution with a single actor called twice: {end_time - start_time:.6f} seconds")


def two_actors_execution():
    print("\nUsing Two Actors:")
    function_actor_1 = FunctionActor.remote()
    function_actor_2 = FunctionActor.remote()
    start_time = time.time()

    # Call the actor method on both instances
    x = function_actor_1.f.remote(1)
    y = function_actor_2.f.remote(2)

    # Get the results
    result_x = ray.get(x)
    result_y = ray.get(y)

    end_time = time.time()
    print(f"Result of f(1) from actor 1: {result_x}")
    print(f"Result of f(2) from actor 2: {result_y}")
    print(f"Time taken for function execution with two different actors: {end_time - start_time:.6f} seconds")


# Initialize Ray once
initialize_ray()

# Interactive loop for user input
while True:
    print("\nChoose an option:")
    print("1. Execute the single actor experiment")
    print("2. Execute the two actors experiment")
    print("-1. Exit the application")

    user_input = input("Enter your choice: ").strip()

    if user_input == "1":
        single_actor_execution()
    elif user_input == "2":
        two_actors_execution()
    elif user_input == "-1":
        print("Shutting down Ray and exiting the application.")
        ray.shutdown()
        break
    else:
        print("Invalid input. Please enter '1', '2', or '-1'.")
