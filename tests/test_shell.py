import base64
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from shell import execute, load_vfs, parse_line, save_vfs


def test_parse_line():
    command, args = parse_line("cd src/tests")
    assert command == "cd"
    assert args == ["src/tests"]


def test_parse_line_empty():
    command, args = parse_line("   ")
    assert command == ""
    assert args == []


def test_execute_ls():
    result = execute("ls", ["-la"], None)
    assert "ls" in result
    assert "-la" in result


def test_execute_cd():
    result = execute("cd", ["Documents"], None)
    assert "cd" in result
    assert "Documents" in result


def test_execute_unknown():
    result = execute("blabla", [], None)
    assert "не найдена" in result


def test_load_vfs_missing_file():
    vfs = load_vfs("/tmp/does_not_exist_vfs.csv")
    assert vfs is None


def make_temp_csv():
    descriptor, path = tempfile.mkstemp(suffix=".csv")
    os.close(descriptor)
    return path


def test_load_vfs_bad_format():
    tmp_path = make_temp_csv()
    with open(tmp_path, "w", encoding="utf-8") as tmp_file:
        tmp_file.write("not,a,valid,vfs\n")
    vfs = load_vfs(tmp_path)
    os.remove(tmp_path)
    assert vfs is None


def test_load_vfs_valid():
    content = base64.b64encode(b"hello").decode("ascii")
    tmp_path = make_temp_csv()
    with open(tmp_path, "w", encoding="utf-8") as tmp_file:
        tmp_file.write("path,type,content\n")
        tmp_file.write("/,dir,\n")
        tmp_file.write(f"/file.txt,file,{content}\n")
    vfs = load_vfs(tmp_path)
    os.remove(tmp_path)
    assert vfs["/"]["type"] == "dir"
    assert vfs["/file.txt"]["content"] == b"hello"


def test_vfs_save_roundtrip():
    vfs = {
        "/": {"type": "dir", "content": b""},
        "/docs": {"type": "dir", "content": b""},
        "/docs/readme.txt": {"type": "file", "content": b"hi there"},
    }
    tmp_path = make_temp_csv()
    save_vfs(vfs, tmp_path)
    loaded = load_vfs(tmp_path)
    os.remove(tmp_path)
    assert loaded == vfs


def test_execute_vfs_save_no_vfs():
    result = execute("vfs-save", ["/tmp/out.csv"], None)
    assert "не загружена" in result


def test_execute_vfs_save_no_path():
    result = execute("vfs-save", [], {})
    assert "укажите путь" in result


if __name__ == "__main__":
    for test in (
        test_parse_line,
        test_parse_line_empty,
        test_execute_ls,
        test_execute_cd,
        test_execute_unknown,
        test_load_vfs_missing_file,
        test_load_vfs_bad_format,
        test_load_vfs_valid,
        test_vfs_save_roundtrip,
        test_execute_vfs_save_no_vfs,
        test_execute_vfs_save_no_path,
    ):
        test()
        print("OK:", test.__name__)
    print("Все тесты пройдены.")
