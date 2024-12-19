import xml.etree.ElementTree as ET
import math
import sys
import argparse

# Словарь для хранения переменных
variables = {}

# Функция для парсинга XML
def parse_xml(input_xml):
    try:
        tree = ET.ElementTree(ET.fromstring(input_xml))
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        sys.exit(1)

# Функция для вычисления выражений
def evaluate_expression(expr):
    try:
        # Преобразуем операнды в их значения, если это переменные
        expr = [str(variables.get(e, e)) for e in expr]
        
        # Если операнд является числом или строкой с числом, пытаемся преобразовать его
        def parse_operand(operand):
            try:
                operand = operand.replace(";", "").strip()
                return int(operand)
            except ValueError:
                return operand  # возвращаем переменную, если это не число
        
        expr = [parse_operand(e) for e in expr]
        
        if expr[0] == '+':
            return int(expr[1]) + int(expr[2])
        elif expr[0] == '-':
            return int(expr[1]) - int(expr[2])
        elif expr[0] == 'sqrt':
            return math.sqrt(int(expr[1]))
        elif expr[0] == 'mod':
            return int(expr[1]) % int(expr[2])
        else:
            raise ValueError(f"Неизвестная операция: {expr[0]}")
    except Exception as e:
        print(f"Ошибка вычисления выражения: {e}")
        sys.exit(1)

# Функция для обработки значения (число или вложенный элемент)
def process_value(value_element):
    # Если элемент - это операция, нужно обработать его отдельно
    if value_element.tag == 'operation':
        return process_element(value_element)
    
    # Возвращаем пустую строку, если нет текста или вложенных элементов
    if len(value_element) == 0:
        return value_element.text.strip() if value_element.text else ""
    else:
        return '\n'.join(process_element(child) for child in value_element)

# Функция для обработки каждого элемента XML
def process_element(element):
    output = []
    
    # Обработка тега <define>
    if element.tag == 'define':
        if 'name' not in element.attrib or 'value' not in element.attrib:
            print(f"Ошибка: отсутствует атрибут 'name' или 'value' в элементе <define>")
            sys.exit(1)
        name = element.attrib['name']
        value = element.attrib['value']
        
        # Если значение не является числом, пробуем подставить как переменную
        if value.isdigit():
            value = int(value)
        elif value in variables:
            value = variables[value]
        else:
            print(f"Ошибка: значение переменной {value} не найдено.")
            sys.exit(1)
        
        variables[name] = value
        output.append(f"{name} = {value};")

    # Обработка тега <operation>
    elif element.tag == 'operation':
        if 'operation' not in element.attrib:
            print(f"Ошибка: отсутствует атрибут 'operation' в элементе <operation>")
            sys.exit(1)

        operation = element.attrib['operation']
        
        # Собираем операнды, включая вложенные операции
        operands = []
        for child in element:
            operand = process_value(child)
            if operand:  # Добавляем только непустые операнды
                operands.append(operand)

        if len(operands) < 2:
            print(f"Ошибка: операция должна содержать хотя бы два операнда в элементе <operation>")
            sys.exit(1)

        result = evaluate_expression([operation] + operands)
        output.append(f"{result};")

    # Обработка тега <value>
    elif element.tag == 'value':
        value = element.text.strip() if element.text else ""
        if value:
            output.append(value)

    # Если элемент содержит вложенные элементы, обрабатываем их
    elif len(element) > 0:
        return process_value(element)

    # Возвращаем результат
    return '\n'.join(output)

# Главная функция
def main():
    parser = argparse.ArgumentParser(description="Конвертирование XML в конфигурационный язык")
    parser.add_argument('input_file', type=argparse.FileType('r'), help="XML файл для преобразования")
    args = parser.parse_args()

    input_xml = args.input_file.read()
    root = parse_xml(input_xml)
    output = process_element(root)

    # Форматируем вывод, добавляем скобки, заменяем : на ; и добавляем ; после последнего значения
    output_str = output.strip()
    if output_str and not output_str.endswith(';'):
        output_str += ';'  # Добавляем ; в конце, если его нет

    # Добавляем скобки вокруг результата
    print(f"{{\n{output_str}\n}}")

if __name__ == "__main__":
    main()
