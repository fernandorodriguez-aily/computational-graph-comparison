from aily_ai_brain.common.langfuse_handler import get_langfuse_handler
from aily_ai_brain.modules.llms.llm_selector import get_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def setup_basic_chain(model_id: str, prompt: str, langfuse_tags: list[str]):
    prompt_template = ChatPromptTemplate.from_template(
        template=prompt,
    )
    langfuse_handler = get_langfuse_handler(
        langfuse_tags=langfuse_tags,
    )
    llm = get_llm(
        langfuse_handler=langfuse_handler,
        sensitive_data=False,
        model_id=model_id,
    )
    output_parser = StrOutputParser()

    return prompt_template | llm | output_parser
