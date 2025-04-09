import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import os
import locale  # Para configurar o locale

# Configurar o locale completo para português do Brasil
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale 'pt_BR.UTF-8' não disponível. Tentando 'portuguese_brazil'.")
    try:
        locale.setlocale(locale.LC_ALL, 'portuguese_brazil')  # Alternativa para Windows
    except locale.Error:
        print("Nenhum locale português disponível. Usando padrão do sistema.")
        locale.setlocale(locale.LC_ALL, '')

# Verificar o locale configurado
print("Locale atual:", locale.getlocale())

# Definição da paleta de cores
COR_PRINCIPAL = "#4682B4"  # Azul escuro para fundo
COR_DESTAQUE = "#4DA6FF"  # Azul médio para elementos de destaque
COR_TEXTO = "#333333"  # Cinza escuro para textos
COR_BORDA = "#99CCFF"  # Azul claro para bordas
COR_BOTAO = "#CCE5FF"  # Azul muito claro para botões
COR_RELOGIO = "#FFFD54"  # Amarelo vibrante claro para o relógio
COR_TOOLTIP = "#FFFD54"  # Amarelo vibrante claro para tooltips
COR_LINHAS = "#F8FBFF"  # Azul muito claro para as linhas de tarefas

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

# Classe para criar tooltips personalizados
class Tooltip:
    def __init__(self, widget, text, bg_color=None, fg_color=None, font=None):
        self.widget = widget
        self.text = text
        self.bg_color = bg_color or "lightyellow"
        self.fg_color = fg_color or "black"
        self.font = font or ("Helvetica", 8)  # Fonte menor
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)  # Seguir o mouse
        self.tip_window = None

    def on_enter(self, event=None):
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background=self.bg_color, foreground=self.fg_color,
            relief=tk.SOLID, borderwidth=1,
            font=self.font, padx=3, pady=2
        )
        label.pack(ipadx=1)
    
    def on_motion(self, event=None):
        if self.tip_window:
            x, y = event.x_root + 10, event.y_root + 10
            self.tip_window.wm_geometry(f"+{x}+{y}")
        
    def on_leave(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# Funções de gerenciamento de arquivos
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
            file.write(f"Planejamento Diário CONCLUÍDO - {dia_semana} ({data_atual})\n\n")
        else:
            file.write(
                f"Planejamento Diário (Progresso Parcial) - {dia_semana} ({data_atual})\n\n"
            )
        for chave, resposta in respostas.items():
            if chave in tarefas and resposta:
                file.write(f"{chave} - {tarefas[chave]} - {resposta}\n")
        file.write("\n")

def gerar_relatorio_semanal():
    # Obtém o caminho do arquivo semanal e define os dias da semana atual
    arquivo_semanal = obter_arquivo_semanal()
    hoje = datetime.now()
    dias_semana = [(hoje - timedelta(days=i)) for i in range(7)]
    dias_semana.reverse()

    # Inicializa o dicionário do relatório para cada tarefa
    relatorio = {}
    for tarefa_id, descricao in tarefas.items():
        relatorio[tarefa_id] = {"descricao": descricao, "dias": {}}

    # Preenche o relatório com os dados dos arquivos diários
    for data in dias_semana:
        arquivo_diario = obter_arquivo_diario(data)
        dia_str = data.strftime("%A (%d/%m)")
        if os.path.exists(arquivo_diario):
            respostas = carregar_progresso(arquivo_diario)
            for tarefa_id in tarefas.keys():
                # Mapeia os status "Sim" e "Não" para "Vaga aplicada" e "Vaga não aplicada"
                status = respostas.get(tarefa_id, "Não registrado")
                if status == "Sim":
                    relatorio[tarefa_id]["dias"][dia_str] = "Vaga aplicada"
                elif status == "Não":
                    relatorio[tarefa_id]["dias"][dia_str] = "Vaga não aplicada"
                else:
                    relatorio[tarefa_id]["dias"][dia_str] = "Não registrado"
        else:
            for tarefa_id in tarefas.keys():
                relatorio[tarefa_id]["dias"][dia_str] = "Não registrado"

    # Escreve o relatório no arquivo semanal
    with open(arquivo_semanal, "w", encoding="utf-8") as file:
        hoje = datetime.now()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = hoje
        file.write(
            f"RELATÓRIO SEMANAL ({inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')})\n\n"
        )
        for tarefa_id, info in relatorio.items():
            file.write(f"Tarefa {tarefa_id}: {info['descricao']}\n\n")
            # Calcula o total de dias com "Vaga aplicada"
            total_aplicadas = sum(1 for status in info["dias"].values() if status == "Vaga aplicada")
            file.write(f"Progresso por dia:\n\n")
            for dia, status in info["dias"].items():
                file.write(f"  - {dia}: {status}\n")
            file.write(f"\nTotal de dias com vaga aplicada: {total_aplicadas}/7 dias\n\n")
    messagebox.showinfo("Sucesso", f"Relatório semanal gerado: {arquivo_semanal}")

# Função para atualizar o relógio em tempo real
def atualizar_relogio():
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lbl_relogio.config(text=hora_atual)
    root.after(1000, atualizar_relogio)

# Função para registrar tarefas
def registrar_tarefas():
    janela_tarefas = tk.Toplevel(root)
    janela_tarefas.title("Registrar Tarefas Diárias")
    janela_tarefas.configure(bg=COR_PRINCIPAL)

    largura_tarefas = 690
    altura_tarefas = 460
    centralizar_janela(janela_tarefas, largura_tarefas, altura_tarefas)

    header_frame = tk.Frame(janela_tarefas, bg=COR_PRINCIPAL, height=40)
    header_frame.pack(fill=tk.X, pady=0)
    
    btn_voltar = tk.Button(
        header_frame,
        text="←",
        font=("Arial", 16, "bold"),
        bg=COR_PRINCIPAL,
        fg=COR_RELOGIO,
        relief=tk.FLAT,
        bd=0,
        activebackground=COR_PRINCIPAL,
        activeforeground=COR_RELOGIO,
        command=janela_tarefas.destroy,
        cursor="hand2"
    )
    btn_voltar.pack(side=tk.LEFT, padx=10)
    Tooltip(btn_voltar, "Voltar para a janela principal", COR_TOOLTIP, COR_TEXTO)

    titulo_tarefas = tk.Label(
        header_frame,
        text="Registrar Tarefas Diárias",
        bg=COR_PRINCIPAL,
        fg=COR_TEXTO,
        font=("Helvetica", 16, "bold"),
    )
    titulo_tarefas.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=10, padx=(50, 0))
    Tooltip(titulo_tarefas, "Local para registrar ou atualizar suas tarefas diárias", COR_TOOLTIP, COR_TEXTO)
    
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lbl_relogio_tarefas = tk.Label(
        header_frame,
        text=data_hora,
        bg=COR_PRINCIPAL,
        fg=COR_RELOGIO,
        font=("Helvetica", 10)
    )
    lbl_relogio_tarefas.pack(side=tk.RIGHT, padx=15, pady=5)
    Tooltip(lbl_relogio_tarefas, "Data e hora atuais do sistema", COR_TOOLTIP, COR_TEXTO)
    
    def atualizar_relogio_tarefas():
        hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        lbl_relogio_tarefas.config(text=hora_atual)
        janela_tarefas.after(1000, atualizar_relogio_tarefas)
    
    atualizar_relogio_tarefas()

    content_frame = tk.Frame(janela_tarefas, bg=COR_PRINCIPAL)
    content_frame.pack(fill=tk.BOTH, expand=True)

    frame_tarefas = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
    frame_tarefas.pack(pady=20, padx=20, fill="both", expand=True)
    
    frame_tarefas.grid_columnconfigure(0, weight=1)

    # Dicionário para armazenar as variáveis dos radio buttons
    vars_respostas = {}
    for chave in tarefas.keys():
        vars_respostas[chave] = tk.StringVar(value="Não")

    # Cria as linhas de tarefas com opções "Sim" e "Não"
    for i, (chave, tarefa) in enumerate(tarefas.items()):
        frame_linha = tk.Frame(frame_tarefas, bg=COR_LINHAS)
        frame_linha.grid(row=i, column=0, sticky="ew", columnspan=3)
        frame_linha.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            frame_linha,
            text=f"{chave} - {tarefa}",
            bg=COR_LINHAS,
            fg=COR_TEXTO,
            font=("Helvetica", 10),
            wraplength=500,
            justify="left",
            pady=5,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        frame_radio = tk.Frame(frame_linha, bg="white", bd=0)
        frame_radio.grid(row=0, column=1, sticky="e", padx=10)
        
        radio_sim = tk.Radiobutton(
            frame_radio,
            text="Sim",
            variable=vars_respostas[chave],
            value="Sim",
            bg="white",
            fg=COR_TEXTO,
            font=("Helvetica", 10),
            selectcolor="white",
            activebackground="white",
        )
        radio_nao = tk.Radiobutton(
            frame_radio,
            text="Não",
            variable=vars_respostas[chave],
            value="Não",
            bg="white",
            fg=COR_TEXTO,
            font=("Helvetica", 10),
            selectcolor="white",
            activebackground="white",
        )
        radio_sim.pack(side=tk.LEFT, padx=5)
        radio_nao.pack(side=tk.LEFT, padx=5)

    frame_botoes = tk.Frame(content_frame, bg=COR_PRINCIPAL)
    frame_botoes.pack(pady=20)

    btn_salvar = tk.Button(
        frame_botoes,
        text="Salvar Registro Diário",
        command=lambda: salvar_progresso_interface(
            obter_arquivo_diario(), vars_respostas
        ),
        bg=COR_BOTAO,
        fg=COR_TEXTO,
        font=("Helvetica", 11),
        padx=15,
        pady=8,
        bd=1,
        relief=tk.RAISED,
        activebackground=COR_DESTAQUE,
        activeforeground="white",
        cursor="hand2"
    )
    btn_salvar.grid(row=0, column=0, padx=10)
    Tooltip(btn_salvar, "Salva seu progresso atual sem fechar a janela", COR_TOOLTIP, COR_TEXTO)
    
    btn_finalizar = tk.Button(
        frame_botoes,
        text="Finalizar Planejamento",
        command=lambda: finalizar_planejamento(
            obter_arquivo_diario(), vars_respostas, janela_tarefas
        ),
        bg=COR_BOTAO,
        fg=COR_TEXTO,
        font=("Helvetica", 11),
        padx=15,
        pady=8,
        bd=1,
        relief=tk.RAISED,
        activebackground=COR_DESTAQUE,
        activeforeground="white",
        cursor="hand2"
    )
    btn_finalizar.grid(row=0, column=1, padx=10)
    Tooltip(btn_finalizar, "Finaliza e salva o planejamento do dia e fecha esta janela", COR_TOOLTIP, COR_TEXTO)

