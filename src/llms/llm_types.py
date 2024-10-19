from enum import Enum


class LLMType(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
