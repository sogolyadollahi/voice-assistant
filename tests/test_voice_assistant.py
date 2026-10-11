
from unittest.mock import patch

from intent_parser import ParsedCommand, parse_intent
from voice_assistant import execute_command


def test_greeting_command():
    with patch(
        "voice_assistant.get_greeting",
        return_value="Good morning!",
    ):
        response = execute_command(ParsedCommand("greeting"))

    assert response == "Good morning!"


def test_time_command():
    with patch(
        "voice_assistant.get_current_time",
        return_value="It is 10:30 AM.",
    ):
        response = execute_command(ParsedCommand("time"))

    assert response == "It is 10:30 AM."


def test_date_command():
    with patch(
        "voice_assistant.get_current_date",
        return_value="Today is Monday, January 05, 2026.",
    ):
        response = execute_command(ParsedCommand("date"))

    assert response == "Today is Monday, January 05, 2026."


def test_search_command_passes_query_to_handler():
    with patch(
        "voice_assistant.search_web",
        return_value="Searching the web for Python.",
    ) as mocked_search:
        command = parse_intent("Search for Python")
        response = execute_command(command)

    assert response == "Searching the web for Python."
    mocked_search.assert_called_once_with("python")


def test_unknown_command_returns_fallback():
    response = execute_command(
        ParsedCommand("unknown")
    )

    assert response == "I didn't understand that command. Please try again."


def test_exit_command_returns_goodbye():
    response = execute_command(
        parse_intent("Goodbye")
    )

    assert response == "Goodbye!"


def test_parsed_command_has_default_entities():
    command = parse_intent("Hello")

    assert command.intent == "greeting"
    assert command.entities == {}