# Função para atualizar o status do planejamento
def atualizar_status():
    arquivo_hoje = obter_arquivo_diario()
    if os.path.exists(arquivo_hoje):
        with open(arquivo_hoje, "r", encoding="utf-8") as file:
            primeira_linha = file.readline().strip()
            if "CONCLUÍDO" in primeira_linha:
                status_lbl.config(text="Status: Planejamento diário concluído")
            else:
                status_lbl.config(text="Status: Planejamento iniciado")
    else:
        status_lbl.config(text="Status: Sem planejamento hoje")

def salvar_progresso_interface(arquivo_txt, vars_respostas):
    # Salva o progresso parcial com base nas respostas selecionadas
    respostas = {chave: var.get() for chave, var in vars_respostas.items() if var.get()}
    salvar_progresso(arquivo_txt, respostas)
    messagebox.showinfo("Sucesso", "Progresso salvo com sucesso.")
    atualizar_status()

def finalizar_planejamento(arquivo_txt, vars_respostas, janela):
    # Finaliza o planejamento, verificando se todas as tarefas foram preenchidas
    respostas = {chave: var.get() for chave, var in vars_respostas.items()}
    if all(respostas.get(k, "") for k in tarefas.keys()):
        salvar_progresso(arquivo_txt, respostas, finalizada=True)
        messagebox.showinfo("Sucesso", "Planejamento diário finalizado com sucesso.")
        if datetime.now().weekday() == 6:  # Domingo
            gerar_relatorio_semanal()
        janela.destroy()
        atualizar_status()
    else:
        messagebox.showwarning("Aviso", "Preencha todas as tarefas antes de finalizar.")

