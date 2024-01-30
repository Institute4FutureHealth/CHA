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
    AFFECT_SLEEP_GET = "affect_sleep_get"
    AFFECT_ACTIVITY_GET = "affect_activity_get"
    AFFECT_SLEEP_ANALYSIS = "affect_sleep_analysis"
    AFFECT_ACTIVITY_ANALYSIS = "affect_activity_analysis"
    GOOGLE_TRANSLATE = "google_translate"
    ASK_USER = "ask_user"
    READ_FROM_DATAPIPE = "read_from_datapipe"
    TEST_FILE = "test_file"
    RUN_PYTHON_CODE = "run_python_code"
    PPG_GET = "affect_ppg_get"
    PPG_ANALYSIS = "affect_ppg_analysis"
    STRESS_ANALYSIS = "affect_stress_analysis"
