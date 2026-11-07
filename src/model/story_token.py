from dataclasses import dataclass
from typing import Any

from model import value_types
from model.syntax import Namespace


@dataclass
class Token:
    type: value_types.Types
    value: Any
    namespace: Namespace | None = None
