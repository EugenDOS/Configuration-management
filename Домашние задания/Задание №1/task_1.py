import argparse
import tkinter as tk
import calendar
from datetime import datetime
from zipfile import ZipFile

current_directory = ""
permissions = {}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Main info getter")
    parser.add_argument("user_name", type=str, help="User name")
    parser.add_argument("pc_name", type=str, help="PC name")
    parser.add_argument("zip_path", type=str, help="Path to zip archive")
    return parser.parse_args()

def command(cmd=None):
    global current_directory
    
    if cmd:
        command = cmd
    else:
        command = input_area.get("1.0", tk.END)[:-1]
    
    with ZipFile(args.zip_path, "a") as myzip:
        
        if command == "ls": 
            return ls([name for name in myzip.namelist() if name.startswith(current_directory)])
        
        elif command == "exit": 
            exit()
        
        elif command.startswith("cd"):
            try:
                path = command.split()[1]
                return cd(path)
            except IndexError:
                return write("Bad syntax for cd. Use: cd <file_path>\n")
        
        elif command.startswith("chmod"):
            try:
                parts = command.split()
                mode = parts[1]
                file_path = parts[2]
                return chmod(mode, file_path)
            except IndexError:
                return write("Bad syntax for chmod. Use: chmod <mode> <file_path>\n")
                
        elif command.startswith("cal"):
            try:
                parts = command.split()
                if len(parts) == 1:  # Если команда без аргументов
                    return cal()
                elif len(parts) == 2:  # Если указан только месяц
                    month = int(parts[1])
                    year = datetime.now().year  # Текущий год по умолчанию
                    return cal(month, year)
                elif len(parts) == 3:  # Если указан и месяц, и год
                    month = int(parts[1])
                    year = int(parts[2])
                    return cal(month, year)
                else:
                    return write("Bad syntax for cal. Use: cal [month] [year]\n")
            except ValueError:
                return write("Invalid month or year. Please enter numeric values.\n")

        elif command.startswith("find"):
            try:
                parts = command.split()
                if len(parts) == 2:  # Если указан критерий поиска
                    search_term = parts[1]
                    return find(search_term)
                else:
                    return write("Bad syntax for find. Use: find <search_term>\n")
            except ValueError:
                return write("Invalid search term.\n")
                
        else:
            return write("Bad syntax or unknown command.\n")


def find(search_term):
    with ZipFile(args.zip_path) as myzip:
        matches = [name for name in myzip.namelist() if search_term in name]
        
        if matches:
            rslt = ""
            rslt += write(f"Found {len(matches)} result(s):")
            for match in matches:
                rslt += write(match)
            write()
            return rslt
        else:
            return write(f"No results found for '{search_term}'.\n")

def cal(month=None, year=None):
    # Если месяц и год не указаны, выводим текущий месяц и год
    if month is None and year is None:
        now = datetime.now()
        month = now.month
        year = now.year
    
    cal_str = calendar.TextCalendar().formatmonth(year, month)
    return write(cal_str)

def chmod(mode, file_path):
    global permissions
    # Проверка, что файл существует в архиве
    with ZipFile(args.zip_path) as myzip:
        full_path = current_directory + file_path
        if full_path in myzip.namelist():
            try:
                octal_mode = int(mode, 8)
                permissions[full_path] = octal_mode
                return write(f"Changed permissions of {file_path} to {mode}\n")
            except ValueError:
                return write("Invalid mode. Use octal format (e.g., 755, 644).\n")
        else:
            return write(f"File {file_path} not found in the current directory.\n")

def ls(name_list):
    directories = set()
    files = set()
    
    for name in name_list:
        # Удаление части пути до текущей директории
        relative_path = name[len(current_directory):]

        # Если есть поддиректории, то это директория
        if relative_path.endswith("/"):
            directories.add(relative_path.split("/")[0] + "/")
        else:
            # Если это файл, добавляем его полностью (с расширением)
            files.add(relative_path)

    # Объединение директорий и файлов для вывода
    all_items = sorted(directories | files)
    
    if all_items:
        rslt = ""
        for item in all_items:
            if current_directory + item in permissions:
                mode_str = oct(permissions[current_directory + item])[2:]
                rslt += write(f"{mode_str} {item}")
            else:
                rslt += write(f"--- {item}")
        write()
        return rslt
    else:
        return write("No files or directories found\n")

def cd(path):
    global current_directory
    with ZipFile(args.zip_path) as myzip:
        if path == "/":  # Если пользователь хочет перейти в корень
            current_directory = ""  # Корень архива
            return write("Returned to root directory\n"), current_directory
        elif any(name.startswith(path) for name in myzip.namelist()):
            current_directory = path if path.endswith("/") else path + "/"
            return write(f"Changed directory to {current_directory}\n"), current_directory
        else:
            return write(f"Directory {path} not found\n"), current_directory
    updateLabel()

def updateLabel():
    label.config(text=f"PATH: {current_directory}")

def write(text=""):
    try:
        output_area.configure(state=tk.NORMAL)
        output_area.insert(tk.END, text+"\n")
        output_area.configure(state=tk.DISABLED)
        return text
    except:
        return text

def clear():
    output_area.configure(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.configure(state=tk.DISABLED)


if __name__ == "__main__":    
    args = parse_arguments()
    
    root = tk.Tk()
    root.title(f"Terminal — {args.user_name}@{args.pc_name}")
    root.geometry("450x320")

    label = tk.Label(text=f"PATH: {current_directory}")
    label.pack()

    output_area = tk.Text(root, height=10, width=45, state=tk.DISABLED)
    output_area.pack(pady=10)

    input_area = tk.Text(root, height=2, width=45)
    input_area.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    exec_button = tk.Button(button_frame, text="Run", command=command)
    exec_button.pack(side=tk.LEFT, padx=10)

    clear_button = tk.Button(button_frame, text="Clear", command=clear)
    clear_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()
