
from datetime import datetime
from urllib.parse import quote_plus
import webbrowser


def get_greeting() -> str:
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning!"

    if 12 <= hour < 18:
        return "Good afternoon!"

    return "Good evening!"


def get_current_time() -> str:
    return datetime.now().strftime("It is %I:%M %p.")




def get_current_date() -> str:
    date_text = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {date_text}."




def search_web(query: str) -> str:
    query = query.strip()

    if not query:
        return "Please tell me what you want to search for."

    url = "https://www.google.com/search?q=" + quote_plus(query)
    opened = webbrowser.open(url)

    if opened:
        return f"Searching the web for {query}."

    return "I couldn't open the browser. Please check your browser settings."
