
from unittest.mock import patch

from commands import (
    get_current_date,
    get_current_time,
    search_web,
)
from intent_parser import ParsedCommand
from voice_assistant import execute_command


def test_time_format():
    with patch("commands.datetime") as mocked_datetime:
        mocked_datetime.now.return_value.strftime.return_value = "10:30 AM"

        assert get_current_time() == "10:30 AM"


def test_date_format():
    with patch("commands.datetime") as mocked_datetime:
        mocked_datetime.now.return_value.strftime.return_value = (
            "Saturday, October 10, 2026"
        )

        assert get_current_date() == (
            "Today is Saturday, October 10, 2026."
        )



def test_search_opens_browser():
    with patch(
        "commands.webbrowser.open",
        return_value=True,
    ) as mocked_open:
        response = search_web("Python decorators")

    assert response == "Searching the web for Python decorators."
    assert "Python+decorators" in mocked_open.call_args.args[0]


def test_empty_search_does_not_open_browser():
    with patch("commands.webbrowser.open") as mocked_open:
        response = search_web("   ")

    assert response == "Please tell me what you want to search for."
    mocked_open.assert_not_called()


def test_execute_unknown_command():
    response = execute_command(ParsedCommand("unknown"))

    assert "didn't understand" in response


def test_execute_search_command():
    with patch(
        "voice_assistant.search_web",
        return_value="Searching the web for Python.",
    ) as mocked_search:
        response = execute_command(
            ParsedCommand(
                intent="search",
                entities={"query": "Python"},
            )
        )

    assert response == "Searching the web for Python."
    mocked_search.assert_called_once_with("Python")


def test_execute_exit_command():
    assert execute_command(ParsedCommand("exit")) == "Goodbye!"
