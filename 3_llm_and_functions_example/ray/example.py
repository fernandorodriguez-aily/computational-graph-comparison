# example.py
import ray
from aily_ai_brain.common.enums import OpenAIModelID
from aily_py_commons.io.env_vars import COREPRODUCT_DEV, AilySettings
from actors import LangchainActor, AddNumberWithRandomErrorActor
from aily_py_commons.aily_logging import aily_logging as logging

# Helper function to call the actor's run method with custom retries
@ray.remote
def run_with_retries(actor, *args, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return ray.get(actor.run.remote(*args, **kwargs))
        except Exception as e:
            # Log error with aily_logging
            logging.error(f"Attempt {attempt + 1}/{max_retries} for {actor} failed with error: {str(e)}")
            if attempt == max_retries - 1:
                logging.error(f"Final attempt failed for {actor}. No more retries.")
                raise


if __name__ == "__main__":
    # Initialize Ray
    ray.init()

    # Initialize environment variables or settings
    AilySettings(COREPRODUCT_DEV)

    langfuse_tags = [
        "team: genai",
        "environment: dev",
        "project: test_ray",
    ]

    # Chain task configurations
    model_id = OpenAIModelID.GPT35Turbo
    chain_config_1 = {
        "model_id": model_id,
        "prompt": "What color is the sky? Reply with a single word.",
        "tags": langfuse_tags
    }
    chain_config_2 = {
        "model_id": model_id,
        "prompt": "Give the name of an animal with {number} legs. Reply with a single word.",
        "tags": langfuse_tags
    }
    chain_config_3 = {
        "model_id": model_id,
        "prompt": "Write a one-line story of a {animal} in {color} field.",
        "tags": langfuse_tags
    }

    # Create Ray remote actor instances with configurations
    chain_1 = LangchainActor.remote(chain_config_1, "Color generator")
    chain_2 = LangchainActor.remote(chain_config_2, "Animal generator")
    chain_3 = LangchainActor.remote(chain_config_3, "Story generator")

    initial_value = 1

    # Initialize add tasks as remote actors
    add_2 = AddNumberWithRandomErrorActor.remote(2)
    add_3 = AddNumberWithRandomErrorActor.remote(3)

    # Execute the computational graph
    # First math operations
    x1_ref = run_with_retries.remote(add_2, initial_value)  # x1 = initial_value + 2
    x2_ref = run_with_retries.remote(add_3, x1_ref)  # x2 = x1 + 3

    # Get color
    x3_ref = run_with_retries.remote(chain_1, {})  # x3: color result

    # Wait for the number to be ready before passing to chain_2
    number = ray.get(x2_ref)
    x4_ref = run_with_retries.remote(chain_2, {"number": number})  # x4: animal result based on x2 (number)

    # Wait for both color and animal to be ready
    color, animal = ray.get([x3_ref, x4_ref])
    x5_ref = run_with_retries.remote(chain_3, {"animal": animal, "color": color})  # x5: final story result

    # Get final result
    result = ray.get(x5_ref)
    print(f"{result}")

    # Shut down Ray
    ray.shutdown()
