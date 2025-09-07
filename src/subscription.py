from dataclasses import dataclass
from datetime import datetime
from user import User
from newsletter import Newsletter


@dataclass
class Subscription:
    user: User
    newsletter: Newsletter
    subscribed_at: datetime
