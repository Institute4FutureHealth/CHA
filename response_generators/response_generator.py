from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from llms.llm import BaseLLM


class BaseResponseGenerator(BaseModel):
    """
    **Description:**

        Base class for a response generator, providing a foundation for generating responses using a language model.

    """

    llm_model: BaseLLM = None
    prefix: str = ""

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
            "You should perform final calculations or process on the gathered information to provide the final answer. "
            "Also add explanations based on instructions from the "
            "Thinker don't directly put the instructions in the final answer to the user."
            "Return all `address:[path]` exactly as they are."
            "User: {query}"
        )

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

        prompt = (
            self._generator_prompt.replace("{query}", query)
            .replace("{thinker}", thinker)
            .replace("{prefix}", prefix)
        )
        kwargs["max_tokens"] = 1000
        response = self._response_generator_model.generate(
            query=prompt, **kwargs
        )
        return response
