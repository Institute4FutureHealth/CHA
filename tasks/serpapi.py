"""
A part of the task implementation is borrowed from LangChain: 
https://github.com/langchain-ai/langchain
"""
from tasks.task import BaseTask
from typing import Any, Optional, List, Dict
from utils import get_from_dict_or_env
from pydantic import Field, model_validator, Extra
import aiohttp


class SerpAPI(BaseTask):
    name: str = "serpapi"
    chat_name: str = "InternetSearchSerp"
    description: str = (
        "A low-cost Google Search API."
        "Useful for when you need to answer questions about current events."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["It should be a search query."]
    outputs: List[str] = []
    output_type: bool = False

    search_engine: Any = None  #: :meta private:
    params: Dict = Field(
        default={
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
    )
    serpapi_api_key: Optional[str] = None
    aiosession: Optional[aiohttp.ClientSession] = None

    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        """
        Validate that api key and python package exists in environment.

        Args:
            values (Dict): The dictionary of attribute values.
        Return:
            Dict: The updated dictionary of attribute values.
        Raise:
            ValueError: If the SerpAPI python package is not installed.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        serpapi_api_key = get_from_dict_or_env(
            values, "serpapi_api_key", "SERPAPI_API_KEY"
        )
        values["serpapi_api_key"] = serpapi_api_key
        try:
            from serpapi import GoogleSearch

            values["search_engine"] = GoogleSearch
        except ImportError:
            raise ValueError(
                "Could not import serpapi python package. "
                "Please install it with `pip install google-search-results`."
            )
        return values

    def get_params(self, query: str) -> Dict[str, str]:
        """
        Get parameters for SerpAPI.

        Args:
            query (str): The search query.
        Return:
            Dict[str, str]: The parameters for the SerpAPI.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        _params = {
            "api_key": self.serpapi_api_key,
            "q": query,
        }
        params = {**self.params, **_params}
        return params

    def results(self, query: str) -> Dict:
        """
        Run query through SerpAPI and return the raw result.

        Args:
            query (str): The search query.
        Return:
            Dict: The raw result from the SerpAPI.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        params = self.get_params(query)
        search = self.search_engine(params)
        res = search.get_dict()
        return res

    @staticmethod
    def _process_response(res: Dict) -> str:
        """
        Process response from SerpAPI.

        Args:
            res (Dict): The raw response from the SerpAPI.
        Return:
            str: Processed information from the SerpAPI response.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        try:
            toret = "url: " + res["organic_results"][0]["link"] + "\nmetadata: " + res["organic_results"][0]["snippet"]
        except KeyError:
            return (
                "Could not get the proper response from the search. Try another search query."
            )
        return toret

    def execute(
            self,
            input: str,
    ) -> str:
        """
        Run query through SerpAPI and parse result.

        Args:
            input (str): The input, which should be a search query.
        Return:
            str: The parsed result from the SerpAPI.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        inputs = self.parse_input(input)
        return self._process_response(self.results(inputs[0]))

    def explain(
            self,
    ) -> str:
        """
        Provide an explanation of the task.

        Return:
            str: Explanation of the SerpAPI task.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return (
            "This task searched in the internet using google search engine, returns the url"
            "and the first top result of the google search."
        )
