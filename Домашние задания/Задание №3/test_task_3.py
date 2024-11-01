import pytest
import yaml
from peco.peco import *
from task_3 import main, ParserError

# Функция для парсинга строк напрямую
def parse_config(src):
    s = parse(src, main)
    if s.ok:
        # Преобразуем результат в словарь
        result_dict = dict(s.stack[0]) if isinstance(s.stack, tuple) else s.stack
        return yaml.dump(result_dict, default_flow_style=False, allow_unicode=True)
    else:
        raise ParserError("Parsing failed.")

# === Тесты для чисел (Num) ===
def test_valid_num():
    src = "var Num := 42;"
    expected_output = "Num: 42.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

def test_invalid_num():
    src = "var Num := invalid_number;"
    with pytest.raises(ParserError):
        parse_config(src)

# === Тесты для массивов (List) ===
def test_valid_list():
    src = "var List := (list 1 2 3 4 5);"
    expected_output = "List:\n- 1.0\n- 2.0\n- 3.0\n- 4.0\n- 5.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

def test_invalid_list():
    src = "var List := (list 1 2 three 4 5);"
    with pytest.raises(ParserError):
        parse_config(src)

def test_empty_list():
    src = "var EmptyList := (list);"
    expected_output = "EmptyList: []\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

# === Тесты для объектов (Vm) ===
def test_valid_obj():
    src = '''
    var Vm := [
        Ip => (list 192 168 1 1),
        Memory => 2048,
    ];
    '''
    expected_output = "Vm:\n  Ip:\n  - 192.0\n  - 168.0\n  - 1.0\n  - 1.0\n  Memory: 2048.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

def test_invalid_obj():
    src = '''
    var Vm := [
        Ip => (list 192 168 1 one),
        Memory => 2048,
    ];
    '''
    with pytest.raises(ParserError):
        parse_config(src)

def test_empty_dict():
    src = "var EmptyDict := [];"
    expected_output = "EmptyDict: {}\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

# === Тесты для константных выражений (операции с переменными) ===
def test_valid_const_expr():
    src = '''
    var Num := 10;
    var ConstExpr := @{+ Num 5};
    '''
    expected_output = "Num: 10.0\nConstExpr: 15.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

def test_invalid_const_expr():
    src = '''
    var Num := 10;
    @{+ NotDefinedVar 5}
    '''
    with pytest.raises(ParserError):
        parse_config(src)

def test_mod_operation():
    src = '''
    var Num := 10;
    var ModResult := @{mod Num 3};
    '''
    expected_output = "Num: 10.0\nModResult: 1.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

def test_min_operation():
    src = '''
    var Num := 10;
    var MinResult := @{min Num 3};
    '''
    expected_output = "Num: 10.0\nMinResult: 3.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

# === Тесты для вложенных структур ===
def test_valid_nested_obj():
    src = '''
    var Vm := [
        Ip => (list 192 168 1 1),
        Config => [
            CPU => 4,
            RAM => 4096,
        ],
    ];
    '''
    expected_output = (
        "Vm:\n"
        "  Ip:\n"
        "  - 192.0\n"
        "  - 168.0\n"
        "  - 1.0\n"
        "  - 1.0\n"
        "  Config:\n"
        "    CPU: 4.0\n"
        "    RAM: 4096.0\n"
    )
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

def test_invalid_nested_obj():
    src = '''
    var Vm := [
        Ip => (list 192 168 1 1),
        Config => [
            CPU => four,
            RAM => 4096,
        ],
    ];
    '''
    with pytest.raises(ParserError):
        parse_config(src)

# === Тесты на некорректный синтаксис ===
def test_missing_semicolon():
    src = "var Num := 42"
    with pytest.raises(ParserError):
        parse_config(src)

def test_incorrect_syntax_structure():
    src = '''
    var Num := 10;
    @{+ Num 5
    '''
    with pytest.raises(ParserError):
        parse_config(src)

def test_unclosed_list():
    src = "var List := (list 1 2 3;"
    with pytest.raises(ParserError):
        parse_config(src)

# === Тесты на пробелы и отступы ===
def test_spaces_and_indentation():
    src = "   var    Num   :=   42   ;   "
    expected_output = "Num: 42.0\n"
    assert yaml.safe_load(parse_config(src)) == yaml.safe_load(expected_output)

