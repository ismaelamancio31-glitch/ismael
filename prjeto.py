import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------------- BANCO DE DADOS ---------------- #

conexao = sqlite3.connect("clientes.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    endereco TEXT NOT NULL
)
""")
conexao.commit()


# ---------------- FUNÇÕES ---------------- #

def cadastrar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    if not nome or not email or not telefone or not endereco:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, endereco)
        VALUES (?, ?, ?, ?)
    """, (nome, email, telefone, endereco))
    conexao.commit()

    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cliente cadastrado!")


def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM clientes")
    for cliente in cursor.fetchall():
        tree.insert("", "end", values=cliente)


def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)


def editar_cliente():
    try:
        item = tree.selection()[0]
        cliente = tree.item(item, "values")
    except:
        messagebox.showwarning("Atenção", "Selecione um cliente!")
        return

    cliente_id = cliente[0]

    novo_nome = simpledialog.askstring("Editar", "Nome:", initialvalue=cliente[1])
    novo_email = simpledialog.askstring("Editar", "Email:", initialvalue=cliente[2])
    novo_telefone = simpledialog.askstring("Editar", "Telefone:", initialvalue=cliente[3])
    novo_endereco = simpledialog.askstring("Editar", "Endereço:", initialvalue=cliente[4])

    if novo_nome and novo_email and novo_telefone and novo_endereco:
        cursor.execute("""
            UPDATE clientes SET nome=?, email=?, telefone=?, endereco=? WHERE id=?
        """, (novo_nome, novo_email, novo_telefone, novo_endereco, cliente_id))
        conexao.commit()

        atualizar_lista()
        messagebox.showinfo("Sucesso", "Cliente atualizado!")


def excluir_cliente():
    try:
        item = tree.selection()[0]
        cliente = tree.item(item, "values")
        cliente_id = cliente[0]
    except:
        messagebox.showwarning("Atenção", "Selecione um cliente!")
        return

    confirmacao = messagebox.askyesno("Confirmar", "Excluir este cliente?")

    if confirmacao:
        cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        conexao.commit()
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Cliente excluído!")


# ---------------- INTERFACE GRÁFICA ---------------- #

janela = tk.Tk()
janela.title("Cadastro de Clientes - Tema Escuro")
janela.geometry("750x520")
janela.configure(bg="#1E1E1E")  # fundo escuro


# ---------------- TEMA ESCURO / ESTILOS ---------------- #

style = ttk.Style()
style.theme_use("clam")

style.configure("Dark.TEntry",
                fieldbackground="#2D2D2D",
                background="#2D2D2D",
                foreground="white")

style.configure("Dark.Treeview",
                background="#2D2D2D",
                foreground="white",
                fieldbackground="#2D2D2D",
                rowheight=25)

style.map("Dark.Treeview",
          background=[("selected", "#007ACC")],
          foreground=[("selected", "white")])

style.configure("Title.TLabel",
                font=("Arial", 20, "bold"),
                background="#1E1E1E",
                foreground="white")

style.configure("Label.TLabel",
                font=("Arial", 12),
                background="#1E1E1E",
                foreground="white")

style.configure("Green.TButton",
                background="#28A745",
                foreground="white",
                font=("Arial", 11, "bold"))
style.map("Green.TButton",
          background=[("active", "#218838")])

style.configure("Blue.TButton",
                background="#007BFF",
                foreground="white",
                font=("Arial", 11, "bold"))
style.map("Blue.TButton",
          background=[("active", "#0069D9")])

style.configure("Red.TButton",
                background="#DC3545",
                foreground="white",
                font=("Arial", 11, "bold"))
style.map("Red.TButton",
          background=[("active", "#C82333")])


# ---------------- LAYOUT ---------------- #

titulo = ttk.Label(janela, text="Sistema de Cadastro de Clientes", style="Title.TLabel")
titulo.pack(pady=10)

frame_form = tk.Frame(janela, bg="#1E1E1E")
frame_form.pack(pady=10)

labels = ["Nome", "Email", "Telefone", "Endereço"]
entries = []

for label_text in labels:
    frame_linha = tk.Frame(frame_form, bg="#1E1E1E")
    frame_linha.pack(fill="x", pady=5)

    label = ttk.Label(frame_linha, text=label_text + ":", style="Label.TLabel")
    label.pack(side="left", padx=10)

    entry = ttk.Entry(frame_linha, width=60, style="Dark.TEntry")
    entry.pack(side="left", padx=10)
    entries.append(entry)

entry_nome, entry_email, entry_telefone, entry_endereco = entries

# Botão cadastrar (verde)
btn_cadastrar = ttk.Button(janela, text="Cadastrar Cliente",
                           style="Green.TButton", command=cadastrar_cliente)
btn_cadastrar.pack(pady=10)

# Tabela escura
tree_frame = tk.Frame(janela, bg="#1E1E1E")
tree_frame.pack()

colunas = ("ID", "Nome", "Email", "Telefone", "Endereço")
tree = ttk.Treeview(tree_frame, columns=colunas, show="headings",
                    height=10, style="Dark.Treeview")

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.pack()

# Botões coloridos
frame_btns = tk.Frame(janela, bg="#1E1E1E")
frame_btns.pack(pady=15)

btn_editar = ttk.Button(frame_btns, text="Editar Cliente",
                        style="Blue.TButton", command=editar_cliente)
btn_editar.grid(row=0, column=0, padx=15)

btn_excluir = ttk.Button(frame_btns, text="Excluir Cliente",
                         style="Red.TButton", command=excluir_cliente)
btn_excluir.grid(row=0, column=1, padx=15)

atualizar_lista()

janela.mainloop()
