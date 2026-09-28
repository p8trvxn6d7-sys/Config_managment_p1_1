# Эмулятор командной строки

Вариант 31. Этап 1.

## Что сделано

- REPL с приглашением на основе логина и хоста
- ls и cd как заглушки, печатают переданные аргументы
- exit завершает работу
- неизвестная команда не роняет программу

## Запуск

```
./run.sh
```

## Тесты

```
python3 tests/test_shell.py
```

## Пример

```
user@host:~$ ls -la /home
ls: аргументы = ['-la', '/home']
user@host:~$ cd ..
cd: аргументы = ['..']
user@host:~$ blabla
blabla: команда не найдена
user@host:~$ exit
```

## Структура

```
.
├── README.md
├── run.sh
├── src/shell.py
└── tests/test_shell.py
```
