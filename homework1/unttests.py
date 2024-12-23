import unittest
import os
import shutil
from emulator import ShellEmulator
import tkinter as tk

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию для тестов
        self.test_virtual_fs = "test_virtual_fs.zip"
        self.test_virtual_fs_dir = "test_virtual_fs"
        self.test_config = "test_config.toml"
        self.root = tk.Tk()
        self.create_test_fs()
        self.create_test_config()
        self.app = ShellEmulator(self.root, self.test_config)

    def tearDown(self):
        # Удаляем временную директорию и файлы после тестов
        shutil.rmtree(self.test_virtual_fs_dir, ignore_errors=True)
        os.remove(self.test_virtual_fs)
        os.remove(self.test_config)
        self.root.destroy()

    def create_test_fs(self):
        os.makedirs(self.test_virtual_fs_dir, exist_ok=True)
        with open(os.path.join(self.test_virtual_fs_dir, "file1.txt"), "w") as f:
            f.write("Hello, world!\nThis is a test file.")
        with open(os.path.join(self.test_virtual_fs_dir, "file2.txt"), "w") as f:
            f.write("Another file.")
        shutil.make_archive(self.test_virtual_fs[:-4], 'zip', self.test_virtual_fs_dir)

    def create_test_config(self):
        with open(self.test_config, "w") as f:
            f.write(f"""
computer_name = "test_shell"

[paths]
virtual_fs = "{self.test_virtual_fs}"
log_file = "test_log.xml"
""")

    def test_list_files(self):
        self.app.list_files([])
        output = self.app.text_area.get(1.0, tk.END).strip()
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    def test_change_directory(self):
        self.app.change_directory([".."])
        self.assertEqual(self.app.current_path, "/")
        self.app.change_directory(["home"])
        self.assertNotEqual(self.app.current_path, "/")


    def test_word_count(self):
        self.app.word_count(["file1.txt"])
        output = self.app.text_area.get(1.0, tk.END).strip()
        self.assertIn("2 7 34", output)  # Проверка количества строк, слов и символов

    def test_clear_screen(self):
        self.app.text_area.insert(1.0, "Some text")
        self.app.clear_screen([])
        output = self.app.text_area.get(1.0, tk.END).strip()
        self.assertEqual(output, "")

    def exit_shell(self, args):
        self.master.quit()
        raise SystemExit


if __name__ == "__main__":
    unittest.main()
