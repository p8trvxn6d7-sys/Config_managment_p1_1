import getpass
import socket
import sys


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


def parse_args():
    vfs_path = sys.argv[1] if len(sys.argv) > 1 else None
    script_path = sys.argv[2] if len(sys.argv) > 2 else None
    return vfs_path, script_path


def print_debug(vfs_path, script_path):
    print(f"путь к VFS: {vfs_path}")
    print(f"путь к стартовому скрипту: {script_path}")


def run_script(path):
    try:
        with open(path, encoding="utf-8") as script_file:
            lines = script_file.readlines()
    except OSError:
        print(f"не удалось открыть файл скрипта: {path}")
        return False

    for line in lines:
        line = line.rstrip("\n")
        print(get_prompt() + line)

        command, args = parse_line(line)
        if command == "exit":
            return True

        result = execute(command, args)
        if result is not None:
            print(result)

    return False


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


def main():
    vfs_path, script_path = parse_args()
    print_debug(vfs_path, script_path)

    exited = False
    if script_path:
        exited = run_script(script_path)

    if not exited:
        run_repl()


if __name__ == "__main__":
    main()
