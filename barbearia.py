import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta

# Conexão com o banco de dados
conexao = sqlite3.connect('barbearia.db')
cursor = conexao.cursor()

# Criação das tabelas
def criar_tabelas():
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        preferencias TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS barbeiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especialidades TEXT,
        disponibilidade TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTCREMENT,
        cliente_id INTEGER,
        barbeiro_id INTEGER,
        data_horario TEXT NOT NULL,
        servico TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (barbeiro_id) REFERENCES barbeiros (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS financeiro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL NOT NULL,
        descricao TEXT NOT NULL,
        barbeiro_id INTEGER,
        FOREIGN KEY (barbeiro_id) REFERENCES barbeiros (id)
    )''')
    conexao.commit()

# Funções
def cadastrar_cliente():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    preferencias = entry_preferencias.get()

    if nome.strip():
        cursor.execute('INSERT INTO clientes (nome, telefone, preferencias) VALUES (?, ?, ?)',
                       (nome, telefone, preferencias))
        conexao.commit()
        messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado!")
        limpar_campos_cliente()
    else:
        messagebox.showwarning("Erro", "O campo 'Nome' é obrigatório!")

def cadastrar_barbeiro():
    nome = entry_nome_barbeiro.get()
    especialidades = entry_especialidades.get()
    disponibilidade = entry_disponibilidade.get()

    if nome.strip():
        cursor.execute('INSERT INTO barbeiros (nome, especialidades, disponibilidade) VALUES (?, ?, ?)',
                       (nome, especialidades, disponibilidade))
        conexao.commit()
        messagebox.showinfo("Sucesso", f"Barbeiro {nome} cadastrado!")
        limpar_campos_barbeiro()
    else:
        messagebox.showwarning("Erro", "O campo 'Nome' é obrigatório!")

def agendar_servico():
    try:
        cliente_id = int(entry_cliente_id.get())
        barbeiro_id = int(entry_barbeiro_id.get())
        data_horario = entry_data_horario.get()
        servico = entry_servico.get()

        # Validação de formato de data
        datetime.strptime(data_horario, '%Y-%m-%d %H:%M')

        if servico.strip():
            cursor.execute('INSERT INTO agendamentos (cliente_id, barbeiro_id, data_horario, servico) VALUES (?, ?, ?, ?)',
                           (cliente_id, barbeiro_id, data_horario, servico))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Serviço agendado!")
            limpar_campos_agendamento()
        else:
            messagebox.showwarning("Erro", "O campo 'Serviço' é obrigatório!")
    except ValueError:
        messagebox.showerror("Erro", "Data e hora inválidas! Use o formato aaaa-mm-dd hh:mm.")

def listar_agendamentos():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    cursor.execute("SELECT * FROM agendamentos WHERE data_horario BETWEEN ? AND ?",
                   (inicio_semana.strftime('%Y-%m-%d 00:00:00'), fim_semana.strftime('%Y-%m-%d 23:59:59')))

    resultados = cursor.fetchall()
    if not resultados:
        messagebox.showinfo("Listagem", "Nenhum agendamento encontrado para a semana.")
    else:
        for agendamento in resultados:
            print(agendamento)  # Substituir por exibição em interface gráfica

# Funções de limpeza de campos
def limpar_campos_cliente():
    entry_nome.delete(0, END)
    entry_telefone.delete(0, END)
    entry_preferencias.delete(0, END)

def limpar_campos_barbeiro():
    entry_nome_barbeiro.delete(0, END)
    entry_especialidades.delete(0, END)
    entry_disponibilidade.delete(0, END)

def limpar_campos_agendamento():
    entry_cliente_id.delete(0, END)
    entry_barbeiro_id.delete(0, END)
    entry_data_horario.delete(0, END)
    entry_servico.delete(0, END)

# Interface gráfica
root = Tk()
root.title("Estilo Nobre - Sistema de Gestão")
root.geometry("800x600")

# Inicializa as tabelas
criar_tabelas()

# Tab de Cadastro
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

aba_cadastro = Frame(notebook)
notebook.add(aba_cadastro, text="Cadastro")

Label(aba_cadastro, text="Cadastro de Clientes").grid(row=0, column=0, columnspan=2)
Label(aba_cadastro, text="Nome").grid(row=1, column=0)
entry_nome = Entry(aba_cadastro)
entry_nome.grid(row=1, column=1)

Button(aba_cadastro, text="Cadastrar Cliente", command=cadastrar_cliente).grid(row=2, column=0, columnspan=2)

root.mainloop()
