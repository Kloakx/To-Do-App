import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List Application")

        # Connect to SQLite database (will create it if it doesn't exist)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        
        # Create table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                task TEXT)''')
        self.conn.commit()

        # Create GUI elements
        self.task_entry = tk.Entry(master, width=40, font=("Helvetica", 14))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(master, text="Add Task", width=20, font=("Helvetica", 14), command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(master, text="Delete Task", width=20, font=("Helvetica", 14), command=self.delete_task)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.tasks_listbox = tk.Listbox(master, width=50, height=10, font=("Helvetica", 12))
        self.tasks_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the database and display in Listbox."""
        self.tasks_listbox.delete(0, tk.END)  # Clear the listbox
        self.cursor.execute('SELECT * FROM tasks')
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, task[1])

    def add_task(self):
        """Add a new task to the database."""
        task = self.task_entry.get()
        if task:
            self.cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            self.conn.commit()
            self.load_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        """Delete the selected task from the database."""
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            task_id = selected_task[0] + 1  # Index is zero-based, but ID starts from 1
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
