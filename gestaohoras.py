import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv
from datetime import datetime
import os

# Função para garantir que o arquivo CSV exista e tenha cabeçalhos
def garantir_criar_csv(nome_arquivo, cabecalho):
    if not os.path.exists(nome_arquivo):  # Se o arquivo não existir
        with open(nome_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(cabecalho)  # Cria o cabeçalho

# Função para registrar as horas de trabalho e o local
def registrar_horas(nome, horas, local):
    garantir_criar_csv('registro_horas.csv', ['Nome', 'Data', 'Horas Trabalhadas', 'Local'])  # Cria o CSV se necessário
    with open('registro_horas.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nome, datetime.today().strftime('%Y-%m-%d'), horas, local])

# Função para registrar um trabalhador e salvar no CSV
def registrar_trabalhador(trabalhadores):
    nome = simpledialog.askstring("Registrar Trabalhador", "Digite o nome do trabalhador:")
    if nome not in trabalhadores:
        trabalhadores.append(nome)
        garantir_criar_csv('trabalhadores.csv', ['Nome'])  # Cria o CSV se necessário
        with open('trabalhadores.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nome])
        messagebox.showinfo("Sucesso", f"Trabalhador {nome} registrado com sucesso!")
    else:
        messagebox.showwarning("Atenção", f"Trabalhador {nome} já está registrado!")

# Função para registrar uma obra e salvar no CSV
def registrar_obra(obras):
    local = simpledialog.askstring("Registrar Obra", "Digite o nome da obra:")
    if local not in obras:
        obras.append(local)
        garantir_criar_csv('obras.csv', ['Local'])  # Cria o CSV se necessário
        with open('obras.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([local])
        messagebox.showinfo("Sucesso", f"Obra {local} registrada com sucesso!")
    else:
        messagebox.showwarning("Atenção", f"Obra {local} já está registrada!")

# Função para carregar trabalhadores do CSV
def carregar_trabalhadores():
    trabalhadores = []
    if os.path.exists('trabalhadores.csv'):  # Verifica se o arquivo existe
        with open('trabalhadores.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                trabalhadores.append(row[0])
    return trabalhadores

# Função para carregar obras do CSV
def carregar_obras():
    obras = []
    if os.path.exists('obras.csv'):  # Verifica se o arquivo existe
        with open('obras.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                obras.append(row[0])
    return obras

# Função para calcular as horas trabalhadas de um empregado em um mês
def horas_trabalhadas_empregado(nome, mes, ano):
    total_horas = 0
    if os.path.exists('registro_horas.csv'):  # Verifica se o arquivo existe
        with open('registro_horas.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                data = datetime.strptime(row[1], '%Y-%m-%d')
                if row[0].lower() == nome.lower() and data.month == mes and data.year == ano:
                    total_horas += float(row[2])  # Soma as horas trabalhadas
    return total_horas

# Função para calcular as horas trabalhadas em uma obra em um mês
def horas_trabalhadas_obra(local, mes, ano):
    total_horas = 0
    if os.path.exists('registro_horas.csv'):  # Verifica se o arquivo existe
        with open('registro_horas.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                data = datetime.strptime(row[1], '%Y-%m-%d')
                if row[3].lower() == local.lower() and data.month == mes and data.year == ano:
                    total_horas += float(row[2])  # Soma as horas trabalhadas
    return total_horas

# Função para criar a interface gráfica
def criar_interface():
    # Carregar trabalhadores e obras
    trabalhadores = carregar_trabalhadores()
    obras = carregar_obras()

    # Criando a janela principal
    root = tk.Tk()
    root.title("Registro de Horas de Trabalho")
    root.config(bg="#363636")

    # Obtendo as dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Definindo o tamanho da janela
    window_width = 500
    window_height = 500

    # Calculando as coordenadas para centralizar a janela
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Definindo o tamanho e a posição da janela
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
    # Estilo
    font = ("Arial", 12)
    label_color = "white"
    button_color = "#1E90FF"
    button_hover_color = "#45a049"
    error_color = "red"
    
    # Função para registrar horas
    def registrar_horas_gui():
        if not trabalhadores or not obras:
            messagebox.showwarning("Atenção", "Antes de registrar horas, adicione trabalhadores e obras.")
            return
        nome = simpledialog.askstring("Registrar Horas", "Digite o nome do trabalhador:")
        if nome not in trabalhadores:
            messagebox.showwarning("Atenção", "Trabalhador não encontrado!")
            return
        local = simpledialog.askstring("Registrar Horas", "Digite o local de trabalho (obra):")
        if local not in obras:
            messagebox.showwarning("Atenção", "Obra não encontrada!")
            return
        horas = simpledialog.askfloat("Registrar Horas", "Horas trabalhadas:")
        registrar_horas(nome, horas, local)
        messagebox.showinfo("Sucesso", "Horas registradas com sucesso!")

    # Função para registrar trabalhador
    def registrar_trabalhador_gui():
        registrar_trabalhador(trabalhadores)

    # Função para registrar obra
    def registrar_obra_gui():
        registrar_obra(obras)

    # Função para calcular horas trabalhadas por empregado
    def horas_trabalhadas_empregado_gui():
        nome = simpledialog.askstring("Horas Trabalhadas", "Digite o nome do empregado:")
        if nome not in trabalhadores:
            messagebox.showwarning("Atenção", "Trabalhador não encontrado!")
            return
        mes = simpledialog.askinteger("Horas Trabalhadas", "Digite o mês (1-12):")
        ano = simpledialog.askinteger("Horas Trabalhadas", "Digite o ano:")
        total_horas = horas_trabalhadas_empregado(nome, mes, ano)
        messagebox.showinfo("Horas Trabalhadas", f"{nome} trabalhou {total_horas} horas em {mes}/{ano}.")

    # Função para calcular horas trabalhadas em uma obra
    def horas_trabalhadas_obra_gui():
        local = simpledialog.askstring("Horas Trabalhadas", "Digite o local de trabalho:")
        if local not in obras:
            messagebox.showwarning("Atenção", "Obra não encontrada!")
            return
        mes = simpledialog.askinteger("Horas Trabalhadas", "Digite o mês (1-12):")
        ano = simpledialog.askinteger("Horas Trabalhadas", "Digite o ano:")
        total_horas = horas_trabalhadas_obra(local, mes, ano)
        messagebox.showinfo("Horas Trabalhadas", f"Foram trabalhadas {total_horas} horas na obra {local} em {mes}/{ano}.")

    # Criando os botões
    tk.Button(root, text="Registrar Horas", command=registrar_horas_gui, bg=button_color, fg="white", font=font, width=30, height=2).pack(pady=14)
    tk.Button(root, text="Registrar Trabalhador", command=registrar_trabalhador_gui, bg=button_color, fg="white", font=font, width=30, height=2).pack(pady=14)
    tk.Button(root, text="Registrar Obra", command=registrar_obra_gui, bg=button_color, fg="white", font=font, width=30, height=2).pack(pady=14)
    tk.Button(root, text="Verificar Horas de Empregado", command=horas_trabalhadas_empregado_gui, bg=button_color, fg="white", font=font, width=30, height=2).pack(pady=14)
    tk.Button(root, text="Verificar Horas de Obra", command=horas_trabalhadas_obra_gui, bg=button_color, fg="white", font=font, width=30, height=2).pack(pady=14)
    tk.Button(root, text="Sair", command=root.quit, bg="red", fg="white", font=font, width=30, height=2).pack(pady=10)

    # Iniciar a interface gráfica
    root.mainloop()

# Iniciar a aplicação
criar_interface()
