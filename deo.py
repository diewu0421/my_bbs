import tkinter as tk

def on_button_click():
    label.config(text="Hello, Tkinter!")

root = tk.Tk()
root.title("Grid布局示例")

# 添加标签和按钮
label = tk.Label(root, text="Hello, World!")
label.grid(row=0, column=0)

button = tk.Button(root, text="Click Me", command=on_button_click)
button.grid(row=1, column=0)

root.mainloop()
