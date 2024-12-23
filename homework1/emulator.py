import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import zipfile
import datetime
import argparse
import toml
import xml.etree.ElementTree as ET

class ShellEmulator:
    def __init__(self, master, config_path):
        self.master = master
        self.master.title("Shell Emulator")

        self.load_config(config_path)
        self.current_path = "/"
        self.history = []

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)

        self.label = tk.Label(master, text=f"{self.computer_name}:{self.current_path}$ ")
        self.label.pack(padx=10, pady=5)

        self.extract_virtual_fs()

    def load_config(self, config_path):
        try:
            config = toml.load(config_path)
            self.computer_name = config.get("computer_name", "shell")
            self.virtual_fs_path = config["paths"]["virtual_fs"]
            self.log_file_path = config["paths"]["log_file"]
        except (FileNotFoundError, KeyError, toml.TomlDecodeError) as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки конфигурации: {e}")
            self.master.quit()

    def log_action(self, action):
        root = ET.Element("log")
        entry = ET.SubElement(root, "entry")
        ET.SubElement(entry, "timestamp").text = datetime.datetime.now().isoformat()
        ET.SubElement(entry, "action").text = action

        try:
            if os.path.exists(self.log_file_path):
                tree = ET.parse(self.log_file_path)
                root = tree.getroot()
                root.append(entry)
            else:
                root.append(entry)
            tree = ET.ElementTree(root)
            tree.write(self.log_file_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            self.text_area.insert(tk.END, f"Ошибка записи в лог: {e}\n")

    def extract_virtual_fs(self):
        if not os.path.exists(self.virtual_fs_path):
            messagebox.showerror("Ошибка", "Файл виртуальной файловой системы не найден.")
            self.master.quit()
            return

        with zipfile.ZipFile(self.virtual_fs_path, 'r') as zip_ref:
            zip_ref.extractall("virtual_fs")

    def execute_command(self, event):
        command = self.entry.get().strip()
        self.history.append(command)
        self.log_action(command)

        cmd, *args = command.split()
        cmd_dict = {
            "ls": self.list_files,
            "cd": self.change_directory,
            "exit": self.exit_shell,
            "wc": self.word_count,
            "clear": self.clear_screen
        }

        if cmd in cmd_dict:
            cmd_dict[cmd](args)
        else:
            self.text_area.insert(tk.END, f"{cmd}: команда не найдена\n")

        self.entry.delete(0, tk.END)
        self.label.config(text=f"{self.computer_name}:{self.current_path}$ ")

    def list_files(self, args):
        path = os.path.join("virtual_fs", self.current_path.strip("/"))
        try:
            files = os.listdir(path)
            output = "\n".join(files) if files else "Пустая директория"
            self.text_area.insert(tk.END, f"{output}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Ошибка: директория не найдена\n")

    def change_directory(self, args):
        if not args:
            self.text_area.insert(tk.END, "Ошибка: не указан путь\n")
            return

        new_path = args[0]
        if new_path == "..":
            if self.current_path != "/":
                self.current_path = "/".join(self.current_path.strip("/").split("/")[:-1]) or "/"
        else:
            potential_path = os.path.join("virtual_fs", self.current_path.strip("/"), new_path)
            if os.path.isdir(potential_path):
                self.current_path = os.path.join(self.current_path, new_path).replace("\\", "/").lstrip("/")
            else:
                self.text_area.insert(tk.END, "Ошибка: директория не найдена\n")

    def word_count(self, args):
        if not args:
            self.text_area.insert(tk.END, "Ошибка: не указан файл\n")
            return

        file_path = os.path.join("virtual_fs", self.current_path.strip("/"), args[0])
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.splitlines()
                words = content.split()
                chars = len(content)
                self.text_area.insert(tk.END, f"{len(lines)} {len(words)} {chars} {args[0]}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Ошибка: файл не найден\n")

    def clear_screen(self, args):
        self.text_area.delete(1.0, tk.END)

    def exit_shell(self, args):
        self.master.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("config", help="Путь к конфигурационному файлу")
    args = parser.parse_args()

    root = tk.Tk()
    app = ShellEmulator(root, args.config)
    root.mainloop()
