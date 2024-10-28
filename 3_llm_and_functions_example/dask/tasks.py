import secrets

from abc import ABC, abstractmethod
from typing import Any
from langchain_core.runnables.base import Runnable
from dask import delayed
from tenacity import retry, stop_after_attempt, wait_fixed

from aily_py_commons.aily_logging import aily_logging as logging

class Task(ABC):

    # Decorators do not apply, need to be manually added in subclasses
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    @delayed
    @abstractmethod
    def run(self, x: Any):
        pass


class LangchainTask(Task):

    def __init__(self, chain: Runnable, name: str):
        self._chain = chain
        self._name = name

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    @delayed
    def run(self, x: Any):
        logging.info(f"LangchainTask({self._name}): Receiving {x}")
        return self._chain.invoke(x)


class AddNumberWithRandomErrorTask(Task):

    def __init__(self, number: int):
        self._number = number

    @delayed
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def run(self, x: int) -> int:
        logging.info(f"AddNumberTask({self._number}): Receiving {x}")
        if secrets.randbelow(100) / 100.0 > 0.7:  # More secure random
            logging.error(f"AddNumberTask({self._number}): Encountered an error")
            raise ValueError(f"AddNumberTask({self._number}): Encountered an error")
        return x + self._number