def resetar_planejamento():
    # Reseta o planejamento do dia atual, apagando o arquivo correspondente
    arquivo_txt = obter_arquivo_diario()
    if os.path.exists(arquivo_txt):
        if messagebox.askyesno(
            "Confirmação",
            "Tem certeza que deseja resetar o planejamento de hoje? Isso apagará todas as informações.",
        ):
            os.remove(arquivo_txt)
            messagebox.showinfo("Sucesso", "Planejamento diário resetado com sucesso.")
            atualizar_status()
    else:
        messagebox.showinfo(
            "Informação", "Não há planejamento para hoje para ser resetado."
        )

def gerar_relatorio():
    # Solicita confirmação antes de gerar o relatório semanal
    if messagebox.askyesno("Confirmação", "Deseja gerar o relatório semanal agora?"):
        gerar_relatorio_semanal()

# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    tela_largura = janela.winfo_screenwidth()
    tela_altura = janela.winfo_screenheight()
    x = (tela_largura - largura) // 2
    y = (tela_altura - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

# Criar a janela principal
root = tk.Tk()
root.title("Planejamento Diário")
root.configure(bg=COR_PRINCIPAL)
root.resizable(True, True)

# Tentar forçar o Tkinter a usar UTF-8 (opcional, pode ser necessário em alguns sistemas)
try:
    root.tk.call('encoding', 'system', 'utf-8')
except:
    print("Não foi possível forçar o Tkinter a usar UTF-8. Continuando com codificação padrão.")

largura_root = 450
altura_root = 500
centralizar_janela(root, largura_root, altura_root)

titulo_frame = tk.Frame(root, bg=COR_PRINCIPAL)
titulo_frame.pack(fill=tk.X, pady=15)

titulo_lbl = tk.Label(
    titulo_frame,
    text="Sistema de Planejamento Diário",
    bg=COR_PRINCIPAL,
    fg=COR_TEXTO,
    font=("Helvetica", 18, "bold")
)
titulo_lbl.pack()
Tooltip(titulo_lbl, "Sistema para controle e organização das suas tarefas diárias", COR_TOOLTIP, COR_TEXTO)

lbl_relogio = tk.Label(
    root,
    text="",
    bg=COR_PRINCIPAL,
    fg=COR_RELOGIO,
    font=("Helvetica", 12)
)
lbl_relogio.pack(pady=5)
Tooltip(lbl_relogio, "Data e hora atuais do sistema", COR_TOOLTIP, COR_TEXTO)
atualizar_relogio()

ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

frame_menu = tk.Frame(root, bg=COR_PRINCIPAL)
frame_menu.pack(expand=True, pady=20)

btn_registrar = tk.Button(
    frame_menu,
    text="Registrar ou Atualizar Tarefas",
    command=registrar_tarefas,
    bg=COR_BOTAO,
    fg=COR_TEXTO,
    font=("Helvetica", 11),
    padx=15,
    pady=8,
    bd=1,
    relief=tk.RAISED,
    activebackground=COR_DESTAQUE,
    activeforeground="white",
    width=30,
    cursor="hand2"
)
btn_registrar.pack(pady=10, fill=tk.X)
Tooltip(btn_registrar, "Abre uma nova janela para registrar ou atualizar suas tarefas diárias", COR_TOOLTIP, COR_TEXTO)

btn_resetar = tk.Button(
    frame_menu,
    text="Resetar Planejamento do Dia",
    command=resetar_planejamento,
    bg=COR_BOTAO,
    fg=COR_TEXTO,
    font=("Helvetica", 11),
    padx=15,
    pady=8,
    bd=1,
    relief=tk.RAISED,
    activebackground=COR_DESTAQUE,
    activeforeground="white",
    width=30,
    cursor="hand2"
)
btn_resetar.pack(pady=10, fill=tk.X)
Tooltip(btn_resetar, "Apaga o planejamento do dia atual, permitindo que você comece novamente", COR_TOOLTIP, COR_TEXTO)

btn_relatorio = tk.Button(
    frame_menu,
    text="Gerar Relatório Semanal",
    command=gerar_relatorio,
    bg=COR_BOTAO,
    fg=COR_TEXTO,
    font=("Helvetica", 11),
    padx=15,
    pady=8,
    bd=1,
    relief=tk.RAISED,
    activebackground=COR_DESTAQUE,
    activeforeground="white",
    width=30,
    cursor="hand2"
)
btn_relatorio.pack(pady=10, fill=tk.X)
Tooltip(btn_relatorio, "Gera um relatório resumindo as tarefas realizadas durante a semana", COR_TOOLTIP, COR_TEXTO)

btn_fechar = tk.Button(
    frame_menu,
    text="Fechar o Programa",
    command=root.quit,
    bg=COR_BOTAO,
    fg=COR_TEXTO,
    font=("Helvetica", 11),
    padx=15,
    pady=8,
    bd=1,
    relief=tk.RAISED,
    activebackground=COR_DESTAQUE,
    activeforeground="white",
    width=30,
    cursor="hand2"
)
btn_fechar.pack(pady=10, fill=tk.X)
Tooltip(btn_fechar, "Encerra o programa de planejamento diário", COR_TOOLTIP, COR_TEXTO)

rodape_frame = tk.Frame(root, bg=COR_PRINCIPAL)
rodape_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

rodape_texto = tk.Label(
    rodape_frame,
    text="© 2025 Sistema de Planejamento | Emprego",
    font=("Helvetica", 8),
    bg=COR_PRINCIPAL,
    fg=COR_TEXTO
)
rodape_texto.pack()

# Label para exibir o status do planejamento diário
global status_lbl
arquivo_hoje = obter_arquivo_diario()
status_lbl = tk.Label(
    root,
    text="Status: Carregando...",
    bg=COR_PRINCIPAL,
    fg=COR_TEXTO,
    font=("Helvetica", 10)
)
status_lbl.pack(side=tk.BOTTOM, pady=5)
Tooltip(status_lbl, "Indica o status do planejamento para o dia de hoje", COR_TOOLTIP, COR_TEXTO)

atualizar_status()

data_atual = datetime.now().date()

def verificar_mudanca_dia():
    # Verifica se o dia mudou e atualiza o status automaticamente
    global data_atual
    nova_data = datetime.now().date()
    if nova_data != data_atual:
        data_atual = nova_data
        atualizar_status()
    root.after(60000, verificar_mudanca_dia)  # Verifica a cada 60 segundos

verificar_mudanca_dia()

root.mainloop()