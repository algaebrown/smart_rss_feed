from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Newsletter:
    title: str
    content: str
    publication_date: datetime
    url: Optional[str] = None
