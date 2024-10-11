import re
import sys
import yaml

# Исключение для синтаксических ошибок
class ConfigSyntaxError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Функция для вычисления константных выражений
def evaluate_expression(op, var1, var2, variables):
    var1 = variables.get(var1, var1)  # Подстановка переменной или числа
    var2 = variables.get(var2, var2)  # Подстановка переменной или числа

    try:
        var1 = int(var1)
    except ValueError:
        raise ConfigSyntaxError(f"Ошибка: переменная '{var1}' должна быть числом.")

    try:
        var2 = int(var2)
    except ValueError:
        raise ConfigSyntaxError(f"Ошибка: переменная '{var2}' должна быть числом.")

    if op == '+':
        return var1 + var2
    elif op == '-':
        return var1 - var2
    elif op == '*':
        return var1 * var2
    elif op == 'mod':
        return var1 % var2
    elif op == 'min':
        return min(var1, var2)
    else:
        raise ConfigSyntaxError(f"Неизвестная операция '{op}'")

# Удаление комментариев
def remove_comments(text):
    text = re.sub(r'#.*', '', text)  # Однострочные комментарии
    text = re.sub(r'\{-.*?-\}', '', text, flags=re.DOTALL)  # Многострочные комментарии
    return text

# Парсинг константных выражений
def parse_expression(expr, variables):
    tokens = expr.strip().split()
    if len(tokens) != 3:
        raise ConfigSyntaxError("Ошибка синтаксиса: неверное выражение")
    op, var1, var2 = tokens
    return evaluate_expression(op, var1, var2, variables)

# Парсинг значений (число, переменная или выражение)
def parse_value(value, variables):
    value = value.strip()
    if value.isdigit():
        return int(value)
    elif value.startswith('@{') and value.endswith('}'):
        return parse_expression(value[2:-1], variables)
    elif value in variables:
        return variables[value]
    else:
        raise ConfigSyntaxError(f"Неизвестное значение: {value}")

# Парсинг словарей
def parse_dict(text, variables):
    # Удаление внешних скобок
    content = text[1:-1].strip()
    if not content:
        return {}
    
    # Регулярное выражение для захвата ключей и значений
    dict_items = re.findall(r'\s*([_A-Za-z][_A-Za-z0-9]*)\s*=>\s*(@\{.*?\}|\d+|[_A-Za-z][_A-Za-z0-9]*)\s*(?:,|$)', content)
    if not dict_items:
        raise ConfigSyntaxError(f"Ошибка синтаксиса: неверный формат словаря '{text}'")
    
    result = {}
    for key, value in dict_items:
        result[key] = parse_value(value.strip(), variables)
    return result

# Парсинг списков
def parse_list(text, variables):
    # Удаление внешних скобок и ключевого слова 'list'
    content = text[5:-1].strip()
    if not content:
        return []
    
    # Использование регулярных выражений для захвата элементов списка, включая выражения
    items = re.findall(r'@{.*?}|\S+', content)
    return [parse_value(item, variables) for item in items]

# Функция для парсинга кода входного файла
def parse_input(input_text):
    input_text = remove_comments(input_text)
    lines = input_text.splitlines()
    variables = {}
    result = {}

    for line in lines:
        line = line.strip()
        
        if not line:
            continue

        if line.startswith("var"):
            match = re.match(r"var\s+([_A-Za-z][_A-Za-z0-9]*)\s*:=\s*(.*);", line)
            if not match:
                raise ConfigSyntaxError("Ошибка синтаксиса: неверное объявление переменной")
            var_name, var_value = match.groups()
            if not var_value.strip():
                raise ConfigSyntaxError("Ошибка синтаксиса: неверное объявление переменной")
            var_value = parse_value(var_value, variables)
            variables[var_name] = var_value
        elif line.startswith('[') and line.endswith(']'):
            result['dict'] = parse_dict(line, variables)
        elif line.startswith('(list') and line.endswith(')'):
            result['list'] = parse_list(line, variables)
        else:
            raise ConfigSyntaxError(f"Ошибка синтаксиса: неизвестная строка '{line}'")

    return result

# Основная функция программы
def main():
    if len(sys.argv) != 2:
        print("Использование: python task_3.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
        sys.exit(1)

    try:
        result = parse_input(input_text)
        yaml_output = yaml.dump(result, allow_unicode=True, default_flow_style=False)
        print(yaml_output)
    except ConfigSyntaxError as e:
        print(f"Ошибка синтаксиса: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
