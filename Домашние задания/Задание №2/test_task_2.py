import json
import pytest
import yaml
from zipfile import ZipFile
from unittest.mock import patch
from task_2 import parse_package_json_from_zip, fetch, fetch_deps_from_internet, build_mermaid, read_config

# Фикстура для создания тестового ZIP архива с package.json
@pytest.fixture
def zip_with_package_json(tmp_path):
    package_json_content = json.dumps({
        "name": "test-package",
        "version": "1.0.0",
        "dependencies": {
            "dep1": "^1.0.0",
            "dep2": "^2.0.0"
        }
    })

    package_json_bytes = package_json_content.encode('utf-8')
    zip_path = tmp_path / "test-package.zip"

    with ZipFile(zip_path, 'w') as zip_file:
        zip_file.writestr('test-package/package.json', package_json_bytes)
    
    return zip_path

# Тест для функции parse_package_json_from_zip
def test_parse_package_json_from_zip(zip_with_package_json):
    deps, package_name = parse_package_json_from_zip(zip_with_package_json)
    
    assert package_name == "test-package"
    assert deps == {"dep1": "^1.0.0", "dep2": "^2.0.0"}

# Тест для функции fetch
@patch('requests.get')
def test_fetch(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "dependencies": {
            "transitive-dep1": "^3.0.0"
        }
    }

    deps = fetch("test-package", "1.0.0")
    assert deps == {"transitive-dep1": "^3.0.0"}

    mock_get.assert_called_once_with('https://registry.npmjs.org/test-package/1.0.0')

# Тест для функции fetch_deps_from_internet
@patch('requests.get')
def test_fetch_deps_from_internet(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    # Увеличиваем количество значений в side_effect для каждого запроса
    mock_response.json.side_effect = [
        {"dependencies": {"dep1": "^1.0.0", "dep2": "^2.0.0"}},  # Для root-package
        {"dependencies": {"dep3": "^3.0.0"}},                    # Для dep1
        {"dependencies": {}},                                    # Для dep2
        {"dependencies": {}}                                     # Для dep3
    ]
    
    deps = []
    fetch_deps_from_internet(deps, "root-package", "1.0.0")
    
    assert deps == [
        ("root-package", "dep1"),
        ("dep1", "dep3"),
        ("root-package", "dep2")
    ]

# Тест для функции build_mermaid
def test_build_mermaid():
    deps = [
        ("root-package", "dep1"),
        ("dep1", "dep2"),
        ("dep2", "dep3")
    ]
    
    mermaid_code = build_mermaid(deps, "root-package")
    expected_code = """flowchart TD
  root-package --> dep1
  dep1 --> dep2
  dep2 --> dep3
"""
    assert mermaid_code == expected_code

# Фикстура для создания тестового YAML файла конфигурации
@pytest.fixture
def config_yaml(tmp_path):
    config_content = {
        'package_path': 'test-package.zip',
        'output_path': 'output.md'
    }
    config_path = tmp_path / "config.yaml"
    
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(config_content, file)
    
    return config_path

# Тест для функции read_config
def test_read_config(config_yaml):
    config = read_config(config_yaml)
    
    assert config['package_path'] == 'test-package.zip'
    assert config['output_path'] == 'output.md'
