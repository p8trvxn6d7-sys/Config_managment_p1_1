import argparse
import base64
import csv
import getpass
import socket

VFS_HEADER = ["path", "type", "content"]


def get_prompt():
    user = getpass.getuser()
    host = socket.gethostname().split(".")[0]
    return f"{user}@{host}:~$ "


def parse_line(line):
    parts = line.split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def load_vfs(path):
    vfs = {}
    try:
        with open(path, newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            if header != VFS_HEADER:
                raise ValueError("неверный заголовок")
            for row in reader:
                if len(row) != len(VFS_HEADER):
                    raise ValueError("неверное число колонок")
                node_path, node_type, content = row
                if node_type not in ("dir", "file"):
                    raise ValueError("неверный тип узла")
                data = base64.b64decode(content) if content else b""
                vfs[node_path] = {"type": node_type, "content": data}
    except FileNotFoundError:
        print(f"не удалось найти файл VFS: {path}")
        return None
    except (ValueError, StopIteration):
        print(f"неверный формат файла VFS: {path}")
        return None
    return vfs


def save_vfs(vfs, path):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(VFS_HEADER)
        for node_path, node in vfs.items():
            content = node["content"]
            encoded = ""
            if content:
                encoded = base64.b64encode(content).decode("ascii")
            writer.writerow([node_path, node["type"], encoded])


def execute(command, args, vfs):
    if command == "":
        return None
    if command == "ls":
        return f"ls: аргументы = {args}"
    if command == "cd":
        return f"cd: аргументы = {args}"
    if command == "vfs-save":
        if not args:
            return "vfs-save: укажите путь для сохранения"
        if vfs is None:
            return "vfs-save: VFS не загружена"
        save_vfs(vfs, args[0])
        return f"vfs-save: сохранено в {args[0]}"
    return f"{command}: команда не найдена"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("vfs_path", nargs="?")
    parser.add_argument("script_path", nargs="?")
    args = parser.parse_args()
    return args.vfs_path, args.script_path


def print_debug(vfs_path, script_path):
    print(f"путь к VFS: {vfs_path}")
    print(f"путь к стартовому скрипту: {script_path}")


def run_script(path, vfs):
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

        result = execute(command, args, vfs)
        if result is not None:
            print(result)

    return False


def run_repl(vfs):
    while True:
        try:
            line = input(get_prompt())
        except EOFError:
            print()
            break

        command, args = parse_line(line)

        if command == "exit":
            break

        result = execute(command, args, vfs)
        if result is not None:
            print(result)


def main():
    vfs_path, script_path = parse_args()
    print_debug(vfs_path, script_path)

    vfs = load_vfs(vfs_path) if vfs_path else None

    exited = False
    if script_path:
        exited = run_script(script_path, vfs)

    if not exited:
        run_repl(vfs)


if __name__ == "__main__":
    main()
