import argparse
import tkinter as tk
from zipfile import ZipFile


parser = argparse.ArgumentParser(description="Main info getter")
parser.add_argument("user_name", type=str, help="User name")
parser.add_argument("pc_name", type=str, help="PC name")
parser.add_argument("zip_path", type=str, help="Path to zip archive")
args = parser.parse_args()


current_directory = ""

# Словарь для хранения прав доступа к файлам в виде метаданных
permissions = {}

def command():
    global current_directory
    command = input_area.get("1.0", tk.END)[:-1]
    
    with ZipFile(args.zip_path, "a") as myzip:
        
        if command == "ls": 
            ls([name for name in myzip.namelist() if name.startswith(current_directory)])
        
        elif command == "exit": 
            exit()
        
        elif command.startswith("cd"):
            try:
                path = command.split()[1]
                cd(path)
            except IndexError:
                write("Bad syntax for cd. Use: cd <file_path>\n")
        
        elif command.startswith("chmod"):
            try:
                parts = command.split()
                mode = parts[1]
                file_path = parts[2]
                chmod(mode, file_path)
            except IndexError:
                write("Bad syntax for chmod. Use: chmod <mode> <file_path>\n")
                
        else:
            write("Bad syntax or unknow command\n")

def chmod(mode, file_path):
    global permissions
    # Проверка, что файл существует в архиве
    with ZipFile(args.zip_path) as myzip:
        full_path = current_directory + file_path
        if full_path in myzip.namelist():
            try:
                octal_mode = int(mode, 8)
                permissions[full_path] = octal_mode
                write(f"Changed permissions of {file_path} to {mode}")
            except ValueError:
                write("Invalid mode. Use octal format (e.g., 755, 644).\n")
        else:
            write(f"File {file_path} not found in the current directory.\n")

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
        for item in all_items:
            if current_directory + item in permissions:
                mode_str = oct(permissions[current_directory + item])[2:]
                write(f"{mode_str} {item}")
            else:
                write(f"--- {item}")
        write()
    else:
        write("No files or directories found\n")

def cd(path):
    global current_directory
    with ZipFile(args.zip_path) as myzip:
        if path == "/":  # Если пользователь хочет перейти в корень
            current_directory = ""  # Корень архива
            write("Returned to root directory\n")
        elif any(name.startswith(path) for name in myzip.namelist()):
            current_directory = path if path.endswith("/") else path + "/"
            write(f"Changed directory to {current_directory}\n")
        else:
            write(f"Directory {path} not found\n")
    updateLabel()

def updateLabel():
    label.config(text=f"PATH: {current_directory}")

def write(text=""):
    output_area.configure(state=tk.NORMAL)
    output_area.insert(tk.END, text+"\n")
    output_area.configure(state=tk.DISABLED)

def clear():
    output_area.configure(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.configure(state=tk.DISABLED)


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
