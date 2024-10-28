from aily_ai_brain.common.enums import OpenAIModelID
from aily_py_commons.io.env_vars import COREPRODUCT_DEV, AilySettings

from tasks import LangchainTask, AddNumberWithRandomErrorTask

from utils import setup_basic_chain

if __name__ == "__main__":

    AilySettings(COREPRODUCT_DEV)

    langfuse_tags = [
        "team: genai",
        "environment: dev",
        "project: test_dask",
    ]

    # Chain task
    model_id = OpenAIModelID.GPT35Turbo
    prompt_1 = "What color is the sky? Reply with a single word."
    prompt_2 = "Give the name of an animal with {number} legs. Reply with a single word."
    prompt_3 = "Write a one-line story of a {animal} in {color} field."

    chain_1 = LangchainTask(setup_basic_chain(model_id, prompt_1, langfuse_tags), "Color generator")
    chain_2 = LangchainTask(setup_basic_chain(model_id, prompt_2, langfuse_tags), "Animal generator")
    chain_3 = LangchainTask(setup_basic_chain(model_id, prompt_3, langfuse_tags), "Story generator")

    initial_value = 1

    add_2 = AddNumberWithRandomErrorTask(2)
    add_3 = AddNumberWithRandomErrorTask(3)

    # Static execution Graph

    # Math operations to get number 6
    x1 = add_2.run(initial_value, dask_key_name="add_2")
    x2 = add_3.run(x1, dask_key_name="add_3")

    # Chain to return the color "blue"
    x3 = chain_1.run({}, dask_key_name="color_generator")

    # Chain to return the name of an animal with 6 legs
    x4 = chain_2.run({"number": x2}, dask_key_name="animal_generator")

    # Chain to write a short story of an {animal} in a blue field
    x5 = chain_3.run({"animal": x4, "color": x3}, dask_key_name="story_generator")

    x5.visualize(filename="example_llms_and_functions.png")

    result = x5.compute()

    print(f"{result}")
