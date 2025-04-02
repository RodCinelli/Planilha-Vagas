import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import os

# Estrutura de pastas
pasta_planejamento = "planejamento"
pasta_diario = os.path.join(pasta_planejamento, "diario")
pasta_semanal = os.path.join(pasta_planejamento, "semanal")

# Criar pastas se não existirem
for pasta in [pasta_planejamento, pasta_diario, pasta_semanal]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Cabeçalho das tarefas
tarefas = {
    "1": "Aplicar em vagas no LinkedIn para estágio e júnior em desenvolvedor full stack",
    "2": "Aplicar em vagas no LinkedIn para estágio e júnior em desenvolvedor python",
    "3": "Aplicar em vagas no LinkedIn para estágio e júnior em inteligência artificial",
    "4": "Aplicar em vagas no LinkedIn para estágio em engenheiro de software",
    "5": "Aplicar em vagas no Infojobs",
    "6": "Aplicar em vagas no Vagas.com",
    "7": "Aplicar em vagas no Programathor",
}


# Funções de gerenciamento de arquivos (mantidas sem alterações)
def obter_arquivo_diario(data=None):
    if data is None:
        data = datetime.now()
    data_str = data.strftime("%Y-%m-%d")
    dia_semana = data.strftime("%A")
    return os.path.join(pasta_diario, f"planejamento_{data_str}_{dia_semana}.txt")


def obter_arquivo_semanal():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    periodo = f"{inicio_semana.strftime('%Y-%m-%d')}_{fim_semana.strftime('%Y-%m-%d')}"
    return os.path.join(pasta_semanal, f"relatorio_semanal_{periodo}.txt")


