import json

################# funções #################
def menu_principal():
    print("----- MENU PRINCIPAL -----")
    print("(1) Estudantes")
    print("(2) Professores")
    print("(3) Disciplinas")
    print("(4) Turmas")
    print("(5) Matrículas")
    print("(9) Sair\n")

    return input("Informe a opção desejada: ")

def menu_operacoes():
    print("(1) Incluir")
    print("(2) Listar")
    print("(3) Atualizar")
    print("(4) Excluir")
    print("(9) Voltar ao menu principal\n")

    return input("Informe a ação desejada: ")


################# leitura e escrita em arquivos #################
def escrever_arquivo(lista: list, arquivo: str) -> None:
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)
        f.close()

def ler_arquivo(arquivo: str) -> list:
    data = []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()
        return data
    except:
        return data
    
################# checagem de mesmo id #################
def same_id(lista: list, id: int) -> bool:
    for objeto in lista:
        if objeto.get("codigo") == id:
            return True
    return False
same_id([], 'a')


################# inclusão das informações #################
def incluir_pessoa(arquivo: str) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)
    while True: # loop para verificar erro no input
        try:
            id = int(input("Codigo: "))
            if same_id(lista, id):
                print("CÓDIGO JÁ CADASTRADO!")
                print("INSIRA OUTRO CÓDIGO!")
                continue
            break
        except ValueError:
            print("INSIRA UM NÚMERO!")
        

    nome = input("Nome: ")
    cpf = input("CPF: ")

    lista.append({"codigo": id,
                  "nome": nome,
                  "cpf": cpf}) 
    
    escrever_arquivo(lista, arquivo)


def incluir_disciplina(arquivo: str) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)
    while True: # loop para verificar erro no input
        try:
            id = int(input("Codigo: "))
            if same_id(lista, id):
                print("CÓDIGO JÁ CADASTRADO!")
                print("INSIRA OUTRO CÓDIGO!")
                continue
            break
        except ValueError:
            print("INSIRA UM NÚMERO!")
        
    nome = input("Disciplina: ")

    lista.append({"codigo": id,
                  "disciplina": nome}) 
    
    escrever_arquivo(lista, arquivo)

def incluir_turma(arquivo: str) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)
    while True: # loop para verificar erro no input
        try:
            turma_id = int(input("Codigo: "))
            if same_id(lista, turma_id):
                print("CÓDIGO JÁ CADASTRADO!")
                print("INSIRA OUTRO CÓDIGO!")
                continue
            prof_id = int(input("Codigo professor: "))
            disci_id = int(input("Codigo disciplina: "))
            break
        except ValueError:
            print("INSIRA UM NÚMERO!")


    lista.append({"codigo": turma_id,
                  "professor": prof_id,
                  "disciplina": disci_id}) 
    
    escrever_arquivo(lista, arquivo)

def incluir_matricula(arquivo: str) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)
    while True: # loop para verificar erro no input
        try:
            turma_id = int(input("Codigo da turma: "))
            aluno_id = int(input("Codigo do aluno: "))
            break
        except ValueError:
            print("INSIRA UM NÚMERO!")


    lista.append({"codigo": turma_id,
                  "aluno": aluno_id}) 
    
    escrever_arquivo(lista, arquivo)

################# listagem #################
def listar(arquivo: str) -> None:
    print("===== Listagem =====")
    lista = ler_arquivo(arquivo)
    if lista: # verifica se a lista não está vazia
        for objeto in lista:
            print(objeto)
    else:
        print("SEM CADASTROS!")


################# edição #################
def editar_pessoa(arquivo: str) -> None:
    print("===== Atualização =====")
    lista = ler_arquivo(arquivo)
    while True: # loop para verificar erro no input
        try:
            id_antigo = int(input("Insira o codigo que deseja alterar: "))
            break
        except ValueError:
            print("INSIRA UM NÚMERO!")
    objeto_atualizar = None
    for objeto in lista:
        if objeto.get("codigo") == id_antigo:
            objeto_atualizar = objeto
            break
    if objeto_atualizar:
        print("\nInsira os dados novos\n")
        while True: # loop para verificar erro no input
            try:
                objeto_atualizar["codigo"] = int(input("Código: "))
                break
            except ValueError:
                print("INSIRA UM NÚMERO!")
        objeto_atualizar["nome"] = input("Nome: ")
        objeto_atualizar["cpf"] = input("CPF: ")
    else:
        print("Pessoa não encontrada")
    
    escrever_arquivo(lista, arquivo)

