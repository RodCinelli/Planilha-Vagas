from datetime import datetime, timedelta
import os

# Estrutura de pastas
pasta_planejamento = 'planejamento'
pasta_diario = os.path.join(pasta_planejamento, 'diario')
pasta_semanal = os.path.join(pasta_planejamento, 'semanal')

# Criar pastas se não existirem
for pasta in [pasta_planejamento, pasta_diario, pasta_semanal]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Cabeçalho das tarefas
tarefas = {
    '1': 'Aplicar em vagas no LinkedIn para estágio em engenharia de software', 
    '2': 'Aplicar em vagas no LinkedIn para estágio e desenvolvedor full stack jr', 
    '3': 'Aplicar em vagas no Infojobs',
    '4': 'Aplicar em vagas no Vagas.com',
    '5': 'Aplicar em vagas no Programathor',
}

# Função para obter o nome do arquivo diário baseado na data
def obter_arquivo_diario(data=None):
    if data is None:
        data = datetime.now()
    data_str = data.strftime('%Y-%m-%d')
    dia_semana = data.strftime('%A')
    return os.path.join(pasta_diario, f'planejamento_{data_str}_{dia_semana}.txt')

# Função para obter o nome do arquivo do relatório semanal
def obter_arquivo_semanal():
    hoje = datetime.now()
    # Encontrar o início da semana (segunda-feira)
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    periodo = f"{inicio_semana.strftime('%Y-%m-%d')}_{fim_semana.strftime('%Y-%m-%d')}"
    return os.path.join(pasta_semanal, f'relatorio_semanal_{periodo}.txt')