def carregar_progresso(arquivo_txt):
    respostas = {str(i): "" for i in range(1, 8)}
    try:
        with open(arquivo_txt, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if " - " in line:
                    partes = line.strip().split(" - ", 2)
                    if len(partes) == 3:
                        chave, tarefa, status = partes
                        if chave in respostas:
                            respostas[chave] = status
    except FileNotFoundError:
        pass
    return respostas


def salvar_progresso(arquivo_txt, respostas, finalizada=False):
    with open(arquivo_txt, "w", encoding="utf-8") as file:
        data_atual = datetime.now().strftime("%d/%m/%Y")
        dia_semana = datetime.now().strftime("%A")
        if finalizada:
            file.write(f"Planejamento Diário - {dia_semana} ({data_atual})\n\n")
        else:
            file.write(
                f"Planejamento Diário (Progresso Parcial) - {dia_semana} ({data_atual})\n\n"
            )
        for chave, resposta in respostas.items():
            if chave in tarefas and resposta:
                file.write(f"{chave} - {tarefas[chave]} - {resposta}\n")
        file.write("\n")


def gerar_relatorio_semanal():
    arquivo_semanal = obter_arquivo_semanal()
    hoje = datetime.now()
    dias_semana = [(hoje - timedelta(days=i)) for i in range(7)]
    dias_semana.reverse()

    relatorio = {}
    for tarefa_id, descricao in tarefas.items():
        relatorio[tarefa_id] = {"descricao": descricao, "dias": {}}

    for data in dias_semana:
        arquivo_diario = obter_arquivo_diario(data)
        dia_str = data.strftime("%A (%d/%m)")
        if os.path.exists(arquivo_diario):
            respostas = carregar_progresso(arquivo_diario)
            for tarefa_id in tarefas.keys():
                relatorio[tarefa_id]["dias"][dia_str] = respostas.get(
                    tarefa_id, "Não registrado"
                )
        else:
            for tarefa_id in tarefas.keys():
                relatorio[tarefa_id]["dias"][dia_str] = "Não registrado"

    with open(arquivo_semanal, "w", encoding="utf-8") as file:
        hoje = datetime.now()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = hoje
        file.write(
            f"RELATÓRIO SEMANAL ({inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')})\n\n"
        )
        for tarefa_id, info in relatorio.items():
            file.write(f"Tarefa {tarefa_id}: {info['descricao']}\n\n")
            total_sim = sum(1 for status in info["dias"].values() if status == "Sim")
            file.write(f"Progresso por dia:\n\n")
            for dia, status in info["dias"].items():
                file.write(f"  - {dia}: {status}\n")
            file.write(f"\nTotal de dias realizados: {total_sim}/7 dias\n\n")
    messagebox.showinfo("Sucesso", f"Relatório semanal gerado: {arquivo_semanal}")


# Função principal para registrar tarefas
def registrar_tarefas():
    """Cria a janela para registrar tarefas diárias com 'Não' selecionado por padrão."""
    janela_tarefas = tk.Toplevel(root)  # 'root' é a janela principal
    janela_tarefas.title("Registrar Tarefas Diárias")
    janela_tarefas.configure(bg="#F0F0F0")  # Fundo cinza claro

    # Definir tamanho e centralizar a janela de tarefas
    largura_tarefas = 680
    altura_tarefas = 500
    centralizar_janela(janela_tarefas, largura_tarefas, altura_tarefas)

    # Título da janela
    tk.Label(
        janela_tarefas,
        text="Registrar Tarefas Diárias",
        bg="#F0F0F0",
        fg="#333333",
        font=("Helvetica", 16, "bold"),
    ).pack(pady=10)

    # Frame para as tarefas com borda e fundo branco
    frame_tarefas = tk.Frame(janela_tarefas, bg="white", bd=2, relief="groove")
    frame_tarefas.pack(pady=20, padx=20, fill="both", expand=True)

    # Dicionário de tarefas
    tarefas = {
        "1": "Aplicar em vagas no LinkedIn para estágio e júnior em desenvolvedor full stack",
        "2": "Aplicar em vagas no LinkedIn para estágio e júnior em desenvolvedor python",
        "3": "Aplicar em vagas no LinkedIn para estágio e júnior em inteligência artificial",
        "4": "Aplicar em vagas no LinkedIn para estágio em engenheiro de software",
        "5": "Aplicar em vagas no Infojobs",
        "6": "Aplicar em vagas no Vagas.com",
        "7": "Aplicar em vagas no Programathor",
    }

    # Variáveis para os RadioButtons com 'Não' como padrão
    vars_respostas = {}
    for chave in tarefas.keys():
        vars_respostas[chave] = tk.StringVar(value="Não")  # Sempre "Não" por padrão

    # Exibir tarefas e RadioButtons
    for i, (chave, tarefa) in enumerate(tarefas.items()):
        tk.Label(
            frame_tarefas,
            text=f"{chave} - {tarefa}",
            bg="white",
            fg="#333333",
            font=("Helvetica", 10),
            wraplength=500,
            justify="left",
        ).grid(row=i, column=0, sticky="w", padx=10, pady=10)
        radio_sim = tk.Radiobutton(
            frame_tarefas,
            text="Sim",
            variable=vars_respostas[chave],
            value="Sim",
            bg="white",
            fg="#333333",
            font=("Helvetica", 10),
        )
        radio_nao = tk.Radiobutton(
            frame_tarefas,
            text="Não",
            variable=vars_respostas[chave],
            value="Não",
            bg="white",
            fg="#333333",
            font=("Helvetica", 10),
        )
        radio_sim.grid(row=i, column=1, sticky="w", padx=10, pady=10)
        radio_nao.grid(row=i, column=2, sticky="w", padx=10, pady=10)

    # Frame para botões com fundo cinza claro
    frame_botoes = tk.Frame(janela_tarefas, bg="#F0F0F0")
    frame_botoes.pack(pady=20)

    # Botões de ação
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=10)
    ttk.Button(
        frame_botoes,
        text="Salvar Registro Diário",
        command=lambda: salvar_progresso_interface(
            obter_arquivo_diario(), vars_respostas
        ),
        style="TButton",
    ).grid(row=0, column=0, padx=10)
    ttk.Button(
        frame_botoes,
        text="Finalizar Planejamento",
        command=lambda: finalizar_planejamento(
            obter_arquivo_diario(), vars_respostas, janela_tarefas
        ),
        style="TButton",
    ).grid(row=0, column=1, padx=10)


