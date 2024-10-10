import os
import json
import yaml
import zipfile
import requests

def parse_package_json_from_zip(zip_path: str):
    """Парсинг файла `package.json` внутри ZIP-архива."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Находим файл package.json внутри одноимённой папки в ZIP
        package_name = os.path.splitext(os.path.basename(zip_path))[0]
        package_json_path = f'{package_name}/package.json'
        
        with zip_ref.open(package_json_path) as file:
            package_data = json.load(file)
    
    return package_data.get('dependencies', {}), package_name  # Вернём также имя пакета

def fetch(name, version):
    """Запрос транзитивных зависимостей пакета из NPM."""
    r = requests.get(f'https://registry.npmjs.org/{name}/{version}')
    if r.status_code == 200:
        return r.json().get('dependencies', {})
    return {}

def fetch_deps_from_internet(deps: list, package: str, version: str):
    """Рекурсивное получение зависимостей через NPM API."""
    dependencies = fetch(package, version)
    for dep_name, dep_version in dependencies.items():
        link = (package, dep_name)
        if link not in deps:
            deps.append(link)
            fetch_deps_from_internet(deps, dep_name, dep_version)

def build_mermaid(deps, root_package):
    """Формирование Mermaid-диаграммы."""
    mermaid_code = 'flowchart TD\n'
    added_links = set()
    
    for src, dest in deps:
        if src == root_package:
            src = root_package  # Приведение имени к корневому пакету
        link = f'{src} --> {dest}'
        if link not in added_links:  # Избегаем дублирования и циклических зависимостей
            mermaid_code += f'  {link}\n'
            added_links.add(link)
    
    return mermaid_code

def read_config(config_path: str):
    """Чтение конфигурации из YAML-файла."""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def main():
    config = read_config('config.yaml')
    zip_package_path = config['package_path']  # Путь к ZIP-пакету
    deps = []   # Список для хранения зависимостей
    
    # Получаем зависимости верхнего уровня из package.json в ZIP файле
    dependencies, root_package = parse_package_json_from_zip(zip_package_path)
    
    # Для каждого пакета зависимости находим транзитивные зависимости
    for package_name, package_version in dependencies.items():
        link = (root_package, package_name)
        if link not in deps:
            deps.append(link)
            fetch_deps_from_internet(deps, package_name, package_version)

    # Строим Mermaid диаграмму
    mermaid_code = build_mermaid(deps, root_package)
    output_path = config['output_path']  # Путь к файлу-результату
    
    # Сохраняем результат в указанный файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(mermaid_code)

    print(f"Mermaid код сохранён в {output_path}")
    print(mermaid_code)

if __name__ == "__main__":
    main()
