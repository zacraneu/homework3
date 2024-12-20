# Конвертирование XML в конфигурационный язык

Этот инструмент позволяет преобразовать XML-файлы в конфигурационный язык с использованием Python. Он обрабатывает синтаксис учебного конфигурационного языка и преобразует данные в соответствующий формат. Входной текст принимается в формате XML, а результат выводится в стандартный вывод.

## Описание

Инструмент парсит XML-данные, содержащие описания переменных и операций, и конвертирует их в формат конфигурационного языка, который поддерживает:

- Объявление констант.
- Операции с числами: сложение, вычитание, извлечение квадратного корня и вычисление остатка от деления.
- Вложенные операции и переменные.

Пример команды:
```bash
python config_language.py input.xml
```
где input.xml — это путь к вашему XML-файлу.
Пример команды тестов:
```bash
python test_config_language.py
```
![Результат тестирования](photo/Снимок%20экрана%202024-12-16%20211809.png)

Результат работы программы:

![Результат работы](photo/Снимок%20экрана%202024-12-19%20215537.png)
