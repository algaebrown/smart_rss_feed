from typing import List, Optional
from user import User


class UserStore:
    def __init__(self):
        self._users: List[User] = []

    def create(self, user: User) -> None:
        self._users.append(user)

    def read(self, email: str) -> Optional[User]:
        for u in self._users:
            if u.email == email:
                return u
        return None

    def update(self, email: str, new_user: User) -> bool:
        for i, u in enumerate(self._users):
            if u.email == email:
                self._users[i] = new_user
                return True
        return False

    def delete(self, email: str) -> bool:
        for i, u in enumerate(self._users):
            if u.email == email:
                del self._users[i]
                return True
        return False

    def list_all(self) -> List[User]:
        return list(self._users)
