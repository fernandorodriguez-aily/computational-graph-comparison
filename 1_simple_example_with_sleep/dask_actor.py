import time
from dask import delayed, compute


class FunctionActor:
    name = "Function"

    @delayed
    def compute(self, x):
        time.sleep(2)  # Simulating a time-consuming operation
        return x + 1


def single_actor_execution():
    print("\nUsing a Single Function Actor:")
    function_actor = FunctionActor()
    start_time = time.time()

    # Create delayed tasks
    x_single = function_actor.compute(1)
    y_single = function_actor.compute(2)

    # Compute results
    result_x_single, result_y_single = compute(x_single, y_single)

    # End timing for single actor execution
    end_time_single = time.time()

    # Print results and time taken
    print(f"Result of f(1) from single actor: {result_x_single}")
    print(f"Result of f(2) from single actor: {result_y_single}")
    print(f"Time taken for function execution using a single actor: {end_time_single - start_time:.6f} seconds")


def two_actors_execution():
    print("\nUsing Two Function Actors:")
    function_actor_1 = FunctionActor()
    function_actor_2 = FunctionActor()
    start_time = time.time()

    # Create delayed tasks
    x_1 = function_actor_1.compute(1)
    y_2 = function_actor_2.compute(2)

    # Compute results
    result_x_1, result_y_2 = compute(x_1, y_2)

    # End timing for two actors execution
    end_time_two = time.time()

    # Print results and time taken
    print(f"Result of f(1) from actor 1: {result_x_1}")
    print(f"Result of f(2) from actor 2: {result_y_2}")
    print(f"Time taken for function execution using two different actors: {end_time_two - start_time:.6f} seconds")


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
        print("Exiting the application.")
        break
    else:
        print("Invalid input. Please enter '1', '2', or '-1'.")
