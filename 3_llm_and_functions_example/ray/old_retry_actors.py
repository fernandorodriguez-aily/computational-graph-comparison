# actors.py
import secrets
from abc import ABC, abstractmethod
from typing import Any, Dict
import ray
from tenacity import retry, stop_after_attempt, wait_fixed
from aily_py_commons.aily_logging import aily_logging as logging


class Actor(ABC):
    @abstractmethod
    def run(self, x: Any):
        pass


@ray.remote
class LangchainActor(Actor):
    def __init__(self, chain_config: Dict, name: str):
        self._chain_config = chain_config
        self._name = name
        self._chain = None

    def _initialize_chain(self):
        if self._chain is None:
            from utils import setup_basic_chain
            self._chain = setup_basic_chain(
                self._chain_config["model_id"],
                self._chain_config["prompt"],
                self._chain_config["tags"]
            )

    def run(self, x: Any):
        logging.info(f"LangchainActor({self._name}): Receiving {x}")

        # Define retry decorator inside the method
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
        def _run_with_retry():
            self._initialize_chain()
            return self._chain.invoke(x)

        return _run_with_retry()


@ray.remote
class AddNumberWithRandomErrorActor(Actor):
    def __init__(self, number: int):
        self._number = number

    def run(self, x: int) -> int:
        logging.info(f"AddNumberWithRandomErrorActor({self._number}): Receiving {x}")

        @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
        def _run_with_retry():
            error_prob = 0.3
            if secrets.randbelow(100) / 100.0 < error_prob:
                logging.error(f"AddNumberWithRandomErrorActor({self._number}): Encountered an error")
                raise ValueError(f"AddNumberWithRandomErrorActor({self._number}): Encountered an error")
            return x + self._number

        return _run_with_retry()
