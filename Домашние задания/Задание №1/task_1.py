import argparse
import tkinter as tk
from zipfile import ZipFile


parser = argparse.ArgumentParser(description="Main info getter")
parser.add_argument("user_name", type=str, help="User name")
parser.add_argument("pc_name", type=str, help="PC name")
parser.add_argument("zip_path", type=str, help="Path to zip archive")
args = parser.parse_args()


def command():
    command = input_area.get("1.0", tk.END)[:-1]
    
    with ZipFile(args.zip_path, "a") as myzip:
        
        if command == "ls": ls(myzip.namelist())
        
        elif command == "exit": exit()
        
        elif command.startswith("cat"): 
            path = command.split()[1]
            cat(myzip.read(path).decode())

            
def write(text_widget: tk.Text, text):
    text_widget.configure(state=tk.NORMAL)
    text_widget.insert(tk.END, text)
    text_widget.configure(state=tk.DISABLED)

def ls(name_list):
    names = ""
    for name in name_list:
        names += name + "\n"
    write(output_area, names)

def cat(content):
    output_area.insert(tk.END, content + "\n")

def clear():
    output_area.delete('1.0', tk.END)


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