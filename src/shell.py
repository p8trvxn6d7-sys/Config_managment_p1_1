import argparse
import base64
import csv
import getpass
import socket

VFS_HEADER = ["path", "type", "content"]


def get_prompt(cwd):
    user = getpass.getuser()
    host = socket.gethostname().split(".")[0]
    location = cwd if cwd else "~"
    return f"{user}@{host}:{location}$ "


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


def resolve_path(cwd, arg):
    if arg in ("", "."):
        base = cwd
    elif arg.startswith("/"):
        base = arg
    else:
        base = cwd.rstrip("/") + "/" + arg

    parts = []
    for part in base.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)

    if not parts:
        return "/"
    return "/" + "/".join(parts)


def vfs_children(vfs, dir_path):
    children = []
    for node_path in vfs:
        if node_path == dir_path:
            continue
        parent = node_path.rsplit("/", 1)[0]
        if parent == "":
            parent = "/"
        if parent == dir_path:
            children.append(node_path)
    return sorted(children)


def ls_command(vfs, cwd, args):
    if vfs is None:
        return "ls: VFS не загружена"

    target_path = resolve_path(cwd, args[0]) if args else cwd
    if target_path not in vfs:
        return f"ls: путь не найден: {target_path}"

    node = vfs[target_path]
    if node["type"] == "file":
        return target_path.rsplit("/", 1)[-1]

    children = vfs_children(vfs, target_path)
    names = [child.rsplit("/", 1)[-1] for child in children]
    return " ".join(names)


def cd_command(vfs, state, args):
    if vfs is None:
        return "cd: VFS не загружена"

    target_path = resolve_path(state["cwd"], args[0]) if args else "/"
    if target_path not in vfs:
        return f"cd: путь не найден: {target_path}"

    node = vfs[target_path]
    if node["type"] != "dir":
        return f"cd: не каталог: {target_path}"

    state["cwd"] = target_path
    return None


def rev_command(vfs, cwd, args):
    if vfs is None:
        return "rev: VFS не загружена"
    if not args:
        return "rev: укажите путь к файлу"

    target_path = resolve_path(cwd, args[0])
    if target_path not in vfs:
        return f"rev: путь не найден: {target_path}"

    node = vfs[target_path]
    if node["type"] != "file":
        return f"rev: не файл: {target_path}"

    text = node["content"].decode("utf-8", errors="replace")
    lines = text.splitlines()
    reversed_lines = [line[::-1] for line in lines]
    return "\n".join(reversed_lines)


def tree_lines(vfs, path, prefix):
    children = vfs_children(vfs, path)
    lines = []
    for index, child_path in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        name = child_path.rsplit("/", 1)[-1]
        lines.append(prefix + connector + name)
        if vfs[child_path]["type"] == "dir":
            extension = "    " if is_last else "│   "
            lines.extend(tree_lines(vfs, child_path, prefix + extension))
    return lines


def tree_command(vfs, cwd, args):
    if vfs is None:
        return "tree: VFS не загружена"

    target_path = resolve_path(cwd, args[0]) if args else cwd
    if target_path not in vfs:
        return f"tree: путь не найден: {target_path}"

    lines = [target_path]
    lines.extend(tree_lines(vfs, target_path, ""))
    return "\n".join(lines)


def vfs_save_command(vfs, args):
    if not args:
        return "vfs-save: укажите путь для сохранения"
    if vfs is None:
        return "vfs-save: VFS не загружена"
    save_vfs(vfs, args[0])
    return f"vfs-save: сохранено в {args[0]}"


def touch_command(vfs, cwd, args):
    if vfs is None:
        return "touch: VFS не загружена"
    if not args:
        return "touch: укажите имя файла"

    target_path = resolve_path(cwd, args[0])
    if target_path in vfs:
        return None

    parent = target_path.rsplit("/", 1)[0]
    if parent == "":
        parent = "/"
    if parent not in vfs:
        return f"touch: каталог не найден: {parent}"
    if vfs[parent]["type"] != "dir":
        return f"touch: не каталог: {parent}"

    vfs[target_path] = {"type": "file", "content": b""}
    return None


def help_command():
    lines = [
        "ls [путь]        показать содержимое каталога или имя файла",
        "cd [путь]        перейти в каталог",
        "rev путь         вывести файл с развёрнутыми строками",
        "tree [путь]      показать дерево каталогов",
        "touch путь       создать пустой файл",
        "vfs-save путь    сохранить VFS в CSV-файл",
        "help             показать эту справку",
        "exit             выйти из эмулятора",
    ]
    return "\n".join(lines)


def execute(command, args, vfs, state):
    if command == "":
        return None
    if command == "ls":
        return ls_command(vfs, state["cwd"], args)
    if command == "cd":
        return cd_command(vfs, state, args)
    if command == "rev":
        return rev_command(vfs, state["cwd"], args)
    if command == "tree":
        return tree_command(vfs, state["cwd"], args)
    if command == "touch":
        return touch_command(vfs, state["cwd"], args)
    if command == "vfs-save":
        return vfs_save_command(vfs, args)
    if command == "help":
        return help_command()
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


def run_script(path, vfs, state):
    try:
        with open(path, encoding="utf-8") as script_file:
            lines = script_file.readlines()
    except OSError:
        print(f"не удалось открыть файл скрипта: {path}")
        return False

    for line in lines:
        line = line.rstrip("\n")
        print(get_prompt(state["cwd"]) + line)

        command, args = parse_line(line)
        if command == "exit":
            return True

        result = execute(command, args, vfs, state)
        if result is not None:
            print(result)

    return False


def run_repl(vfs, state):
    while True:
        try:
            line = input(get_prompt(state["cwd"]))
        except EOFError:
            print()
            break

        command, args = parse_line(line)

        if command == "exit":
            break

        result = execute(command, args, vfs, state)
        if result is not None:
            print(result)


def main():
    vfs_path, script_path = parse_args()
    print_debug(vfs_path, script_path)

    vfs = load_vfs(vfs_path) if vfs_path else None
    state = {"cwd": "/"}

    exited = False
    if script_path:
        exited = run_script(script_path, vfs, state)

    if not exited:
        run_repl(vfs, state)


if __name__ == "__main__":
    main()
