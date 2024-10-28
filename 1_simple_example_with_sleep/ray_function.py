import time
import ray


@ray.remote
def f(x):
    time.sleep(2)  # Simulating a time-consuming operation
    return x + 1


def initialize_ray():
    print("Initialize Ray")

    # Start timing for Ray initialization
    init_start_time = time.time()

    # Initialize Ray
    ray.init()

    # End timing for Ray initialization
    init_end_time = time.time()

    # Print the time taken to initialize Ray
    print(f"Time taken to initialize Ray: {init_end_time - init_start_time:.6f} seconds")


def execute_function():
    print("Start time")

    # Start timing for function execution
    start_time = time.time()

    # Call the remote function
    x = f.remote(1)
    y = f.remote(2)

    # Get the results
    result_x = ray.get(x)
    result_y = ray.get(y)

    # End timing for function execution
    end_time = time.time()

    # Print the results and the time taken
    print(f"Result of f(1): {result_x}")
    print(f"Result of f(2): {result_y}")
    print(f"Time taken for function execution: {end_time - start_time:.6f} seconds")


# Initialize Ray once
initialize_ray()

# Interactive loop for user input
while True:
    print("\nChoose an option:")
    print("1. Execute the remote function")
    print("-1. Exit the application")

    user_input = input("Enter your choice: ").strip()

    if user_input == "1":
        execute_function()
    elif user_input == "-1":
        print("Shutting down Ray and exiting the application.")
        ray.shutdown()
        break
    else:
        print("Invalid input. Please enter '1' or '-1'.")
