from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List


@dataclass
class Newsletter:
    title: str
    content: str
    publication_date: datetime
    url: Optional[str] = None
    embedding: Optional[List[float]] = None
    tsne: Optional[List[float]] = None
    filters: Dict[str, Any] = (
        None  # e.g. {'date_filter': True, 'AI_filter': {'match': True, ...}}
    )
    full_text: Optional[str] = None  # For storing full text if content is a summary
    user_selected: bool = False
    domain: Optional[str] = None  # e.g. 'tech', 'health', etc.