def salvar_progresso_interface(arquivo_txt, vars_respostas):
    """Salva o progresso parcial e exibe mensagem de sucesso."""
    respostas = {chave: var.get() for chave, var in vars_respostas.items() if var.get()}
    salvar_progresso(arquivo_txt, respostas)
    messagebox.showinfo("Sucesso", "Progresso salvo com sucesso.")


def finalizar_planejamento(arquivo_txt, vars_respostas, janela):
    """Finaliza o planejamento diário, verifica se todas as tarefas foram respondidas."""
    respostas = {chave: var.get() for chave, var in vars_respostas.items()}
    if all(respostas.get(k, "") for k in tarefas.keys()):
        salvar_progresso(arquivo_txt, respostas, finalizada=True)
        messagebox.showinfo("Sucesso", "Planejamento diário finalizado com sucesso.")
        if datetime.now().weekday() == 6:  # Domingo
            gerar_relatorio_semanal()
        janela.destroy()
    else:
        messagebox.showwarning("Aviso", "Preencha todas as tarefas antes de finalizar.")


def resetar_planejamento():
    arquivo_txt = obter_arquivo_diario()
    if os.path.exists(arquivo_txt):
        if messagebox.askyesno(
            "Confirmação",
            "Tem certeza que deseja resetar o planejamento de hoje? Isso apagará todas as informações.",
        ):
            os.remove(arquivo_txt)
            messagebox.showinfo("Sucesso", "Planejamento diário resetado com sucesso.")
    else:
        messagebox.showinfo(
            "Informação", "Não há planejamento para hoje para ser resetado."
        )


def gerar_relatorio():
    if messagebox.askyesno("Confirmação", "Deseja gerar o relatório semanal agora?"):
        gerar_relatorio_semanal()


# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    """Centraliza a janela na tela com base em sua largura e altura."""
    tela_largura = janela.winfo_screenwidth()  # Obtém a largura da tela
    tela_altura = janela.winfo_screenheight()  # Obtém a altura da tela
    x = (tela_largura - largura) // 2  # Calcula a posição x
    y = (tela_altura - altura) // 2  # Calcula a posição y
    janela.geometry(f"{largura}x{altura}+{x}+{y}")  # Define a geometria


# Criar a janela principal
root = tk.Tk()
root.title("Planejamento Diário")
root.configure(bg="#F0F0F0")
root.resizable(True, True)

# Definir tamanho e centralizar a janela principal
largura_root = 400
altura_root = 300
centralizar_janela(root, largura_root, altura_root)

# Adicionar ícone (descomente e ajuste o caminho conforme necessário)
# root.iconbitmap('caminho/para/seu/icon.ico')

# Frame para botões do menu
frame_menu = tk.Frame(root, bg="#F0F0F0")
frame_menu.pack(expand=True)

# Botões do menu principal
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
ttk.Button(
    frame_menu,
    text="Registrar ou Atualizar Tarefas do Dia",
    command=registrar_tarefas,
    style="TButton",
).pack(pady=10)
ttk.Button(
    frame_menu,
    text="Resetar Planejamento do Dia",
    command=resetar_planejamento,
    style="TButton",
).pack(pady=10)
ttk.Button(
    frame_menu,
    text="Gerar Relatório Semanal Manualmente",
    command=gerar_relatorio,
    style="TButton",
).pack(pady=10)
ttk.Button(
    frame_menu, 
    text="Fechar o Programa", 
    command=root.quit, 
    style="TButton",
).pack(pady=10)

# Executar o loop principal
root.mainloop()
