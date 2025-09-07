from newsletter import Newsletter
from typing import List


def format_newsletter_for_email(newsletter: Newsletter) -> str:
    return (
        f"Subject: {newsletter.title}\n"
        f"Date: {newsletter.publication_date.strftime('%A, %d %B %Y %H:%M')}\n"
        f"URL: {newsletter.url if hasattr(newsletter, 'url') and newsletter.url else 'N/A'}\n"
        f"\n{newsletter.content}\n"
    )


def format_multiple_newsletters(newsletters: List[Newsletter]) -> str:
    return "\n\n---\n\n".join(format_newsletter_for_email(n) for n in newsletters)
