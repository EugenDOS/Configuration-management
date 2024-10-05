import json
import os
from task_2 import parse_package_json, fetch_deps_from_node_modules, build_mermaid

def test_parse_package_json(tmpdir):
    # Создаем временный package.json файл
    package_path = tmpdir.mkdir("node_modules").mkdir("example-package")
    package_json_path = package_path.join("package.json")
    package_json_data = {
        "dependencies": {
            "dep1": "1.0.0",
            "dep2": "2.0.0"
        }
    }
    with open(package_json_path, 'w', encoding='utf-8') as f:
        json.dump(package_json_data, f)

    # Передаем путь до node_modules, а не только tmpdir
    dependencies = parse_package_json(os.path.join(str(tmpdir), "node_modules"), "example-package")
    
    # Проверяем результат
    assert dependencies == {"dep1": "1.0.0", "dep2": "2.0.0"}


def test_fetch_deps_from_node_modules(tmpdir):
    # Временные package.json файлы
    node_modules_path = tmpdir.mkdir("node_modules")
    package_path = node_modules_path.mkdir("example-package")
    package_json_data = {
        "dependencies": {
            "dep1": "1.0.0",
        }
    }
    with open(package_path.join("package.json"), 'w', encoding='utf-8') as f:
        json.dump(package_json_data, f)

    dep1_path = node_modules_path.mkdir("dep1")
    dep1_json_data = {
        "dependencies": {
            "dep2": "2.0.0"
        }
    }
    with open(dep1_path.join("package.json"), 'w', encoding='utf-8') as f:
        json.dump(dep1_json_data, f)

    deps = []
    fetch_deps_from_node_modules(str(node_modules_path), deps, "example-package")

    assert deps == [("example-package", "dep1"), ("dep1", "dep2")]

def test_build_mermaid():
    deps = [("example-package", "dep1"), ("dep1", "dep2")]
    expected_mermaid = "flowchart TD\n  example-package --> dep1\n  dep1 --> dep2\n"
    result = build_mermaid(deps)
    assert result == expected_mermaid
