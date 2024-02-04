from typing import Any
from typing import Dict
from typing import List

from pydantic import model_validator

from tasks.task import BaseTask


class GoogleSearch(BaseTask):
    """
    **Description:**

        This task uses google search to search the query in the internet and returns the urls.

    """

    name: str = "google_search"
    chat_name: str = "GoogleSearch"
    description: str = "Uses google to search the internet for the requested query and returns the url of the top website."
    dependencies: List[str] = []
    inputs: List[str] = ["It should be a search query."]
    outputs: List[str] = [
        "It returns a json object containing key: **url**. For example: {'url': 'http://google.com'}"
    ]
    output_type: bool = False
    search_engine: Any = None

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
            Validate that api key and python package exists in environment.

        Args:
            values (Dict): The dictionary of attribute values.
        Return:
            Dict: The updated dictionary of attribute values.
        Raise:
            ValueError: If the SerpAPI python package is not installed.

        """

        try:
            from googlesearch import search

            values["search_engine"] = search
        except ImportError:
            raise ValueError(
                "Could not import googlesearch python package. "
                "Please install it with `pip install googlesearch-python`."
            )
        return values

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        query = inputs[0]
        result = {"url": list(self.search_engine(query))[0]}
        return result

    def explain(
        self,
    ) -> str:
        return "This task uses google search to search the query in the internet and returns the urls."
