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
        if command == "ls":
            names = ""
            for name in myzip.namelist():
                names += name + "\n"
            output_area.insert(tk.END, names)

        elif command == "exit":
            exit()

        elif command.startswith("cat"):
            path = command.split()[1]
            content = myzip.read(path).decode()
            output_area.insert(tk.END, content + "\n")


root = tk.Tk()
root.title("Linux command prompt visializer")

output_area = tk.Text(root, height=10, width=40)
output_area.pack(pady=10)

input_area = tk.Text(root, height=2, width=40)
input_area.pack(pady=10)

exec_button = tk.Button(root, text="Run", command=command)
exec_button.pack(pady=5)

root.mainloop()