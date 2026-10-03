# Эмулятор командной строки

Вариант 31. Этапы 1-3.

## Что сделано

- REPL с приглашением на основе логина и хоста
- ls и cd как заглушки, печатают переданные аргументы
- exit завершает работу
- неизвестная команда не роняет программу
- параметры командной строки: путь к VFS, путь к стартовому скрипту
- отладочный вывод параметров при старте
- стартовый скрипт выполняется построчно, ошибочные строки пропускаются, на экране виден и ввод, и вывод
- VFS загружается из CSV (путь,тип,содержимое в base64), работает только в памяти
- обработка ошибок загрузки VFS: файл не найден, неверный формат
- vfs-save путь сохраняет текущую VFS обратно в CSV

## Запуск

```
python3 src/shell.py [путь_к_vfs] [путь_к_скрипту]
```

или без параметров:

```
./run.sh
```

## Тесты

```
python3 tests/test_shell.py
```

## OS-скрипты для проверки

```
./scripts/run_no_args.sh
./scripts/run_with_vfs.sh
./scripts/run_with_script.sh
./scripts/run_vfs_minimal.sh
./scripts/run_vfs_files.sh
./scripts/run_vfs_nested.sh
./scripts/run_vfs_missing.sh
./scripts/run_vfs_invalid.sh
```

## Формат CSV для VFS

Три колонки: path,type,content.
type — dir или file.
content — пусто для dir, base64 для file.

```
path,type,content
/,dir,
/docs,dir,
/docs/readme.txt,file,cHJpdmV0IG1pcgo=
```

## Пример

```
$ python3 src/shell.py examples/vfs.csv examples/startup.txt
путь к VFS: examples/vfs.csv
путь к стартовому скрипту: examples/startup.txt
user@host:~$ ls -la /home
ls: аргументы = ['-la', '/home']
user@host:~$ cd Documents
cd: аргументы = ['Documents']
user@host:~$ unknown_command
unknown_command: команда не найдена
user@host:~$ vfs-save output/vfs_saved.csv
vfs-save: сохранено в output/vfs_saved.csv
user@host:~$ exit
```

## Структура

```
.
├── README.md
├── run.sh
├── src/shell.py
├── tests/test_shell.py
├── examples/
│   ├── startup.txt
│   ├── startup_vfs.txt
│   ├── vfs.csv
│   ├── vfs_minimal.csv
│   ├── vfs_files.csv
│   ├── vfs_nested.csv
│   └── vfs_invalid.csv
└── scripts/
    ├── run_no_args.sh
    ├── run_with_vfs.sh
    ├── run_with_script.sh
    ├── run_vfs_minimal.sh
    ├── run_vfs_files.sh
    ├── run_vfs_nested.sh
    ├── run_vfs_missing.sh
    └── run_vfs_invalid.sh
```
