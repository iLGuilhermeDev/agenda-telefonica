import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- Banco de dados ---
DB_FILE = "agenda.db"

def conectar_banco():
    return sqlite3.connect(DB_FILE)

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def adicionar_contato(nome, telefone, email):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contatos (nome, telefone, email)
        VALUES (?, ?, ?)
    """, (nome, telefone, email))
    conn.commit()
    conn.close()

def listar_contatos():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, email FROM contatos ORDER BY nome")
    contatos = cursor.fetchall()
    conn.close()
    return contatos

def buscar_contato(termo):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, telefone, email FROM contatos
        WHERE nome LIKE ? ORDER BY nome
    """, (f"%{termo}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def atualizar_contato(id_contato, novo_nome, novo_telefone, novo_email):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contatos
        SET nome = ?, telefone = ?, email = ?
        WHERE id = ?
    """, (novo_nome, novo_telefone, novo_email, id_contato))
    conn.commit()
    atualizado = cursor.rowcount > 0
    conn.close()
    return atualizado

def remover_contato(id_contato):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))
    conn.commit()
    removido = cursor.rowcount > 0
    conn.close()
    return removido

# --- Interface gráfica (Tkinter) ---
class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contatos")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Frame para entrada de dados
        frame_form = tk.Frame(root, padx=10, pady=10)
        frame_form.pack(fill="x")

        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Telefone:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_telefone = tk.Entry(frame_form, width=30)
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="E-mail:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_email = tk.Entry(frame_form, width=30)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        # Frame para botões de ação
        frame_botoes = tk.Frame(root, padx=10, pady=5)
        frame_botoes.pack(fill="x")

        self.btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=self.adicionar, width=12)
        self.btn_adicionar.pack(side="left", padx=5)

        self.btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=self.atualizar, width=12, state="disabled")
        self.btn_atualizar.pack(side="left", padx=5)

        self.btn_remover = tk.Button(frame_botoes, text="Remover", command=self.remover, width=12, state="disabled")
        self.btn_remover.pack(side="left", padx=5)

        self.btn_limpar = tk.Button(frame_botoes, text="Limpar campos", command=self.limpar_campos, width=12)
        self.btn_limpar.pack(side="left", padx=5)

        # Frame para busca
        frame_busca = tk.Frame(root, padx=10, pady=5)
        frame_busca.pack(fill="x")

        tk.Label(frame_busca, text="Buscar por nome:").pack(side="left", padx=5)
        self.entry_busca = tk.Entry(frame_busca, width=30)
        self.entry_busca.pack(side="left", padx=5)
        self.btn_buscar = tk.Button(frame_busca, text="Buscar", command=self.buscar, width=8)
        self.btn_buscar.pack(side="left", padx=5)
        self.btn_mostrar_todos = tk.Button(frame_busca, text="Mostrar todos", command=self.carregar_contatos, width=12)
        self.btn_mostrar_todos.pack(side="left", padx=5)

        # Treeview para exibir os contatos
        frame_tree = tk.Frame(root, padx=10, pady=5)
        frame_tree.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tree, columns=("id", "nome", "telefone", "email"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("email", text="E-mail")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=200)
        self.tree.column("telefone", width=120)
        self.tree.column("email", width=200)

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind para selecionar um contato da lista
        self.tree.bind("<<TreeviewSelect>>", self.on_selecionar)

        # Variável para armazenar o ID do contato selecionado
        self.id_selecionado = None

        # Carrega os contatos ao iniciar
        self.carregar_contatos()

    def carregar_contatos(self):
        """Limpa a treeview e carrega todos os contatos do banco."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        contatos = listar_contatos()
        for contato in contatos:
            self.tree.insert("", "end", values=contato)

    def buscar(self):
        """Busca contatos pelo nome e exibe no treeview."""
        termo = self.entry_busca.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um nome para buscar.")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        resultados = buscar_contato(termo)
        if resultados:
            for contato in resultados:
                self.tree.insert("", "end", values=contato)
        else:
            messagebox.showinfo("Busca", "Nenhum contato encontrado.")
            # Opcional: recarregar todos? Deixamos a lista vazia ou recarregamos todos
            # Vamos recarregar todos para não ficar vazio
            self.carregar_contatos()

    def adicionar(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome é obrigatório.")
            return
        try:
            adicionar_contato(nome, telefone, email)
            messagebox.showinfo("Sucesso", f"Contato '{nome}' adicionado!")
            self.limpar_campos()
            self.carregar_contatos()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar: {e}")

    def on_selecionar(self, event):
        """Quando um contato é selecionado na treeview, preenche os campos e habilita botões."""
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        valores = item["values"]
        if valores:
            self.id_selecionado = valores[0]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, valores[1])
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, valores[2] if valores[2] else "")
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, valores[3] if valores[3] else "")
            # Habilita botões de atualizar e remover
            self.btn_atualizar.config(state="normal")
            self.btn_remover.config(state="normal")
            # Desabilita adicionar enquanto edita? Não é necessário, mas pode-se deixar ambos ativos.
            # O usuário pode clicar em adicionar com campos preenchidos, isso não é um problema.

    def limpar_campos(self):
        self.id_selecionado = None
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.btn_atualizar.config(state="disabled")
        self.btn_remover.config(state="disabled")
        # Limpa a seleção na treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def atualizar(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um contato para atualizar.")
            return
        novo_nome = self.entry_nome.get().strip()
        novo_telefone = self.entry_telefone.get().strip()
        novo_email = self.entry_email.get().strip()
        if not novo_nome:
            messagebox.showerror("Erro", "O nome não pode ficar vazio.")
            return
        try:
            if atualizar_contato(self.id_selecionado, novo_nome, novo_telefone, novo_email):
                messagebox.showinfo("Sucesso", "Contato atualizado!")
                self.limpar_campos()
                self.carregar_contatos()
            else:
                messagebox.showerror("Erro", "Contato não encontrado para atualizar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

    def remover(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um contato para remover.")
            return
        # Pega o nome para exibir confirmação
        nome = self.entry_nome.get().strip()
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover '{nome}'?"):
            try:
                if remover_contato(self.id_selecionado):
                    messagebox.showinfo("Sucesso", "Contato removido!")
                    self.limpar_campos()
                    self.carregar_contatos()
                else:
                    messagebox.showerror("Erro", "Falha ao remover contato.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover: {e}")

# --- Inicialização ---
if __name__ == "__main__":
    criar_tabela()  # Garante que a tabela existe
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()