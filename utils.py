import os
import re
from typing import Any
from typing import Dict
from typing import Optional


def get_from_dict_or_env(
    data: Dict[str, Any],
    key: str,
    env_key: str,
    default: Optional[str] = None,
) -> str:
    """Get a value from a dictionary or an environment variable."""
    if key in data and data[key]:
        return data[key]
    else:
        return get_from_env(key, env_key, default=default)


def get_from_env(
    key: str, env_key: str, default: Optional[str] = None
) -> str:
    """Get a value from a dictionary or an environment variable."""
    if env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )


def parse_addresses(input_string: str):
    pattern = r"address:([a-zA-Z0-9/_-]+\.(?:png|csv|json|wav))"
    cleaned_text = re.sub(pattern, "", input_string)
    addresses = re.findall(pattern, input_string)
    return cleaned_text, addresses
