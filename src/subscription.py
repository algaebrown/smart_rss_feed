from dataclasses import dataclass
from datetime import datetime
from src.user import User
from src.newsletter import Newsletter

@dataclass
class Subscription:
    user: User
    newsletter: Newsletter
    subscribed_at: datetime
