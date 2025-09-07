from typing import List, Optional
from src.subscription import Subscription


class SubscriptionStore:
    def __init__(self):
        self._subscriptions: List[Subscription] = []

    def create(self, subscription: Subscription) -> None:
        self._subscriptions.append(subscription)

    def read(self, user_email: str, newsletter_title: str) -> Optional[Subscription]:
        for s in self._subscriptions:
            if s.user.email == user_email and s.newsletter.title == newsletter_title:
                return s
        return None

    def update(
        self, user_email: str, newsletter_title: str, new_subscription: Subscription
    ) -> bool:
        for i, s in enumerate(self._subscriptions):
            if s.user.email == user_email and s.newsletter.title == newsletter_title:
                self._subscriptions[i] = new_subscription
                return True
        return False

    def delete(self, user_email: str, newsletter_title: str) -> bool:
        for i, s in enumerate(self._subscriptions):
            if s.user.email == user_email and s.newsletter.title == newsletter_title:
                del self._subscriptions[i]
                return True
        return False

    def list_all(self) -> List[Subscription]:
        return list(self._subscriptions)
