# Эмулятор командной строки

Вариант 31. Этапы 1-5.

## Что сделано

- REPL с приглашением на основе логина, хоста и текущей директории VFS
- параметры командной строки: путь к VFS, путь к стартовому скрипту
- отладочный вывод параметров при старте
- стартовый скрипт выполняется построчно, ошибочные строки пропускаются
- VFS загружается из CSV (путь,тип,содержимое в base64), работает только в памяти
- обработка ошибок загрузки VFS: файл не найден, неверный формат
- vfs-save путь сохраняет текущую VFS обратно в CSV
- ls выводит содержимое каталога или имя файла, с аргументом или без
- cd меняет текущую директорию, поддерживает относительные пути, "." и ".."
- rev разворачивает текстовый файл из VFS построчно
- tree выводит дерево каталогов из текущей директории или с указанного пути
- touch путь создает пустой файл в VFS, если каталог существует
- help выводит список команд с описанием
- неизвестная команда и несуществующий путь не роняют программу

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
./scripts/run_stage4_demo.sh
./scripts/run_stage5_demo.sh
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
$ python3 src/shell.py examples/vfs.csv examples/startup_stage5.txt
путь к VFS: examples/vfs.csv
путь к стартовому скрипту: examples/startup_stage5.txt
user@host:/$ ls
docs readme.txt
user@host:/$ cd docs
user@host:/docs$ touch notes.txt
user@host:/docs$ ls
notes.txt reports
user@host:/docs$ cd ..
user@host:/$ rev readme.txt
rim tevirp
user@host:/$ exit
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
│   ├── startup_stage4.txt
│   ├── startup_stage5.txt
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
    ├── run_vfs_invalid.sh
    ├── run_stage4_demo.sh
    └── run_stage5_demo.sh
```
