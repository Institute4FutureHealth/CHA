from enum import Enum 

class TaskType(str, Enum):
  SERPAPI = "serpapi"
  CLICK = "click"
  GET_CURRENT_PAGE = "current_page"
  EXTRACT_HYPERLINKS = "extract_hyperlinks"
  EXTRACT_TEXT = "extract_text"
  GET_ELEMENTS = "get_elements"
  NAVIGATE_BACK = "navigate_back"
  NAVIGATE = "navigate"
  AFFECT_SLEEP_AVG = "affect_sleep_avg"
  AFFECT_SLEEP_GET = "affect_sleep_get"
  AFFECT_SLEEP_TREND = "affect_sleep_trend"
  AFFECT_SLEEP_ANALYSIS = "affect_sleep_analysis"
  GOOGLE_TRANSLATE = "google_translate"
  ASK_USER = "ask_user"
  TEST_FILE = "test_file"
