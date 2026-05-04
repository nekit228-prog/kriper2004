import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("750x650")
        self.root.configure(bg='#f0f0f0')
        
        # Предопределённые задачи с типами
        self.default_tasks = [
            {"text": "Прочитать статью по Python", "type": "учёба"},
            {"text": "Сделать зарядку 15 минут", "type": "спорт"},
            {"text": "Закончить рабочий отчёт", "type": "работа"},
            {"text": "Изучить новый фреймворк", "type": "учёба"},
            {"text": "Пробежать 3 км", "type": "спорт"},
            {"text": "Провести совещание", "type": "работа"},
            {"text": "Посмотреть вебинар", "type": "учёба"},
            {"text": "Сделать 50 отжиманий", "type": "спорт"},
            {"text": "Ответить на письма", "type": "работа"},
            {"text": "Написать пост в блог", "type": "работа"},
            {"text": "Выучить 10 новых слов", "type": "учёба"},
            {"text": "Пойти на йогу", "type": "спорт"}
        ]
        
        # Загрузка данных
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения
        self.refresh_task_list()
        self.refresh_history()
        
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.tasks = data.get("tasks", self.default_tasks.copy())
                    self.history = data.get("history", [])
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.tasks = self.default_tasks.copy()
                self.history = []
        else:
            self.tasks = self.default_tasks.copy()
            self.history = []
            
    def save_data(self):
        """Сохранение данных в JSON файл"""
        data = {
            "tasks": self.tasks,
            "history": self.history
        }
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            
    def create_widgets(self):
        # Стили
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("Task.TLabel", font=("Arial", 12))
        
        # Заголовок
        title_label = ttk.Label(self.root, text="🎲 Генератор случайных задач", 
                                style="Title.TLabel")
        title_label.pack(pady=15)
        
        # Рамка генерации
        generate_frame = ttk.LabelFrame(self.root, text="Генерация задачи", padding=15)
        generate_frame.pack(fill="x", padx=15, pady=8)
        
        self.generate_btn = tk.Button(generate_frame, text="Сгенерировать задачу", 
                                     command=self.generate_task, 
                                     bg="#4CAF50", fg="white",
                                     font=("Arial", 12, "bold"), 
                                     padx=25, pady=8,
                                     cursor="hand2")
        self.generate_btn.pack(pady=5)
        
        self.current_task_label = tk.Label(generate_frame, text="", 
                                          font=("Arial", 13, "bold"),
                                          fg="#2196F3", 
                                          bg="white",
                                          wraplength=650,
                                          pady=10)
        self.current_task_label.pack(pady=8, fill="x")
        
        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтр по типу", padding=10)
        filter_frame.pack(fill="x", padx=15, pady=8)
        
        self.filter_var = tk.StringVar(value="все")
        filter_types = [("Все", "все"), ("📚 Учёба", "учёба"),
                        ("🏃 Спорт", "спорт"), ("💼 Работа", "работа")]
        
        for text, value in filter_types:
            rb = tk.Radiobutton(filter_frame, text=text, 
                               variable=self.filter_var, 
                               value=value,
                               command=self.refresh_task_list,
                               bg="#f0f0f0",
                               font=("Arial", 10))
            rb.pack(side="left", padx=15)
            
        # Рамка списка задач
        tasks_frame = ttk.LabelFrame(self.root, text="Доступные задачи", padding=10)
        tasks_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Создание фрейма с прокруткой
        tasks_scroll_frame = tk.Frame(tasks_frame)
        tasks_scroll_frame.pack(fill="both", expand=True)
        
        tasks_scrollbar = tk.Scrollbar(tasks_scroll_frame)
        tasks_scrollbar.pack(side="right", fill="y")
        
        self.tasks_listbox = tk.Listbox(tasks_scroll_frame, 
                                       yscrollcommand=tasks_scrollbar.set,
                                       height=6, 
                                       font=("Arial", 10),
                                       selectmode=tk.SINGLE)
        self.tasks_listbox.pack(fill="both", expand=True)
        tasks_scrollbar.config(command=self.tasks_listbox.yview)
        
        # Рамка добавления задачи
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=12)
        add_frame.pack(fill="x", padx=15, pady=8)
        
        # Текст задачи
        tk.Label(add_frame, text="Текст задачи:", font=("Arial", 10), 
                bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.task_entry = tk.Entry(add_frame, width=55, font=("Arial", 10))
        self.task_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Тип задачи
        tk.Label(add_frame, text="Тип задачи:", font=("Arial", 10), 
                bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar(value="учёба")
        type_menu = ttk.Combobox(add_frame, textvariable=self.type_var, 
                                 values=["учёба", "спорт", "работа"], 
                                 state="readonly",
                                 width=20)
        type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Кнопка добавления
        add_btn = tk.Button(add_frame, text="➕ Добавить задачу", 
                           command=self.add_task,
                           bg="#FF9800", fg="white", 
                           font=("Arial", 10, "bold"),
                           padx=20,
                           cursor="hand2")
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Рамка истории
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Кнопки управления историей
        history_buttons_frame = tk.Frame(history_frame, bg="#f0f0f0")
        history_buttons_frame.pack(fill="x", pady=5)
        
        clear_history_btn = tk.Button(history_buttons_frame, 
                                     text="🗑 Очистить историю", 
                                     command=self.clear_history, 
                                     bg="#f44336", 
                                     fg="white",
                                     font=("Arial", 9),
                                     cursor="hand2")
        clear_history_btn.pack(side="left", padx=5)
        
        export_btn = tk.Button(history_buttons_frame,
                              text="💾 Экспорт истории",
                              command=self.export_history,
                              bg="#2196F3",
                              fg="white",
                              font=("Arial", 9),
                              cursor="hand2")
        export_btn.pack(side="left", padx=5)
        # Список истории с прокруткой
        history_scroll_frame = tk.Frame(history_frame)
        history_scroll_frame.pack(fill="both", expand=True)
        
        history_scrollbar = tk.Scrollbar(history_scroll_frame)
        history_scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(history_scroll_frame, 
                                         yscrollcommand=history_scrollbar.set,
                                         height=8, 
                                         font=("Arial", 10),
                                         fg="#333")
        self.history_listbox.pack(fill="both", expand=True)
        history_scrollbar.config(command=self.history_listbox.yview)
        
    def refresh_task_list(self):
        """Обновление списка задач с учётом фильтра"""
        self.tasks_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        
        for i, task in enumerate(self.tasks, 1):
            if filter_type == "все" or task["type"] == filter_type:
                display_text = f"{i:2d}. {task['text']} [{task['type']}]"
                self.tasks_listbox.insert(tk.END, display_text)
                
    def refresh_history(self):
        """Обновление списка истории"""
        self.history_listbox.delete(0, tk.END)
        for i, task in enumerate(reversed(self.history), 1):
            self.history_listbox.insert(tk.END, f"{i:2d}. {task}")
            
    def generate_task(self):
        """Генерация случайной задачи"""
        if not self.tasks:
            messagebox.showwarning("Нет задач", 
                                  "Список задач пуст! Добавьте хотя бы одну задачу.")
            return
            
        # Фильтрация задач по текущему фильтру
        filter_type = self.filter_var.get()
        if filter_type == "все":
            available_tasks = self.tasks
        else:
            available_tasks = [task for task in self.tasks if task["type"] == filter_type]
            
        if not available_tasks:
            messagebox.showwarning("Нет задач", 
                                  f"Нет задач типа '{filter_type}'. Измените фильтр или добавьте задачи.")
            return
            
        task = random.choice(available_tasks)
        self.current_task_label.config(text=f"🎯 Ваша задача: {task['text']} ({task['type']})")
        self.history.append(task['text'])
        self.save_data()
        self.refresh_history()
        
        # Анимация кнопки
        self.generate_btn.config(bg="#45a049")
        self.root.after(100, lambda: self.generate_btn.config(bg="#4CAF50"))
        
    def add_task(self):
        """Добавление новой задачи с проверкой ввода"""
        task_text = self.task_entry.get().strip()
        task_type = self.type_var.get()
        
        # Проверка на пустую строку
        if not task_text:
            messagebox.showerror("Ошибка", "❌ Текст задачи не может быть пустым!")
            return
            
        # Проверка на минимальную длину
        if len(task_text) < 3:
            messagebox.showerror("Ошибка", "❌ Текст задачи должен содержать минимум 3 символа!")
            return
            
        # Проверка на дубликат
        for task in self.tasks:
            if task["text"].lower() == task_text.lower():
                messagebox.showerror("Ошибка", "❌ Такая задача уже существует!")
                return
            
        # Добавление задачи
        self.tasks.append({"text": task_text, "type": task_type})
        self.save_data()
        self.refresh_task_list()
        
        # Очистка поля ввода
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"✅ Задача '{task_text}' успешно добавлена!")
        
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", 
                              "Вы уверены, что хотите очистить всю историю?\nЭто действие нельзя отменить."):
            self.history = []
            self.save_data()
            self.refresh_history()
            self.current_task_label

            config(text="")
            messagebox.showinfo("Успех", "✅ История успешно очищена!")
            
    def export_history(self):
        """Экспорт истории в файл"""
        if not self.history:
            messagebox.showwarning("Нет данных", "История пуста. Нечего экспортировать.")
            return
            
        from datetime import datetime
        filename = f"history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("История сгенерированных задач\n")
            f.write("=" * 50 + "\n")
            for i, task in enumerate(self.history, 1):
                f.write(f"{i}. {task}\n")
                
        messagebox.showinfo("Успех", f"✅ История экспортирована в файл:\n{filename}")

if name == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()