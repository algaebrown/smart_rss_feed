from typing import List, Optional
from src.newsletter import Newsletter

class NewsletterStore:
    def __init__(self):
        self._newsletters: List[Newsletter] = []

    def create(self, newsletter: Newsletter) -> None:
        self._newsletters.append(newsletter)

    def read(self, title: str) -> Optional[Newsletter]:
        for n in self._newsletters:
            if n.title == title:
                return n
        return None

    def update(self, title: str, new_newsletter: Newsletter) -> bool:
        for i, n in enumerate(self._newsletters):
            if n.title == title:
                self._newsletters[i] = new_newsletter
                return True
        return False

    def delete(self, title: str) -> bool:
        for i, n in enumerate(self._newsletters):
            if n.title == title:
                del self._newsletters[i]
                return True
        return False

    def list_all(self) -> List[Newsletter]:
        return list(self._newsletters)
