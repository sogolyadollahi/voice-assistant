
import pytest

from intent_parser import normalize_text, parse_intent


@pytest.mark.parametrize(
    "text",
    ["Hello", "hello!", "Hey there", "HI"],
)
def test_greetings(text):
    assert parse_intent(text).intent == "greeting"


@pytest.mark.parametrize(
    "text",
    [
        "What time is it?",
        "What's the time?",
        "Tell me the time",
        "What is the current time?",
    ],
)
def test_time_intent(text):
    assert parse_intent(text).intent == "time"


@pytest.mark.parametrize(
    "text",
    [
        "What's today's date?",
        "What is the current date?",
        "What date is it?",
        "What day is it?",
    ],
)
def test_date_intent(text):
    assert parse_intent(text).intent == "date"


@pytest.mark.parametrize(
    ("text", "expected_query"),
    [
        ("Search for Python decorators", "python decorators"),
        (
            "Could you search the web for FastAPI testing?",
            "fastapi testing",
        ),
        ("Look up async programming", "async programming"),
        ("Google dependency injection", "dependency injection"),
        (
            "Can you find information about REST APIs?",
            "rest apis",
        ),
    ],
)
def test_search_intent_extracts_query(text, expected_query):
    command = parse_intent(text)

    assert command.intent == "search"
    assert command.entities["query"] == expected_query


def test_unknown_intent():
    assert parse_intent("Tell me something interesting").intent == "unknown"


def test_empty_input():
    command = parse_intent("   ")

    assert command.intent == "unknown"
    assert command.confidence == 0.0


def test_normalization():
    assert normalize_text("  HELLO    THERE  ") == "hello there"


@pytest.mark.parametrize(
    "text",
    ["Goodbye", "bye", "quit", "stop assistant"],
)
def test_exit_intent(text):
    assert parse_intent(text).intent == "exit"
