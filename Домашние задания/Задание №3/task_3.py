import re
import argparse
import yaml

# Регулярные выражения для различных синтаксических элементов
COMMENT_SINGLE_LINE = re.compile(r'#.*')
COMMENT_MULTI_LINE = re.compile(r'{-.*?-}', re.DOTALL)
VAR_DECLARATION = re.compile(r'var\s+([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*(.+);')
CONSTANT_EXPR = re.compile(r'@\{([+\-*\/%])\s+([A-Za-z_][A-Za-z0-9_]*|\d+)\s+(\d+)\}')
LIST_PATTERN = re.compile(r'\(list\s+(.+?)\s*\)')
DICT_PATTERN = re.compile(r'\[\s*([A-Za-z_][A-Za-z0-9_]*\s*=>\s*.+?)\s*\]')
NAME_PATTERN = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')

# Обработка синтаксических ошибок
class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Функция для вычисления выражений на этапе трансляции
def evaluate_expression(op, var1, var2, variables):
    # Преобразуем переменные или оставляем числа
    if var1 in variables:
        var1 = int(variables[var1])  # преобразуем строку в число
    else:
        var1 = int(var1)
    var2 = int(var2)  # второе значение всегда должно быть числом
    
    # Выполняем арифметическую операцию
    if op == '+':
        return var1 + var2
    elif op == '-':
        return var1 - var2
    elif op == '*':
        return var1 * var2
    elif op == 'mod':
        return var1 % var2
    else:
        raise SyntaxError(f"Неизвестная операция '{op}' в константном выражении.")

# Функция для парсинга и обработки входного файла
def parse_input(text):
    # Удаление комментариев
    text = COMMENT_SINGLE_LINE.sub('', text)
    text = COMMENT_MULTI_LINE.sub('', text)
    
    variables = {}
    yaml_data = {}
    
    # Парсинг строк с объявлениями переменных
    for match in VAR_DECLARATION.finditer(text):
        var_name, var_value = match.groups()
        if CONSTANT_EXPR.match(var_value):
            # Обрабатываем выражения с константами
            op, var1, var2 = CONSTANT_EXPR.match(var_value).groups()
            result = evaluate_expression(op, var1, var2, variables)
            variables[var_name] = result
        else:
            # Простое присваивание
            variables[var_name] = int(var_value.strip()) if var_value.strip().isdigit() else var_value.strip()
    
    # Проверка на неправильные конструкции списков
    if not LIST_PATTERN.search(text):
        raise SyntaxError("Ошибка синтаксиса: неверное определение списка. Ожидается конструкция (list ...)")

    # Преобразование списков
    for match in LIST_PATTERN.finditer(text):
        items = match.group(1).split()
        items = [int(item) if item.isdigit() else item for item in items]  # Преобразуем элементы списка в числа
        yaml_data['list'] = items
    
    # Проверка на неправильные конструкции словарей
    if not DICT_PATTERN.search(text):
        raise SyntaxError("Ошибка синтаксиса: неверное определение словаря. Ожидается конструкция [key => value, ...]")

    # Преобразование словарей
    for match in DICT_PATTERN.finditer(text):
        dict_items = {}
        pairs = match.group(1).split(',')
        for pair in pairs:
            if '=>' not in pair:
                raise SyntaxError(f"Ошибка синтаксиса: неверная пара в словаре '{pair}'. Ожидается формат key => value.")
            key, value = pair.split('=>')
            key = key.strip()
            value = value.strip()
            dict_items[key] = int(value) if value.isdigit() else value
        yaml_data['dict'] = dict_items
    
    return yaml_data

# Основная функция
def main():
    parser = argparse.ArgumentParser(description="Конфигурационный парсер в YAML")
    parser.add_argument('input_file', help="Путь к входному файлу конфигурации")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as file:
            input_text = file.read()

        # Парсинг входного текста
        yaml_data = parse_input(input_text)
        
        # Вывод данных в формате YAML
        print(yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True))

    except FileNotFoundError:
        print(f"Ошибка: файл {args.input_file} не найден.")
    except SyntaxError as e:
        print(f"Синтаксическая ошибка: {str(e)}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    main()
