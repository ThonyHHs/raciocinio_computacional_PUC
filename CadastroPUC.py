import json

################# funções #################
def menu_principal() -> str:
    print("----- MENU PRINCIPAL -----")
    print("(1) Estudantes")
    print("(2) Professores")
    print("(3) Disciplinas")
    print("(4) Turmas")
    print("(5) Matrículas")
    print("(9) Sair\n")

    return input("Informe a opção desejada: ")

def menu_operacoes() -> str:
    print("(1) Incluir")
    print("(2) Listar")
    print("(3) Atualizar")
    print("(4) Excluir")
    print("(9) Voltar ao menu principal\n")

    return input("Informe a ação desejada: ")

def gerenciamento_operacoes(escolha: str, arquivo: str, campo_id: str, campo_int: list = [], campo_str: list = []) -> None:
    while True:
        print(f"\n***** [{escolha}] MENU DE OPERAÇÕES *****")
        action = menu_operacoes()

        print()
        if action == '1': # Incluir
            incluir(arquivo, campo_id, campo_int, campo_str)
        elif action == '2': # Listar
            listar(arquivo)
        elif action == '3': # Atualizar
            editar(arquivo, campo_id, campo_int, campo_str)
        elif action == '4': # Excluir
            excluir(arquivo)
        elif action == '9':
            print("===== Voltando ao menu principal =====\n")
            break
        else:
            print("\nOpção inválida\n")


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


################# checagem #################
def same_id(lista: list, id: int) -> bool:
    for objeto in lista:
        if objeto.get("codigo") == id:
            return True
    return False

def verifica_inteiro(campo: str) -> int:
    while True: # loop para verificar erro no input
        try:
            id = int(input(f"{campo}: "))
            return id
        except ValueError:
            print("INSIRA UM NÚMERO!")
    

################# inclusão das informações #################
def incluir(arquivo: str, campo_id: str, campo_int: list = [], campo_str: list = []) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)

    while True:
        id = verifica_inteiro(campo_id)
        if same_id(lista, id):
            print("CÓDIGO JÁ CADASTRADO!")
            print("INSIRA OUTRO CÓDIGO!")
            continue
        else: break

    novos_dados = {campo_id:id}

    for campo in campo_int:
        novos_dados[campo] = verifica_inteiro(campo)

    for campo in campo_str:
        novos_dados[campo] = input(f"{campo}: ")

    lista.append(novos_dados)

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
def editar(arquivo:str, campo_id:str, campo_int: list = [], campo_str: list = []) -> None:
    print("===== Atualização =====")
    lista = ler_arquivo(arquivo)

    id_antigo = verifica_inteiro(campo_id)

    objeto_atualizar = None
    for objeto in lista:
        if objeto.get(campo_id) == id_antigo:
            objeto_atualizar = objeto
            break

    if objeto_atualizar:
        print("\nInsira os dados novos\n")
        objeto_atualizar[campo_id] = verifica_inteiro(campo_id)
        for campo in campo_int:
            objeto_atualizar[campo] = verifica_inteiro(campo)
        for campo in campo_str:
            objeto_atualizar[campo] = input(f"{campo}: ")

    else:
        print("Pessoa não encontrada")
    
    escrever_arquivo(lista, arquivo)

################# exclusão #################
def excluir(arquivo: str) -> None:
    print("===== Exclusão =====")
    while True: # loop para verificar erro no input
        try:
            id_excluir = int(input("Insira o codigo: "))
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

    if option == '1':
        gerenciamento_operacoes("ESTUDANTES", ARQUIVO_ALUNO, "codigo", [], "nome", "cpf")
    elif option == '2':
        gerenciamento_operacoes("PROFESSORES", ARQUIVO_PROFESSOR, "codigo", [], "nome", "cpf")
    elif option == '3':
        gerenciamento_operacoes("DISCIPLINAS", ARQUIVO_DISCIPLINA, "codigo", [], "disciplina")
    elif option == '4':
        gerenciamento_operacoes("TURMAS", ARQUIVO_TURMA, "codigo", ["professor", "disciplina"])
    elif option == '5':
        gerenciamento_operacoes("MATRICULAS", ARQUIVO_MATRICULA, "codigo", ["aluno"])
    elif option == '9':
        print("Finalizando aplicação...")
        break
    else:
        print("Opção inválida")