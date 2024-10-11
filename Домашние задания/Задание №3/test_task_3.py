import pytest
from task_3 import parse_input, ConfigSyntaxError

# Тест на парсинг правильного списка
def test_parse_input_list():
    input_text = "(list 1 2 3 4)"
    result = parse_input(input_text)
    assert result['list'] == [1, 2, 3, 4]

# Тест на парсинг правильного словаря
def test_parse_input_dict():
    input_text = "[key1 => 10, key2 => 20]"
    result = parse_input(input_text)
    assert result['dict'] == {'key1': 10, 'key2': 20}

# Тест на парсинг константного выражения и подстановки
def test_parse_input_constant_expression():
    input_text = """
    var a := 5;
    var b := @{+ a 3};
    [key1 => b]
    """
    result = parse_input(input_text)
    assert result['dict'] == {'key1': 8}

# Тест на вложенные константные выражения
def test_parse_input_nested_expressions():
    input_text = """
    var a := @{+ 2 2};
    var b := @{* a 5};
    (list 1 @{+ 1 2} @{mod 10 3})
    [key => @{* 2 3}]
    """
    result = parse_input(input_text)
    assert result['list'] == [1, 3, 1]
    assert result['dict'] == {'key': 6}

# Тест на синтаксическую ошибку в словаре
def test_parse_input_invalid_dict_syntax():
    input_text = "[key1 10]"  # Неправильный формат словаря
    with pytest.raises(ConfigSyntaxError, match="Ошибка синтаксиса: неверный формат словаря '\\[key1 10\\]'"):
        parse_input(input_text)

# Тест на синтаксическую ошибку в константном выражении
def test_parse_input_invalid_constant_expression():
    input_text = "var a := @{+ 1};"  # Неполное выражение
    with pytest.raises(ConfigSyntaxError, match="Ошибка синтаксиса: неверное выражение"):
        parse_input(input_text)

# Тест на корректную обработку комментариев
def test_parse_input_with_comments():
    input_text = """
    # Это комментарий
    var a := 5;  # Еще один комментарий
    {- Многострочный
    комментарий -}
    [key1 => a]
    """
    result = parse_input(input_text)
    assert result['dict'] == {'key1': 5}

# Тест на работу с числовыми выражениями
def test_parse_input_math_operations():
    input_text = """
    var x := @{+ 10 20};
    var y := @{min 10 15};
    [result1 => x, result2 => y]
    """
    result = parse_input(input_text)
    assert result['dict'] == {'result1': 30, 'result2': 10}

# Тест на парсинг пустого списка
def test_parse_input_empty_list():
    input_text = "(list)"
    result = parse_input(input_text)
    assert result['list'] == []

# Тест на синтаксическую ошибку в объявлении переменной
def test_parse_input_invalid_var_syntax():
    input_text = "var a := ;"  # Неправильный синтаксис объявления переменной
    with pytest.raises(ConfigSyntaxError, match="Ошибка синтаксиса: неверное объявление переменной"):
        parse_input(input_text)

# Тест на корректное парсинг и преобразование целых чисел
def test_parse_input_with_numbers():
    input_text = """
    var num1 := 10;
    var num2 := 20;
    [key1 => num1, key2 => num2]
    """
    result = parse_input(input_text)
    assert result['dict'] == {'key1': 10, 'key2': 20}
