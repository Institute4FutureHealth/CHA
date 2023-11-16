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
  GOOGLE_TRANSLATE = "google_translate"
  ASK_USER = "ask_user"
  TEST_FILE = "test_file"