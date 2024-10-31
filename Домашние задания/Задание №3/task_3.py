import argparse
import yaml
from peco.peco import *

# Глобальный словарь для хранения значений переменных
variables = {}

# Класс для обработки синтаксических ошибок с указанием места ошибки
class ParserError(Exception):
    def __init__(self, message, line=None, position=None):
        self.message = message
        self.line = line
        self.position = position
        super().__init__(self.get_error_message())

    def get_error_message(self):
        location = f" at line {self.line}, position {self.position}" if self.line and self.position else ""
        return f"Syntax Error{location}: {self.message}"

# Обработка определения константных переменных с детализированной ошибкой
def assign_const(n_v):
    variables[n_v[0]] = n_v[1]
    return n_v  # Возвращаем значение, чтобы оно добавилось в стек

mkAssign = to(assign_const)

# Обработка объектов (словарей)
def mk_item(pairs):
    try:
        # Фильтруем только пары (ключ, значение), исключая None и булевые значения
        valid_pairs = [(k, v) for item in pairs if item and isinstance(item, tuple) and len(item) == 2 
                       for k, v in [item] if isinstance(k, str) and v is not None]
        return valid_pairs
    except Exception as e:
        raise ParserError(f"Error in dictionary item definition: {e}")

# Обработка цифр, массивов и объектов (словарей)
mknum = to(lambda n: float(n))
mkarr = to(lambda a: list(a))
mkobj = to(lambda o: dict(mk_item(o)))  # Преобразуем в словарь только валидные пары

# Обработка константных выражений
def constRes(expr):
    try:
        oper      = expr[0]
        var_name  = expr[1]
        num       = expr[2]
        
        # Получение значения переменной из глобального словаря
        if var_name not in variables:
            raise NameError(f"Variable '{var_name}' is not defined.")
        
        var = variables[var_name]
        
        # Выполняем операцию над переменной
        if   oper == "mod": result = var % num
        elif oper == "min": result = min(var, num)
        else:               result = eval(f"{var}{oper}{num}")
        
        # Сохраняем изменённое значение обратно в словарь переменных
        variables[var_name] = result
        
        # Возвращаем обновлённую пару (имя, значение) для стека
        return (var_name, result)
    except Exception as e:
        raise ParserError("Error in constant expression '@{" + f"{oper} {var_name} {num}" + "}': " + str(e))

mkConstRes = to(constRes)

# Обработка лишних пробелов, включая обработку комментариев
ws = many(eat(r'\s+|#.*|{-[^}]+-}'))

# Сканирование кода, повышающее производительность вычислений
scan = lambda f: memo(seq(ws, f))

# Пропуск того, что передано как аргумент (регулярка)
skip = lambda c: scan(eat(c))

# Кладёт распознанное в стек с помощью cite(args*)
tok = lambda c: scan(cite(eat(c)))

# Обработка чисел и имён соответственно
num = seq(tok(r'[-+]?\d+'), mknum)
name = tok(r'[_A-Z][_a-zA-Z0-9]*')

# Рекурсивная пересылка (заглушки)
val = lambda s: val(s)
item = lambda s: item(s)

# Правило для массивов
array = seq(skip(r'\(list'), group(many(val)), skip(r'\)'), mkarr)

# Правило для определения константных переменных
consts = seq(group(seq(skip(r'var'), name, skip(r':='), val, skip(r';'))), mkAssign)

# Правило для объектов (словарей)
obj = seq(skip(r'\['), group(many(seq(item, skip(r',')))), skip(r'\]'), mkobj)

# Правило для элементов словаря
item = group(seq(name, skip(r'=>'), alt(val, obj)))

# Правило обработки значений (варианты типов)
val = alt(num, array, obj)

# Правило обработки операций для константных выражений
operation = tok(r'\+|\-|\*|min|mod')

# Правило обработки константных выражений
constExpr = seq(skip(r'@{'), group(seq(operation, name, num)), skip(r'}'), mkConstRes)

# Точка входа в программу обработки
main = seq(group(seq(many(consts), many(constExpr))), ws, mkobj)

# Функция для загрузки и парсинга конфигурационного файла
def parse_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            src = f.read()
        s = parse(src, main)
        if s.ok:
            result_dict = dict(s.stack[0]) if isinstance(s.stack, tuple) else s.stack
            yaml_output = yaml.dump(result_dict, default_flow_style=False, allow_unicode=True)
            print(yaml_output)
        else:
            print("Parsing failed.")
            if hasattr(s, 'error_position'):
                raise ParserError("Unexpected syntax structure", line=s.error_position.line, position=s.error_position.col)
    except ParserError as e:
        print(e)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while parsing: {e}")

# Основная программа
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a configuration file in a custom language.")
    parser.add_argument("file", help="Path to the configuration file to parse")
    args = parser.parse_args()
    
    # Запуск парсинга файла
    parse_file(args.file)
