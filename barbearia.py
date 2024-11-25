import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta

conexao = sqlite3.connect('barbearia.db')
cursor = conexao.cursor()

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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        barbeiro_id INTEGER,
        data_horario TEXT,
        servico TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (barbeiro_id) REFERENCES barbeiros (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS financeiro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL NOT NULL,
        descricao TEXT,
        barbeiro_id INTEGER,
        FOREIGN KEY (barbeiro_id) REFERENCES barbeiros (id)
    )''')
    conexao.commit()

def cadastrar_cliente():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    preferencias = entry_preferencias.get()
    
    # Bug 1: Não valida se o telefone está vazio
    if nome:
        cursor.execute('INSERT INTO clientes (nome, telefone, preferencias) VALUES (?, ?, ?)', 
                       (nome, telefone, preferencias))
        conexao.commit()
        messagebox.showinfo("Cadastro", f"Cliente {nome} cadastrado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Nome do cliente é obrigatório!")
    limpar_campos_cliente()

def agendar_servico():
    cliente_id = entry_cliente_id.get()
    barbeiro_id = entry_barbeiro_id.get()
    data_horario = entry_data_horario.get()
    servico = entry_servico.get()
    
    # Bug 2: Insere data padrão incorreta se campo de data estiver vazio
    if not data_horario:
        data_horario = "2024-13-01 00:00:00"  # Data inválida
    
    if cliente_id and barbeiro_id and servico:
        cursor.execute('INSERT INTO agendamentos (cliente_id, barbeiro_id, data_horario, servico) VALUES (?, ?, ?, ?)', 
                       (cliente_id, barbeiro_id, data_horario, servico))
        conexao.commit()
        messagebox.showinfo("Agendamento", "Serviço agendado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
    limpar_campos_agendamento()

def relatorio_financeiro():
    janela_relatorio = Toplevel()
    janela_relatorio.title("Relatório Financeiro")
    janela_relatorio.geometry("400x300")

    tree = ttk.Treeview(janela_relatorio, columns=("ID", "Valor", "Descrição", "Barbeiro ID", "Total"), show="headings")
    # Bug 5: A coluna "Total" não existe no banco
    tree.heading("ID", text="ID")
    tree.heading("Valor", text="Valor")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Barbeiro ID", text="Barbeiro ID")
    tree.heading("Total", text="Total")  # Coluna inválida
    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT * FROM financeiro")
    for nota in cursor.fetchall():
        tree.insert("", "end", values=nota)

def listar_agendamentos():
    janela_agendamentos = Toplevel()
    janela_agendamentos.title("Agendamentos da Semana")
    janela_agendamentos.geometry("600x400")

    tree = ttk.Treeview(janela_agendamentos, columns=("ID", "Cliente ID", "Barbeiro ID", "Data e Horário", "Serviço"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Cliente ID", text="Cliente ID")
    tree.heading("Barbeiro ID", text="Barbeiro ID")
    tree.heading("Data e Horário", text="Data e Horário")
    tree.heading("Serviço", text="Serviço")
    tree.pack(fill=BOTH, expand=True)

    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    # Bug 3: Formato de data com erro
    cursor.execute("SELECT * FROM agendamentos WHERE data_horario BETWEEN ? AND ?", 
                   (inicio_semana.strftime('%Y/%m/%d 00:00:00'), fim_semana.strftime('%Y/%m/%d 23:59:59')))
    
    for agendamento in cursor.fetchall():
        tree.insert("", "end", values=agendamento)

def emitir_nota():
    valor = entry_valor.get()
    descricao = entry_descricao_nota.get()
    barbeiro_id = entry_barbeiro_id_nota.get()
    
    # Bug 4: Tratamento incorreto do ID do barbeiro
    if valor and descricao and barbeiro_id:
        cursor.execute('INSERT INTO financeiro (valor, descricao, barbeiro_id) VALUES (?, ?, ?)', 
                       (float(valor), descricao, barbeiro_id))  # barbeiro_id como texto
        conexao.commit()
        messagebox.showinfo("Emissão de Nota", "Nota emitida com sucesso!")
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
    limpar_campos_financeiro()

root.mainloop()
