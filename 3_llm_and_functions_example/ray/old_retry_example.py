# example.py
from aily_ai_brain.common.enums import OpenAIModelID
from aily_py_commons.io.env_vars import COREPRODUCT_DEV, AilySettings
import ray
from old_retry_actors import LangchainActor, AddNumberWithRandomErrorActor


if __name__ == "__main__":
    # Initialize Ray
    ray.init()

    AilySettings(COREPRODUCT_DEV)

    langfuse_tags = [
        "team: genai",
        "environment: dev",
        "project: test_ray",
    ]

    # Chain task
    model_id = OpenAIModelID.GPT35Turbo
    prompt_1 = "What color is the sky? Reply with a single word."
    prompt_2 = "Give the name of an animal with {number} legs. Reply with a single word."
    prompt_3 = "Write a one-line story of a {animal} in {color} field."

    # Create chain configurations instead of actual chains
    chain_config_1 = {
        "model_id": model_id,
        "prompt": prompt_1,
        "tags": langfuse_tags
    }
    chain_config_2 = {
        "model_id": model_id,
        "prompt": prompt_2,
        "tags": langfuse_tags
    }
    chain_config_3 = {
        "model_id": model_id,
        "prompt": prompt_3,
        "tags": langfuse_tags
    }

    # Create task instances with configurations
    chain_1 = LangchainTask.remote(chain_config_1, "Color generator")
    chain_2 = LangchainTask.remote(chain_config_2, "Animal generator")
    chain_3 = LangchainTask.remote(chain_config_3, "Story generator")

    initial_value = 1

    add_2 = AddNumberWithRandomErrorTask.remote(2)
    add_3 = AddNumberWithRandomErrorTask.remote(3)

    # Execute the computational graph
    # First math operations
    x1_ref = add_2.run.remote(initial_value)
    x2_ref = add_3.run.remote(x1_ref)

    # Get color
    x3_ref = chain_1.run.remote({})

    # Wait for the number to be ready before passing to chain_2
    number = ray.get(x2_ref)
    x4_ref = chain_2.run.remote({"number": number})

    # Wait for both color and animal to be ready
    color, animal = ray.get([x3_ref, x4_ref])
    x5_ref = chain_3.run.remote({"animal": animal, "color": color})

    # Get final result
    result = ray.get(x5_ref)
    print(f"{result}")

    # Shut down Ray
    ray.shutdown()