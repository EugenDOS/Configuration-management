import os
import json
import yaml
from zipfile import ZipFile

def parse_package_json_from_zip(zip_file: str, package_name: str):
    """Читаем файл package.json из zip-файла."""
    with ZipFile(zip_file, 'r') as archive:
        # Формируем путь до package.json, который находится в одноимённой папке
        package_json_path = f"{package_name}/package.json"
        try:
            with archive.open(package_json_path) as file:
                package_data = json.load(file)
                return package_data.get('devDependencies', {})
        except KeyError:
            print(f"Файл {package_json_path} не найден в архиве.")
            return {}

def fetch_deps_from_zip(zip_file: str, package_name: str, deps: list, package: str):
    """Рекурсивно получаем транзитивные зависимости из zip-файла."""
    dependencies = parse_package_json_from_zip(zip_file, package)
    for dep_name, dep_version in dependencies.items():
        link = (package, dep_name)
        if link not in deps:
            deps.append(link)
            fetch_deps_from_zip(zip_file, package_name, deps, dep_name)

def build_mermaid(deps):
    """Формируем Mermaid диаграмму."""
    mermaid_code = 'flowchart TD\n'
    for src, dest in deps:
        mermaid_code += f'  {src} --> {dest}\n'
    return mermaid_code

def read_config(config_path: str):
    """Читаем конфигурацию из YAML файла."""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def main():
    config = read_config('config.yaml')

    # Путь к программе для визуализации графов (Graphviz и др.)
    # graphviz_path = config['graphviz_path']

    # Путь к zip-файлу пакета
    zip_file_path = config['package_zip_path']

    # Название папки и пакета
    package_name = config['package_name']

    # Получаем зависимости верхнего уровня из package.json внутри zip-файла
    main_deps = parse_package_json_from_zip(zip_file_path, package_name)
    
    # Список для хранения зависимостей
    deps = []
    
    # Рекурсивно собираем зависимости
    for dep_name, dep_version in main_deps.items():
        deps.append(('root', dep_name))
        fetch_deps_from_zip(zip_file_path, package_name, deps, dep_name)

    # Строим Mermaid диаграмму
    mermaid_code = build_mermaid(deps)
    
    # Путь к файлу-результату
    output_path = config['output_path']
    
    # Сохраняем результат в указанный файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(mermaid_code)
    
    # Выводим результат на экран
    print(f"Mermaid код сохранён в {output_path}.")
    print(mermaid_code)

if __name__ == "__main__":
    main()
