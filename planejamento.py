from datetime import datetime

# Nome do arquivo para armazenar os dados
arquivo_txt = 'planejamento_semanal.txt'

# Cabeçalho das tarefas
tarefas = {
    '1': 'Cap ficha sangrenta e dominação', 
    '2': 'Comprar itens de dominação e ficha sangrenta', 
    '3': 'Missões mundiais, mundiais de baú, missões de profissão nos 2 chars, limpar pouso santo, teatro e máquina',
    '4': 'Todas as quests mundiais',
    '5': 'Raid normal caso necessite upgradar item de pvp',
    '6': 'Dar uma farmada para upar profissão nos 2 chars',
    '7': 'Delves',
    '8': 'Pvp e farmar honra para engastes'
}

# Função para salvar o progresso atual no arquivo .txt
def salvar_progresso(respostas, finalizada=False):
    # Sempre sobrescreve o arquivo para evitar múltiplos registros
    with open(arquivo_txt, 'w', encoding='utf-8') as file:
        if finalizada:
            file.write("Resumo do Planejamento Semanal\n\n")  # Quebra de linha após o título
        else:
            file.write("Planejamento Semanal (Progresso Parcial)\n\n")  # Quebra de linha após o título
        
        for chave, resposta in respostas.items():
            if resposta:  # Salva apenas as tarefas preenchidas
                file.write(f"{chave} - {tarefas[chave]} - {resposta}\n")
        file.write('\n')

# Função para registrar ou atualizar tarefas
def registrar_tarefas():
    # Sempre inicia com respostas vazias
    respostas = {str(i): "" for i in range(1, 9)}
    todas_preenchidas = False

    while not todas_preenchidas:
        print("\nTarefas disponíveis para o Planejamento Semanal:\n")  # Uma quebra de linha após o título
        for chave, tarefa in tarefas.items():
            status = respostas.get(chave, "Não preenchido")
            print(f"{chave} - {tarefa} - {status}")
        
        # Uma linha entre a lista de tarefas e a próxima entrada
        print()  # Adiciona uma linha em branco
        escolha = input("Escolha a tarefa para preencher (1-8) ou '0' para sair: ").strip()
        print()  # Adiciona uma linha em branco após a escolha
        if escolha == '0':
            # Salva o progresso atual para retomada posterior
            salvar_progresso(respostas)
            print("Progresso parcial salvo. Você pode continuar mais tarde.\n")
            break
        elif escolha in tarefas:
            status = input(f"{tarefas[escolha]} (Sim/Não): ").strip().capitalize()
            while status not in ['Sim', 'Não']:
                print("\nResposta inválida! Digite 'Sim' ou 'Não'.\n")
                status = input(f"{tarefas[escolha]} (Sim/Não): ").strip().capitalize()
            respostas[escolha] = status

            # Salvar o progresso incrementalmente
            salvar_progresso(respostas)

            # Verificar se todas as tarefas foram preenchidas
            todas_preenchidas = all(respostas.values())
            if todas_preenchidas:
                print("\nTodas as tarefas do Planejamento Semanal foram preenchidas!")
                # Salva o resumo do planejamento semanal e apaga os registros intermediários
                salvar_progresso(respostas, finalizada=True)
                print("\nResumo do planejamento semanal salvo no arquivo.\n")
                break
        else:
            print("\nOpção inválida! Escolha um número de 1 a 8 ou '0' para sair.\n")

# Função para resetar o arquivo de texto
def resetar_arquivo():
    confirmar = input("\nTem certeza que deseja resetar o planejamento? Isso apagará todas as informações. (Sim/Não): ").strip().capitalize()
    if confirmar == 'Sim':
        with open(arquivo_txt, mode='w', encoding='utf-8') as file:
            file.write("")  # Limpa o conteúdo do arquivo
        print("\nPlanejamento semanal resetado com sucesso.\n")
    else:
        print("\nOperação cancelada.\n")

# Menu principal
def menu():
    print("\nMenu de Planejamento Semanal\n")
    print("1 - Registrar ou atualizar tarefas do planejamento")
    print("2 - Resetar planejamento")
    print("3 - Sair\n")
    opcao = input("Escolha uma opção: ").strip()  

    if opcao == '1':
        registrar_tarefas()
    elif opcao == '2':
        resetar_arquivo()
    elif opcao == '3':
        print("\nSaindo...\n")
    else:
        print("\nOpção inválida!\n")
        menu()

# Executar o menu
menu()
