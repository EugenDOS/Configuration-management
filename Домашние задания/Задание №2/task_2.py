import os
import json
import yaml

def parse_package_json(package_path: str, package: str):
    """Парсинг файла package.json для извлечения зависимостей пакета."""
    package_json_path = os.path.join(package_path, package, 'package.json')
    if not os.path.exists(package_json_path):
        return {}
    with open(package_json_path, 'r', encoding='utf-8') as file:
        package_data = json.load(file)
    return package_data.get('dependencies', {})

def fetch_deps_from_node_modules(node_modules_path: str, deps: list, package: str):
    """Рекурсивное получение транзитивных зависимостей из node_modules."""
    dependencies = parse_package_json(node_modules_path, package)
    for dep_name, dep_version in dependencies.items():
        link = (package, dep_name)
        if link not in deps:
            deps.append(link)
            fetch_deps_from_node_modules(node_modules_path, deps, dep_name)

def build_mermaid(deps):
    """Формирование Mermaid-диаграммы."""
    mermaid_code = 'flowchart TD\n'
    for src, dest in deps:
        mermaid_code += f'  {src} --> {dest}\n'
    return mermaid_code

def read_config(config_path: str):
    """Читение конфигурации из yaml-файла."""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def main():
    config = read_config('config.yaml')
    node_modules_path = config['package_path']  # Путь к папке node_modules
    deps = []   # Список для хранения зависимостей
    
    # Получаем зависимости верхнего уровня из package.json каждого пакета в node_modules
    for package in os.listdir(node_modules_path):
        package_dir = os.path.join(node_modules_path, package)
        if os.path.isdir(package_dir) and os.path.exists(os.path.join(package_dir, 'package.json')):
            fetch_deps_from_node_modules(node_modules_path, deps, package)

    mermaid_code = build_mermaid(deps)  # Строим Mermaid диаграмму
    output_path = config['output_path'] # Путь к файлу-результату
    
    # Сохраняем результат в указанный файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(mermaid_code)

    print(f"Mermaid код сохранён в {output_path}.")
    print(mermaid_code)

if __name__ == "__main__":
    main()
