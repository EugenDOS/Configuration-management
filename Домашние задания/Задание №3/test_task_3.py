import pytest
from peco.peco import parse
from task_3 import main, variables  # точка и словарь переменных из основного кода

# Тест на успешную инициализацию константных переменных
def test_variable_assignment():
    src = '''
    var Num := 42;
    var List := (list 1 2 3 4);
    '''
    parse(src, main)
    assert variables['Num'] == 42.0
    assert variables['List'] == [1.0, 2.0, 3.0, 4.0]

# Тест на вычисление арифметического выражения с константой
def test_arithmetic_expression():
    src = '''
    var Num := 10;
    @{+ Num 5}
    '''
    result = parse(src, main)
    assert result.ok
    assert result.stack[0]['Num'] == 15.0  # Проверка, что Num увеличилось на 5

# Тест на минимальное значение
def test_min_expression():
    src = '''
    var Num := 20;
    @{min Num 10}
    '''
    result = parse(src, main)
    assert result.ok
    assert result.stack[0]['Num'] == 10.0  # Проверка, что Num стал равен минимальному значению

# Тест на модульное деление
def test_mod_expression():
    src = '''
    var Num := 15;
    @{mod Num 4}
    '''
    result = parse(src, main)
    assert result.ok
    assert result.stack[0]['Num'] == 3.0  # Проверка остатка от деления 15 на 4

# Тест на вложенные объекты
def test_nested_object():
    src = '''
    var Vm := [
        Ip => (list 192 168 1 1),
        Memory => 1024,
        Test => [
            UnderTest => 20,
        ],
    ];
    '''
    parse(src, main)
    assert variables['Vm']['Ip'] == [192.0, 168.0, 1.0, 1.0]
    assert variables['Vm']['Memory'] == 1024.0
    assert variables['Vm']['Test']['UnderTest'] == 20.0

# Тест на комментарии и пробелы
def test_comments_and_whitespace():
    src = '''
    # Это комментарий
    var Num := 50; # Комментарий
    var List := (list 5 6 7 8); {- Многострочный комментарий -}
    @{+ Num 10}
    '''
    result = parse(src, main)
    assert result.ok
    assert result.stack[0]['Num'] == 60.0
    assert result.stack[0]['List'] == [5.0, 6.0, 7.0, 8.0]

# Тест на отсутствие переменной в выражении
def test_undefined_variable_error():
    src = '''
    @{+ UndefinedVar 5}
    '''
    with pytest.raises(NameError):
        parse(src, main)
