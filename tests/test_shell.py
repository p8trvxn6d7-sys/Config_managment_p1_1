import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from shell import execute, parse_line


def test_parse_line():
    command, args = parse_line("cd src/tests")
    assert command == "cd"
    assert args == ["src/tests"]


def test_parse_line_empty():
    command, args = parse_line("   ")
    assert command == ""
    assert args == []


def test_execute_ls():
    result = execute("ls", ["-la"])
    assert "ls" in result
    assert "-la" in result


def test_execute_cd():
    result = execute("cd", ["Documents"])
    assert "cd" in result
    assert "Documents" in result


def test_execute_unknown():
    result = execute("blabla", [])
    assert "не найдена" in result


if __name__ == "__main__":
    for test in (
        test_parse_line,
        test_parse_line_empty,
        test_execute_ls,
        test_execute_cd,
        test_execute_unknown,
    ):
        test()
        print("OK:", test.__name__)
    print("Все тесты пройдены.")
