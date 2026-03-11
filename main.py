import tkinter as tk
import ctypes
from tkinter import messagebox
def ask_integer_custom(title, pr):
    result = None

    def on_ok():
        nonlocal result
        try:
            result = int(entry.get())
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число!")
            entry.focus_set()

    def validate(action, char, current_value, new_value):
        if action == '1':
            if char == '-':
                return current_value == "" 
            else:
                return char.isdigit()
        return True

    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.transient()
    dialog.grab_set()
    dialog.resizable(False, False)

    tk.Label(dialog, text=pr).pack(padx=10, pady=5)

    validaciya = (dialog.register(validate), '%d', '%S', '%s', '%P')
    entry = tk.Entry(dialog, validate='key', validatecommand=validaciya)
    entry.pack(padx=10, pady=5)
    entry.focus_set()

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="OK", command=on_ok, width=8).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Отмена", command=dialog.destroy, width=8).pack(side=tk.LEFT, padx=5)

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    dialog.wait_window()
    return result

class PybindQueueAdapter:
    def __init__(self):
        import queue_stl_pybind
        self.q = queue_stl_pybind.Queue()
        self.q.create_queue()

    def enqueue(self, value):
        self.q.enqueue(value)

    def dequeue(self):
        return self.q.dequeue()

    def peek(self):
        return self.q.peek()

    def size(self):
        return self.q.size()

    def clear(self):
        self.q.clear()

    def fill_random(self, count, min_val, max_val):
        self.q.fill_random(count, min_val, max_val)

    def get_all(self):
        return self.q.get_all()

class CppManualAdapter:
    def __init__(self, dll_path):
        import ctypes
        self.lib = ctypes.CDLL(dll_path)
        self.lib.create_queue.argtypes = []
        self.lib.create_queue.restype = None
        self.lib.is_empty.argtypes = []
        self.lib.is_empty.restype = ctypes.c_int
        self.lib.enqueue.argtypes = [ctypes.c_int]
        self.lib.enqueue.restype = None
        self.lib.dequeue.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.dequeue.restype = ctypes.c_int
        self.lib.peek.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.peek.restype = ctypes.c_int
        self.lib.size.argtypes = []
        self.lib.size.restype = ctypes.c_int
        self.lib.clear_queue.argtypes = []
        self.lib.clear_queue.restype = None
        self.lib.fill_random.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.lib.fill_random.restype = None
        self.lib.create_queue()

    def enqueue(self, value):
        self.lib.enqueue(value)

    def dequeue(self):
        success = ctypes.c_int()
        val = self.lib.dequeue(ctypes.byref(success))
        return val, bool(success.value)

    def peek(self):
        val = ctypes.c_int()
        ok = self.lib.peek(ctypes.byref(val))
        return val.value, bool(ok)

    def size(self):
        return self.lib.size()

    def clear(self):
        self.lib.clear_queue()

    def fill_random(self, count, min_val, max_val):
        self.lib.fill_random(count, min_val, max_val)

    def get_all(self):
        items = []
        while True:
            v, ok = self.dequeue()
            if not ok:
                break
            items.append(v)
        for v in items:
            self.enqueue(v)
        return items
    
class PythonQueueAdapter:
    def __init__(self):
        import queue_python
        self.q = queue_python.QueuePython()
        self.q.clear()

    def enqueue(self, value):
        self.q.enqueue(value)

    def dequeue(self):
        return self.q.dequeue()

    def peek(self):
        return self.q.peek()

    def size(self):
        return self.q.size()

    def clear(self):
        self.q.clear()

    def fill_random(self, count, min_val, max_val):
        self.q.fill_random(count, min_val, max_val)

    def get_all(self):
        return self.q.get_all()

class QueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Очередь")
        self.root.geometry("800x650")

        self.queue = None
        self.current_impl = None

        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)
        tk.Label(top_frame, text="Реализация:").pack(side=tk.LEFT)

        self.impl_var = tk.StringVar(value="cpp_pybind")

        rb_manual = tk.Radiobutton(top_frame, text="C++ ручная(ctypes)", variable=self.impl_var,
                           value="cpp_manual", command=self.switch_impl)
        rb_manual.pack(side=tk.LEFT, padx=5)

        rb_pybind = tk.Radiobutton(top_frame, text="C++ STL (pybind)", variable=self.impl_var,
                                   value="cpp_pybind", command=self.switch_impl)
        rb_pybind.pack(side=tk.LEFT, padx=5)

        rb_py = tk.Radiobutton(top_frame, text="Python", variable=self.impl_var,
                               value="python", command=self.switch_impl)
        rb_py.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(root, text="Элементов в очереди: 0", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.listbox = tk.Listbox(root, height=15, width=50, font=("Courier", 12))
        self.listbox.pack(pady=10)

        btn_style = {'bg': 'green', 'fg': 'pink', 'width': 26, 'height': 2}

        self.sozdat_btn = tk.Button(root, text="Очистить очередь", **btn_style,
                                     command=self.create_or_clear)
        self.dobavit_btn = tk.Button(root, text="Добавить элемент", **btn_style,
                                     command=self.add_item)
        self.delet_btn = tk.Button(root, text="Удалить элемент", **btn_style,
                                   command=self.remove_item)
        self.show_perv_btn = tk.Button(root, text="Просмотреть первый элемент", **btn_style,
                                       command=self.peek_item)
        self.show_btn = tk.Button(root, text="Показать очередь", **btn_style,
                                  command=self.show_queue_popup)
        self.show_count_btn = tk.Button(root, text="Показать кол-во элементов", **btn_style,
                                        command=self.show_size)
        self.random_btn = tk.Button(root, text="Заполнить случайными эл-ми", **btn_style,
                                    command=self.fill_random)
        self.exit_btn = tk.Button(root, text="Выход", **btn_style,
                                  command=self.exit_app)

        self.sozdat_btn.pack()
        self.dobavit_btn.pack()
        self.delet_btn.pack()
        self.show_perv_btn.pack()
        self.show_btn.pack()
        self.show_count_btn.pack()
        self.random_btn.pack()
        self.exit_btn.pack()

        self.switch_impl()

    def switch_impl(self):
        impl = self.impl_var.get()
        if impl == self.current_impl:
            return 

        try:
            if impl == "cpp_manual":
                self.queue = CppManualAdapter("./queue_manual.dll")
            elif impl == "cpp_pybind":
                self.queue = PybindQueueAdapter()
            else:
                self.queue = PythonQueueAdapter()

            self.current_impl = impl
            self.refresh_display()
            messagebox.showinfo("Успех", f"Загружена реализация: {impl}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить {impl}:\n{e}")
            self.impl_var.set(self.current_impl)

    def refresh_display(self):
        self.listbox.delete(0, tk.END)
        if not self.queue:
            return
        sz = self.queue.size()
        self.info_label.config(text=f"Элементов(та) в очереди: {sz}")
        for val in self.queue.get_all():
            self.listbox.insert(tk.END, str(val))

    def show_queue_popup(self):
        if not self.queue:
            return
        items = self.queue.get_all()
        if items:
            messagebox.showinfo("Содержимое очереди", " -> ".join(str(x) for x in items))
        else:
            messagebox.showinfo("Содержимое очереди", "Очередь пуста")

    def show_size(self):
        if not self.queue:
            return
        messagebox.showinfo("Количество", f"В очереди {self.queue.size()} элементов(та)")

    def create_or_clear(self):
        if not self.queue:
            return
        self.queue.clear()
        self.refresh_display()
        messagebox.showinfo("Очередь", "Очередь очищена")

    def add_item(self):
        if not self.queue:
            return
        value = ask_integer_custom("Добавить", "Введите целое число:")
        if value is not None:
            self.queue.enqueue(value)
            self.refresh_display()

    def remove_item(self):
        if not self.queue:
            return
        val, success = self.queue.dequeue()
        if success:
            messagebox.showinfo("Удалено", f"Удалён элемент: {val}")
        else:
            messagebox.showwarning("Ошибка", "Очередь пуста!")
        self.refresh_display()

    def peek_item(self):
        if not self.queue:
            return
        val, success = self.queue.peek()
        if success:
            messagebox.showinfo("Первый элемент", f"Первый элемент: {val}")
        else:
            messagebox.showwarning("Ошибка", "Очередь пуста!")

    def fill_random(self):
        if not self.queue:
            return
        count = ask_integer_custom("Случайные", "Сколько элементов добавить?")
        if count is None:
            return
        minv = ask_integer_custom("Случайные", "Минимальное значение:")
        if minv is None:
            return
        maxv = ask_integer_custom("Случайные", "Максимальное значение:")
        if maxv is None:
            return
        if minv > maxv:
            messagebox.showerror("Ошибка", "Минимальное значение не может быть больше максимального")
            return
        self.queue.fill_random(count, minv, maxv)
        self.refresh_display()

    def exit_app(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QueueApp(root)
    root.mainloop()