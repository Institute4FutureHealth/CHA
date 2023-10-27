"""
A part of the task implementation is borrowed from LangChain: 
https://github.com/langchain-ai/langchain
"""
from tasks.task import BaseTask
from typing import Any, Optional, List, Dict
from utils import get_from_dict_or_env
from pydantic import Field, model_validator
import aiohttp

class SerpAPI(BaseTask):
  name = "serpapi"
  chat_name = "InternetSearchSerp"
  description = (
      "A low-cost Google Search API."
      "Useful for when you need to answer questions about current events."      
  )
  dependencies = []
  inputs: List[str] = ["It should be a search query."]
  outputs: List[str] = []
  #False if the output should directly passed back to the planner.
  #True if it should be stored in datapipe
  output_type: bool = False

  search_engine: Any  #: :meta private:
  params: dict = Field(
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
    """Validate that api key and python package exists in environment."""
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
    """Get parameters for SerpAPI."""
    _params = {
        "api_key": self.serpapi_api_key,
        "q": query,
    }
    params = {**self.params, **_params}
    return params

  def results(self, query: str) -> dict:
    """Run query through SerpAPI and return the raw result."""
    params = self.get_params(query)
    search = self.search_engine(params)
    res = search.get_dict()
    return res

  @staticmethod
  def _process_response(res: dict) -> str:
    """Process response from SerpAPI."""
    try:
      toret = "link: " + res["organic_results"][0]["link"] + " metadata: " + res["organic_results"][0]["snippet"]
    except KeyError:
      return (
        "Coul not get the proper response from the search. Try another search query."
      )
    return toret


  def execute(
    self,
    input: str,
  ):
    """Run query through SerpAPI and parse result."""
    inputs = self.parse_input(input)
    return self._process_response(self.results(inputs[0]))

  def explain(
        self,
      ):
    return (
      "This task searched in the internet using google search engine, returns the url"
      "and the first top result of the google search."
    )