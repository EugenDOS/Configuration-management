from peco.peco import *

# Глобальный словарь для хранения значений переменных
variables = {}

# Обработка определения константных переменных
def assign_const(n_v):
    variables[n_v[0]] = n_v[1]
    return n_v  # Возвращаем значение, чтобы оно добавилось в стек

mkAssign = to(assign_const)

# Обработка объектов (словарей)
def mk_item(pairs):
    # Фильтруем только пары (ключ, значение), исключая None и булевые значения
    valid_pairs = [(k, v) for item in pairs if item and isinstance(item, tuple) and len(item) == 2 
                   for k, v in [item] if isinstance(k, str) and v is not None]
    return valid_pairs

# Обработка цифр, массивов и объектов (словарей)
mknum = to(lambda n: float(n))
mkarr = to(lambda a: list(a))
mkobj = to(lambda o: dict(mk_item(o)))  # Преобразуем в словарь только валидные пары

# Обработка константных выражений
def constRes(expr):
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

# Тестирование
def test():
    src = '''
    # comment
    {- что-то -}
    var Num := 666;
    var List := (list 1 2 3 4 5);
    var Vm := [
        Ip => (list 192 168 44 44),
        Memory => 1024,
        Test => [
            UnderTest => 20,
        ],
    ];
    @{mod Num 1}
    '''
    s = parse(src, main)
    print(s.ok)
    print(s.stack)

test()
