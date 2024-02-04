from __future__ import annotations

from typing import Any
from typing import List

from pydantic import BaseModel

from llms.llm import BaseLLM


class BaseResponseGenerator(BaseModel):
    """
    **Description:**

        Base class for a response generator, providing a foundation for generating responses using a language model.

    """

    llm_model: BaseLLM = None
    prefix: str = ""
    summarize_prompt: bool = True
    max_tokens_allowed: int = 10000

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @property
    def _response_generator_type(self):
        return "base"

    @property
    def _response_generator_model(self):
        return self.llm_model

    @property
    def _generator_prompt(self):
        return (
            "===========Thinker: {thinker}==========\n\n"
            "System: {prefix}. You are very helpful empathetic health assistant and your goal is to help the user to get accurate information about "
            "his/her health and well-being, Using the Thinker gathered information and the History, Provide a empathetic proper answer to the user. "
            "Consider Thinker as your trusted source and use whatever is provided by it."
            "Make sure that the answer is explanatory enough without repeatition"
            "Don't change Thinker returned urls or references. "
            "Also add explanations based on instructions from the "
            "Thinker don't directly put the instructions in the final answer to the user."
            "Never answer outside of the Thinker's provided information."
            "Additionally, refrain from including or using any keys, such as 'datapipe:6d808840-1fbe-45a5-859a-abfbfee93d0e,' in your final response."
            "Return all `address:[path]` exactly as they are."
            "User: {query}"
        )

    @property
    def _shorten_prompt(self):
        return (
            "Summarize the following text. Make sure to keep the main ideas "
            "and objectives in the summary. Keep the links "
            "exactly as they are: "
            "{chunk}"
        )

    def divide_text_into_chunks(
        self,
        input_text: str = "",
        max_tokens: int = 10000,
    ) -> List[str]:
        """
        Generate a response based on the input prefix, query, and thinker (task planner).

        Args:
            input_text (str): the input text (e.g., prompt).
            max_tokens (int): Maximum number of tokens allowed.
        Return:
            chunks(List): List of string variables
        """
        # 1 token ~= 4 chars in English
        chunks = [
            input_text[i : i + max_tokens * 4]
            for i in range(0, len(input_text), max_tokens * 4)
        ]
        return chunks

    def summarize_thinker_response(self, thinker, **kwargs):
        chunks = self.divide_text_into_chunks(
            input_text=thinker, max_tokens=self.max_tokens_allowed
        )
        thinker = ""
        kwargs["max_tokens"] = min(
            2000, int(self.max_tokens_allowed / len(chunks))
        )
        for chunk in chunks:
            prompt = self._shorten_prompt.replace("{chunk}", chunk)
            chunk_summary = self._response_generator_model.generate(
                query=prompt, **kwargs
            )
            thinker += chunk_summary + " "
        return thinker

    def generate(
        self,
        prefix: str = "",
        query: str = "",
        thinker: str = "",
        **kwargs: Any,
    ) -> str:
        """
        Generate a response based on the input prefix, query, and thinker (task planner).

        Args:
            prefix (str): Prefix to be added to the response.
            query (str): User's input query.
            thinker (str): Thinker's (Task Planner) generated answer.
            **kwargs (Any): Additional keyword arguments.
        Return:
            str: Generated response.



        Example:
            .. code-block:: python

                from llms.llm_types import LLMType
                from response_generators.response_generator_types import ResponseGeneratorType
                response_generator = initialize_planner(llm=LLMType.OPENAI, response_generator=ResponseGeneratorType.BASE_GENERATOR)
                response_generator.generate(query="How can I improve my sleep?", thinker="Based on data found on the internet there are several ...")
        """

        if (
            self.summarize_prompt
            and len(thinker) / 4 > self.max_tokens_allowed
        ):
            thinker = self.summarize_thinker_response(thinker)

        prompt = (
            self._generator_prompt.replace("{query}", query)
            .replace("{thinker}", thinker)
            .replace("{prefix}", prefix)
        )
        kwargs["max_tokens"] = 2000
        response = self._response_generator_model.generate(
            query=prompt, **kwargs
        )
        return response
