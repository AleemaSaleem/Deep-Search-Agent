from dataclasses import dataclass
from typing import Optional

@dataclass
class UserContext:
    username: str
    search_count: int = 0
