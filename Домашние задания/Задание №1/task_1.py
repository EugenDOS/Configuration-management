import argparse
import tkinter as tk
from zipfile import ZipFile


parser = argparse.ArgumentParser(description="Main info getter")
parser.add_argument("user_name", type=str, help="User name")
parser.add_argument("pc_name", type=str, help="PC name")
parser.add_argument("zip_path", type=str, help="Path to zip archive")
args = parser.parse_args()


current_directory = ""

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
                write(output_area, "Bad syntax")


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
        names = "\n".join(all_items)
        write(output_area, names)
    else:
        write(output_area, "No files or directories found")

def cd(path):
    global current_directory
    # Проверка, что путь существует внутри архива
    with ZipFile(args.zip_path) as myzip:
        if any(name.startswith(path) for name in myzip.namelist()):
            current_directory = path if path.endswith("/") else path + "/"
            write(output_area, f"Changed directory to {current_directory}")
        else:
            write(output_area, f"Directory {path} not found")


def write(text_widget: tk.Text, text):
    text_widget.configure(state=tk.NORMAL)
    text_widget.insert(tk.END, text+"\n\n")
    text_widget.configure(state=tk.DISABLED)

def clear():
    output_area.configure(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.configure(state=tk.DISABLED)


root = tk.Tk()
root.title(f"Terminal — {args.user_name}@{args.pc_name}")

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