# Função para carregar o progresso atual do arquivo .txt diário
def carregar_progresso(arquivo_txt):
    respostas = {str(i): "" for i in range(1, 6)}  # Inicializa respostas vazias
    try:
        with open(arquivo_txt, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if " - " in line:
                    partes = line.strip().split(' - ', 2)
                    if len(partes) == 3:
                        chave, tarefa, status = partes
                        if chave in respostas:
                            respostas[chave] = status
    except FileNotFoundError:
        pass  # Arquivo ainda não existe, não precisa fazer nada

    return respostas

# Função para salvar o progresso atual no arquivo .txt diário
def salvar_progresso(arquivo_txt, respostas, finalizada=False):
    # Sempre sobrescreve o arquivo para evitar múltiplos registros
    with open(arquivo_txt, 'w', encoding='utf-8') as file:
        data_atual = datetime.now().strftime('%d/%m/%Y')
        dia_semana = datetime.now().strftime('%A')
        
        if finalizada:
            file.write(f"Planejamento Diário - {dia_semana} ({data_atual})\n\n")
        else:
            file.write(f"Planejamento Diário (Progresso Parcial) - {dia_semana} ({data_atual})\n\n")
        
        for chave, resposta in respostas.items():
            if chave in tarefas and resposta:  # Salva apenas as tarefas preenchidas
                file.write(f"{chave} - {tarefas[chave]} - {resposta}\n")
        file.write('\n')

# Função para registrar ou atualizar tarefas diárias
def registrar_tarefas_diarias():
    arquivo_txt = obter_arquivo_diario()
    
    # Carregar progresso existente
    respostas = carregar_progresso(arquivo_txt)
    todas_preenchidas = False

    while not todas_preenchidas:
        print(f"\nTarefas disponíveis para o Planejamento Diário ({datetime.now().strftime('%d/%m/%Y')}):\n")
        for chave, tarefa in tarefas.items():
            status = respostas.get(chave, "Não preenchido")
            print(f"{chave} - {tarefa} - {status}")
        
        print()
        escolha = input("Escolha a tarefa para preencher (1-5) ou '0' para sair: ").strip()
        print()
        if escolha == '0':
            # Salva o progresso atual para retomada posterior
            salvar_progresso(arquivo_txt, respostas)
            print("Progresso parcial salvo. Você pode continuar mais tarde.\n")
            break
        elif escolha in tarefas:
            status = input(f"{tarefas[escolha]} (Sim/Não): ").strip().capitalize()
            while status not in ['Sim', 'Não']:
                print("\nResposta inválida! Digite 'Sim' ou 'Não'.\n")
                status = input(f"{tarefas[escolha]} (Sim/Não): ").strip().capitalize()
            respostas[escolha] = status

            # Salvar o progresso incrementalmente
            salvar_progresso(arquivo_txt, respostas)

            # Verificar se todas as tarefas foram preenchidas
            todas_preenchidas = all(respostas.get(k, "") for k in tarefas.keys())
            if todas_preenchidas:
                print("\nTodas as tarefas do Planejamento Diário foram preenchidas!")
                # Salva o resumo do planejamento diário e apaga os registros intermediários
                salvar_progresso(arquivo_txt, respostas, finalizada=True)
                print("\nPlanejamento diário salvo no arquivo.\n")
                
                # Verificar se é domingo para gerar o relatório semanal
                if datetime.now().weekday() == 6:  # 6 é domingo
                    gerar_relatorio_semanal()
                break
        else:
            print("\nOpção inválida! Escolha um número de 1 a 5 ou '0' para sair.\n")

# Função para gerar relatório semanal
def gerar_relatorio_semanal():
    print("\nGerando relatório semanal...\n")
    
    arquivo_semanal = obter_arquivo_semanal()
    
    # Definir o intervalo da semana (últimos 7 dias)
    hoje = datetime.now()
    dias_semana = [(hoje - timedelta(days=i)) for i in range(7)]
    dias_semana.reverse()  # Ordenar do primeiro ao último dia
    
    relatorio = {}
    for tarefa_id, descricao in tarefas.items():
        relatorio[tarefa_id] = {"descricao": descricao, "dias": {}}
    
    # Coletar dados de cada dia
    for data in dias_semana:
        arquivo_diario = obter_arquivo_diario(data)
        dia_str = data.strftime('%A (%d/%m)')
        
        if os.path.exists(arquivo_diario):
            respostas = carregar_progresso(arquivo_diario)
            for tarefa_id in tarefas.keys():
                relatorio[tarefa_id]["dias"][dia_str] = respostas.get(tarefa_id, "Não registrado")
        else:
            for tarefa_id in tarefas.keys():
                relatorio[tarefa_id]["dias"][dia_str] = "Não registrado"
    
    # Salvar relatório semanal
    with open(arquivo_semanal, 'w', encoding='utf-8') as file:
        hoje = datetime.now()
        inicio_semana = hoje - timedelta(days=hoje.weekday() + 1)  # -1 porque hoje é domingo
        fim_semana = hoje
        
        file.write(f"RELATÓRIO SEMANAL ({inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')})\n\n")
        
        for tarefa_id, info in relatorio.items():
            file.write(f"Tarefa {tarefa_id}: {info['descricao']}\n\n")
            
            # Contar quantos "Sim" para a tarefa
            total_sim = sum(1 for status in info["dias"].values() if status == "Sim")
            
            file.write(f"Progresso por dia:\n\n")
            for dia, status in info["dias"].items():
                file.write(f"  - {dia}: {status}\n")
            
            file.write(f"\nTotal de dias realizados: {total_sim}/7 dias\n\n")
    
    print(f"Relatório semanal gerado com sucesso: {arquivo_semanal}\n")

# Função para resetar o arquivo de texto diário
def resetar_arquivo_diario():
    arquivo_txt = obter_arquivo_diario()
    if os.path.exists(arquivo_txt):
        confirmar = input("\nTem certeza que deseja resetar o planejamento de hoje? Isso apagará todas as informações. (Sim/Não): ").strip().capitalize()
        if confirmar == 'Sim':
            os.remove(arquivo_txt)
            print("\nPlanejamento diário resetado com sucesso.\n")
        else:
            print("\nOperação cancelada.\n")
    else:
        print("\nNão há planejamento para hoje para ser resetado.\n")

# Função para gerar manualmente o relatório semanal
def gerar_relatorio_manual():
    confirmar = input("\nDeseja gerar o relatório semanal agora? (Sim/Não): ").strip().capitalize()
    if confirmar == 'Sim':
        gerar_relatorio_semanal()
    else:
        print("\nOperação cancelada.\n")

# Menu principal
def menu():
    print("\nMenu de Planejamento Diário\n")
    print("1 - Registrar ou atualizar tarefas do dia")
    print("2 - Resetar planejamento do dia")
    print("3 - Gerar relatório semanal manualmente")
    print("4 - Sair\n")
    opcao = input("Escolha uma opção: ").strip()  

    if opcao == '1':
        registrar_tarefas_diarias()
        menu()
    elif opcao == '2':
        resetar_arquivo_diario()
        menu()
    elif opcao == '3':
        gerar_relatorio_manual()
        menu()
    elif opcao == '4':
        print("\nSaindo...\n")
    else:
        print("\nOpção inválida!\n")
        menu()

# Executar o menu
if __name__ == "__main__":
    menu()
