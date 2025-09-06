from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    password_hash: str
    profile_info: Optional[str] = None
