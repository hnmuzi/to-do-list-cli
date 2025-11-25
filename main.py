import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import pandas as pd

FILE_NAME = "tasks.json"

# ===================== Fungsi Membaca dan Menyimpan =====================
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# ===================== Fungsi GUI =====================
def refresh_listbox(filter_status="All"):
    listbox.delete(0, tk.END)
    display_index = 0
    for i, task in enumerate(tasks):
        # Filter
        if filter_status == "Done" and not task["done"]:
            continue
        if filter_status == "Pending" and task["done"]:
            continue
        status = "✓" if task["done"] else "✗"
        listbox.insert(tk.END, f"{status} {task['title']}")
        listbox.itemconfig(display_index, fg="green" if task["done"] else "red")
        display_index += 1

def add_task():
    title = entry_task.get().strip()
    if title == "":
        messagebox.showwarning("Peringatan", "Nama tugas tidak boleh kosong!")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    entry_task.delete(0, tk.END)
    refresh_listbox(filter_var.get())

def mark_done():
    try:
        index = listbox.curselection()[0]
        real_index = get_real_index(index)
        tasks[real_index]["done"] = True
        save_tasks(tasks)
        refresh_listbox(filter_var.get())
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih tugas terlebih dahulu!")

def delete_task():
    try:
        index = listbox.curselection()[0]
        real_index = get_real_index(index)
        tasks.pop(real_index)
        save_tasks(tasks)
        refresh_listbox(filter_var.get())
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih tugas terlebih dahulu!")

def get_real_index(listbox_index):
    """Mapping index dari filtered listbox ke tasks asli"""
    count = -1
    for i, task in enumerate(tasks):
        if filter_var.get() == "Done" and not task["done"]:
            continue
        if filter_var.get() == "Pending" and task["done"]:
            continue
        count += 1
        if count == listbox_index:
            return i
    return -1

def export_excel():
    if not tasks:
        messagebox.showinfo("Info", "Tidak ada data untuk diexport.")
        return
    df = pd.DataFrame(tasks)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files","*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukses", f"Data berhasil diexport ke {file_path}")

def apply_filter():
    refresh_listbox(filter_var.get())

# ===================== Main App =====================
tasks = load_tasks()

root = tk.Tk()
root.title("To-Do List")
root.geometry("450x550")

# Judul
label_title = tk.Label(root, text="My To-Do List", font=("Arial", 20))
label_title.pack(pady=10)

# Entry untuk tugas baru
entry_task = tk.Entry(root, font=("Arial", 14))
entry_task.pack(pady=10, padx=20, fill=tk.X)

# Tombol aksi
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

btn_add = tk.Button(frame_buttons, text="Tambah Tugas", command=add_task,
                    width=15, bg="#4CAF50", fg="white")
btn_add.grid(row=0, column=0, padx=5)

btn_done = tk.Button(frame_buttons, text="Tandai Selesai", command=mark_done,
                     width=15, bg="#2196F3", fg="white")
btn_done.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(frame_buttons, text="Hapus Tugas", command=delete_task,
                       width=15, bg="#f44336", fg="white")
btn_delete.grid(row=1, column=0, padx=5, pady=5)

btn_export = tk.Button(frame_buttons, text="Export ke Excel", command=export_excel,
                       width=15, bg="#9C27B0", fg="white")
btn_export.grid(row=1, column=1, padx=5, pady=5)

# Filter tugas
filter_var = tk.StringVar(value="All")
frame_filter = tk.Frame(root)
frame_filter.pack(pady=5)

tk.Label(frame_filter, text="Filter :", font=("Arial", 12)).pack(side=tk.LEFT)
tk.Radiobutton(frame_filter, text="Semua", variable=filter_var,
               value="All", command=apply_filter).pack(side=tk.LEFT)
tk.Radiobutton(frame_filter, text="Belum Selesai", variable=filter_var,
               value="Pending", command=apply_filter).pack(side=tk.LEFT)
tk.Radiobutton(frame_filter, text="Selesai", variable=filter_var,
               value="Done", command=apply_filter).pack(side=tk.LEFT)

# Listbox menampilkan semua tugas
listbox = tk.Listbox(root, font=("Arial", 14), selectmode=tk.SINGLE)
listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(listbox)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

refresh_listbox()
root.mainloop()
