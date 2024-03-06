from __future__ import annotations

from typing import Any
from typing import List

from pydantic import BaseModel

from default_prompts import DefaultPrompts
from llms.llm import BaseLLM


class BaseResponseGenerator(BaseModel):
    """
    **Description:**

        Base class for a response generator, providing a foundation for generating responses using a language model.

    """

    llm_model: BaseLLM = None
    summarize_prompt: bool = True
    max_tokens_allowed: int = 10000

    main_prompt: str = DefaultPrompts.RESPONSE_GENERATOR_MAIN_PROMPT

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
            "===========Thinker:\n{thinker}\n==========\n\n"
            "System: {main_prompt}"
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

        main_prompt = (
            kwargs["response_generator_main_prompt"]
            if "response_generator_main_prompt" in kwargs
            else self.main_prompt
        )

        prompt = (
            self._generator_prompt.replace("{query}", query)
            .replace("{thinker}", thinker)
            .replace("{main_prompt}", main_prompt)
        )
        kwargs["max_tokens"] = 2000
        response = self._response_generator_model.generate(
            query=prompt, **kwargs
        )
        return response