################# exclusão #################
def excluir(arquivo: str) -> None:
    print("===== Exclusão =====")
    while True: # loop para verificar erro no input
        try:
            id_excluir = int(input("Insira o codigo do estudante: "))
            break
        except ValueError:
            print("INSIRA UM NÚMERO!")
    
    lista = ler_arquivo(arquivo)
    aluno_remover = None
    for aluno in lista:
        if aluno.get("codigo") == id_excluir:
            aluno_remover = aluno
    if aluno_remover:
        lista.remove(aluno_remover) 
    else:
        print("\nNão foi possível achar o estudante!")
    
    escrever_arquivo(lista, arquivo)


################# variáveis de arquivos #################
ARQUIVO_ALUNO = "alunos.json"
ARQUIVO_PROFESSOR = "professores.json"
ARQUIVO_DISCIPLINA = "disciplinas.json"
ARQUIVO_TURMA = "turmas.json"
ARQUIVO_MATRICULA = "matriculas.json"


################# loop menu principal #################
while True:
   
    option = menu_principal()

    # verifica se a opção é válida
    if option == '1' or option == '2' or option == '3' or option == '4' or option == '5':

        ################# loop menu de operações #################
        while True:
            if option == '1':
                print("\n***** [ESTUDANTES] MENU DE OPERAÇÕES *****")
                
                action = menu_operacoes()

                print()
                if action == '1': # Incluir
                    incluir_pessoa(ARQUIVO_ALUNO)
                elif action == '2': # Listar
                    listar(ARQUIVO_ALUNO)
                elif action == '3': # Atualizar
                    editar_pessoa(ARQUIVO_ALUNO)
                elif action == '4': # Excluir
                    excluir(ARQUIVO_ALUNO)
                elif action == '9':
                    print("===== Voltando ao menu principal =====\n")
                    break
                else:
                    print("\nOpção inválida\n")


            elif option == '2': # Professores
                print("***** [PROFESSORES] MENU DE OPERAÇÕES *****")

                action = menu_operacoes()

                print()
                if action == '1': # Incluir
                    incluir_pessoa(ARQUIVO_PROFESSOR)
                elif action == '2': # Listar
                    listar(ARQUIVO_PROFESSOR)
                elif action == '3': # Atualizar
                    editar_pessoa(ARQUIVO_PROFESSOR)
                elif action == '4': # Excluir
                    excluir(ARQUIVO_PROFESSOR)
                elif action == '9':
                    print("===== Voltando ao menu principal =====\n")
                    break
                else:
                    print("\nOpção inválida\n")
                

            elif option == '3': # Disciplinas
                print("***** [DISCIPLINAS] MENU DE OPERAÇÕES *****")

                action = menu_operacoes()

                print()
                if action == '1': # Incluir
                    incluir_disciplina(ARQUIVO_DISCIPLINA)
                elif action == '2': # Listar
                    listar(ARQUIVO_DISCIPLINA)
                elif action == '3': # Atualizar
                    editar_pessoa(ARQUIVO_DISCIPLINA)
                elif action == '4': # Excluir
                    excluir(ARQUIVO_DISCIPLINA)
                elif action == '9':
                    print("===== Voltando ao menu principal =====\n")
                    break
                else:
                    print("\nOpção inválida\n")
                
            elif option == '4': # Turmas
                print("***** [TURMAS] MENU DE OPERAÇÕES *****")

                action = menu_operacoes()

                print()
                if action == '1': # Incluir
                    incluir_turma(ARQUIVO_TURMA)
                elif action == '2': # Listar
                    listar(ARQUIVO_TURMA)
                elif action == '3': # Atualizar
                    editar_pessoa(ARQUIVO_TURMA)
                elif action == '4': # Excluir
                    excluir(ARQUIVO_TURMA)
                elif action == '9':
                    print("===== Voltando ao menu principal =====\n")
                    break
                else:
                    print("\nOpção inválida\n")
                
            elif option == '5': # Matrículas
                print("***** [MATRÍCULAS] MENU DE OPERAÇÕES *****")

                action = menu_operacoes()

                print()
                if action == '1': # Incluir
                    incluir_matricula(ARQUIVO_MATRICULA)
                elif action == '2': # Listar
                    listar(ARQUIVO_MATRICULA)
                elif action == '3': # Atualizar
                    editar_pessoa(ARQUIVO_MATRICULA)
                elif action == '4': # Excluir
                    excluir(ARQUIVO_MATRICULA)
                elif action == '9':
                    print("===== Voltando ao menu principal =====\n")
                    break
                else:
                    print("\nOpção inválida\n")


    elif option == '9':
        print("Finalizando aplicação...")
        break
    else:
        print("Opção inválida")