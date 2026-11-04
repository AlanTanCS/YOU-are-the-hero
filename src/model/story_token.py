from dataclasses import dataclass
from typing import Any

from model import value_types


@dataclass
class Token:
    type: value_types.Types
    value: Any
