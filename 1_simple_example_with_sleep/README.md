# Parallelization Demonstration with Ray and Dask

This directory showcases examples of parallel execution using Ray and Dask. Each file demonstrates how these libraries parallelize tasks using decorators.

> **Key Difference Between Dask and Ray:**  
> * In Dask, you can create a single actor and call it multiple times since the `delayed` decorator is applied directly to the method.
> * In Ray, we are required to creating a new object each time it’s needed because the `remote` decorator is applied at the class level.

## Files

- **`dask_function.py`**: Implements Dask's `delayed` functionality to simulate a time-consuming operation and run multiple tasks in parallel.

- **`dask_actor.py`**: Demonstrates Dask's actor model by comparing the execution time of a single actor versus multiple actors.

- **`ray_function.py`**: Uses Ray's `remote` function to simulate a time-consuming operation, executing it concurrently with different arguments.

- **`ray_actor.py`**: Demonstrates Ray's actor model, comparing the execution time of using a single actor versus multiple actors.
