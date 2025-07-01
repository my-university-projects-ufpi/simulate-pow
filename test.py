import tkinter as tk

def start():
    print("Botão clicado!")

root = tk.Tk()
btn = tk.Button(root, text="Clique", command=start)
btn.pack()
root.mainloop()
