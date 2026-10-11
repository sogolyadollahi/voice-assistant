
from dataclasses import dataclass, field
import re


@dataclass(frozen=True)
class ParsedCommand:
    intent: str
    entities: dict[str, str] = field(default_factory=dict)
    confidence: float = 0.0


def normalize_text(text: str) -> str:
    """Normalize casing and whitespace."""
    return " ".join(text.lower().strip().split())


def parse_intent(text: str) -> ParsedCommand:
    """Recognize a supported intent and extract its parameters."""
    normalized = normalize_text(text)

    if not normalized:
        return ParsedCommand("unknown", confidence=0.0)

    # Exit intent
    if normalized in {
        "exit",
        "quit",
        "stop assistant",
        "goodbye",
        "bye",
    }:
        return ParsedCommand("exit", confidence=1.0)

    # Greeting intent
    if re.fullmatch(
        r"(?:hello|hi|hey)(?: there)?[!.]?",
        normalized,
    ):
        return ParsedCommand("greeting", confidence=0.99)

    # Time intent
    time_patterns = [
        r"\bwhat(?:'s| is) the time\b",
        r"\bwhat time is it\b",
        r"\btell me the time\b",
        r"\bcurrent time\b",
    ]

    if any(re.search(pattern, normalized) for pattern in time_patterns):
        return ParsedCommand("time", confidence=0.95)

    # Date intent
    date_patterns = [
        r"\bwhat(?:'s| is) (?:today's|the current) date\b",
        r"\bwhat date is it\b",
        r"\btell me the date\b",
        r"\bwhat day is it\b",
    ]

    if any(re.search(pattern, normalized) for pattern in date_patterns):
        return ParsedCommand("date", confidence=0.95)

    # Search intent with several natural phrasings
    search_patterns = [
        r"^(?:please )?search (?:the web )?for (.+?)[?.!]*$",
        r"^(?:please )?look up (.+?)[?.!]*$",
        r"^(?:please )?google (.+?)[?.!]*$",
        r"^could you search (?:the web )?for (.+?)[?.!]*$",
        r"^can you find information about (.+?)[?.!]*$",
    ]

    for pattern in search_patterns:
        match = re.fullmatch(pattern, normalized)
        if match:
            query = match.group(1).strip()

            if query:
                return ParsedCommand(
                    intent="search",
                    entities={"query": query},
                    confidence=0.90,
                )

    return ParsedCommand("unknown", confidence=0.0)
