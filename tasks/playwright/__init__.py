"""
Heavily borrowed from langchain tools https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/tools/playwright
"""
from tasks.playwright.click import Click
from tasks.playwright.current_page import CurrentWebPage
from tasks.playwright.extract_hyperlinks import ExtractHyperlinks
from tasks.playwright.extract_text import ExtractText
from tasks.playwright.get_elements import GetElements
from tasks.playwright.navigate import Navigate
from tasks.playwright.navigate_back import NavigateBack

__all__ = [
    "Navigate",
    "NavigateBack",
    "ExtractText",
    "ExtractHyperlinks",
    "GetElements",
    "Click",
    "CurrentWebPage",
]
