import getpass
import socket


def get_prompt():
    user = getpass.getuser()
    host = socket.gethostname().split(".")[0]
    return f"{user}@{host}:~$ "


def parse_line(line):
    parts = line.split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def execute(command, args):
    if command == "":
        return None
    if command == "ls":
        return f"ls: аргументы = {args}"
    if command == "cd":
        return f"cd: аргументы = {args}"
    return f"{command}: команда не найдена"


def run_repl():
    while True:
        try:
            line = input(get_prompt())
        except EOFError:
            print()
            break

        command, args = parse_line(line)

        if command == "exit":
            break

        result = execute(command, args)
        if result is not None:
            print(result)


if __name__ == "__main__":
    run_repl()
