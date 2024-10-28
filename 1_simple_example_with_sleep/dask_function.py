import time
from dask import delayed, compute


# Define a delayed function
@delayed
def f(x):
    time.sleep(2)  # Simulating a time-consuming operation
    return x + 1


def execute_tasks():
    print("\nExecuting delayed tasks...")
    start_time = time.time()

    # Create delayed tasks
    x = f(1)
    y = f(2)

    # Compute results
    result_x, result_y = compute(x, y)

    # End timing for function execution
    end_time = time.time()

    # Print results and time taken
    print(f"Result of f(1): {result_x}")
    print(f"Result of f(2): {result_y}")
    print(f"Time taken for function execution: {end_time - start_time:.6f} seconds")


# Interactive loop for user input
while True:
    print("\nChoose an option:")
    print("1. Execute the delayed tasks")
    print("-1. Exit the application")

    user_input = input("Enter your choice: ").strip()

    if user_input == "1":
        execute_tasks()
    elif user_input == "-1":
        print("Exiting the application.")
        break
    else:
        print("Invalid input. Please enter '1' or '-1'.")
