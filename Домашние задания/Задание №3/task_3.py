from peco.peco import *

# Обработка цифр, массивов и объектов (словарей)
mknum = to(lambda n: float(n))
mkarr = to(lambda a: list(a))
mkobj = to(lambda o: dict(o))

# Обработка лишних пробелов, включая обработку комментриев
ws = many(eat(r'\s+|#.*|{-[^}]+-}'))

# Сканирование кода, повышающее производительность вычислений
scan = lambda f: memo(seq(ws, f))

# Пропуск того, что передано как аргумент (регулярка)
skip = lambda c: scan(eat(c))

# Кладёт распознанное в стек 
# eat(args*) -- распознавание
tok = lambda c: scan(cite(eat(c)))

# Правила распознавания для чисел и имён соответственно
num = seq(tok(r'[-+]?\d+'), mknum)
name = tok(r'[_A-Z][_a-zA-Z0-9]*')

# Рекурсивная пересылка для обработки переменных
val = lambda s: val(s)

# Правило для массивов
array = seq(skip(r'\(list'), group(many(val)), skip(r'\)'), mkarr)

# Правило для элементов словаря
item = group(seq(name, skip(r'=>'), val))

# Правило для определения константных переменных
assign = group(seq(skip(r'var'), name, skip(r':='), val, skip(r';')))

# Правило для объектов (словарей)
obj = seq(skip(r'\['), group(many(seq(item, skip(r',')))), skip(r'\]'), mkobj)

# Правило обработки перемнных
val = alt(num, array, obj)

# Точка входа в программу обработки
main = seq(group(many(assign)), ws, mkobj)

def test():
    src = '''
    # comment
    {-
    что-то
    -}
    var Vm := [
        Ip => (list 192 168 44 44),
        Memory => 1024,
    ];
    '''
    s = parse(src, main)
    print(s.ok)
    print(s.stack)

test()