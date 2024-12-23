import argparse
import re
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def remove_comments(text):
    """Удаляет многострочные комментарии из текста."""
    return re.sub(r'\{\{!--.*?--\}\}', '', text, flags=re.DOTALL).strip()

def parse_dictionaries(text):
    """Обрабатывает словари и возвращает их в виде списка словарей."""
    dictionaries = []
    pattern = r'begin\s*(.*?)\s*end'
    matches = re.finditer(pattern, text, flags=re.DOTALL)

    for match in matches:
        dictionary_content = match.group(1).strip()
        entries = re.findall(r'([a-zA-Z][_a-zA-Z0-9]*)\s*:=\s*([^;]+);', dictionary_content)
        dictionary = {key: value.strip() for key, value in entries}
        dictionaries.append(dictionary)

        text = text.replace(match.group(0), '', 1)  # Удаляем обработанный словарь

    return dictionaries, text

def parse_constants(text):
    """Обрабатывает объявления констант и вычисляет их значения."""
    constants = {}
    pattern = r'var\s+([a-zA-Z][_a-zA-Z0-9]*)\s*=\s*([^;]+);'
    matches = re.finditer(pattern, text)

    for match in matches:
        name, value = match.groups()
        value = value.strip()
        if value.isdigit():  # Если значение - целое число
            constants[name] = int(value)
        elif re.match(r'^\|.*\|$', value):  # Если значение - выражение
            constants[name] = evaluate_expression(value[1:-1], constants)
        else:
            constants[name] = value  # Оставляем как строку для других случаев

        text = text.replace(match.group(0), '', 1)  # Удаляем обработанную константу

    return constants, text



def evaluate_expression(expression, constants):
    """Вычисляет постфиксное выражение с использованием констант."""
    try:
        stack = []
        tokens = expression.split()

        for token in tokens:
            if token in constants:
                value = constants[token]
                stack.append(value if isinstance(value, int) else int(value))
            elif token.isdigit():
                stack.append(int(token))
            elif token in {'+', '-', '*'}:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
            elif token.startswith('mod('):
                value = int(token[4:-1])
                stack[-1] %= value
            elif token.startswith('abs('):
                stack[-1] = abs(stack[-1])

        return stack[0] if stack else None

    except Exception as e:
        raise ValueError(f"Ошибка вычисления выражения '{expression}': {e}")



def generate_xml(dictionaries, constants):
    """Генерирует XML-документ из словарей и констант."""
    root = ET.Element('root')

    constants_elem = ET.SubElement(root, 'constants')
    for name, value in constants.items():
        const_elem = ET.SubElement(constants_elem, 'constant', name=name)
        const_elem.text = str(value)

    dictionaries_elem = ET.SubElement(root, 'dictionaries')
    for dictionary in dictionaries:
        dict_elem = ET.SubElement(dictionaries_elem, 'dictionary')
        for key, value in dictionary.items():
            entry_elem = ET.SubElement(dict_elem, 'entry', name=key)
            entry_elem.text = value

    # Преобразование дерева в строку
    rough_string = ET.tostring(root, encoding='unicode')
    dom = parseString(rough_string)
    return dom.toprettyxml(indent="    ")


def process_file(input_file):
    """Обрабатывает входной файл и возвращает XML."""
    with open(input_file, 'r') as file:
        text = file.read()

    text = remove_comments(text)
    dictionaries, text = parse_dictionaries(text)
    constants, text = parse_constants(text)

    if text.strip():
        raise SyntaxError(f"Необработанный текст: {text.strip()}")

    return generate_xml(dictionaries, constants)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Преобразование учебного конфигурационного языка в XML.')
    parser.add_argument('--input', required=True, help='Путь к входному файлу')
    args = parser.parse_args()

    try:
        xml_output = process_file(args.input)
        print(xml_output)
    except Exception as e:
        print(f"Ошибка: {e}")
