# Эмулятор командной строки

Вариант 31. Этапы 1-2.

## Что сделано

- REPL с приглашением на основе логина и хоста
- ls и cd как заглушки, печатают переданные аргументы
- exit завершает работу
- неизвестная команда не роняет программу
- параметры командной строки: путь к VFS, путь к стартовому скрипту
- отладочный вывод параметров при старте
- стартовый скрипт выполняется построчно, ошибочные строки пропускаются, на экране виден и ввод, и вывод

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

## OS-скрипты для проверки параметров

```
./scripts/run_no_args.sh
./scripts/run_with_vfs.sh
./scripts/run_with_script.sh
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
user@host:~$ exit
```

## Структура

```
.
├── README.md
├── run.sh
├── src/shell.py
├── tests/test_shell.py
├── examples/startup.txt
└── scripts/
    ├── run_no_args.sh
    ├── run_with_vfs.sh
    └── run_with_script.sh
```
