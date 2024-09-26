import json

################# variáveis de arquivos #################
ARQUIVO_ALUNO = "alunos.json"
ARQUIVO_PROFESSOR = "professores.json"
ARQUIVO_DISCIPLINA = "disciplinas.json"
ARQUIVO_TURMA = "turmas.json"
ARQUIVO_MATRICULA = "matriculas.json"


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

def gerenciamento_operacoes(escolha: str, arquivo: str, campo_id: str = "", campo_int: list = [], campo_str: list = []) -> None:
    while True:
        print(f"\n***** [{escolha}] MENU DE OPERAÇÕES *****")
        action = menu_operacoes()

        print()
        if action == '1': # Incluir
            if escolha == "MATRICULAS":
                incluir_relacao(arquivo, ARQUIVO_TURMA, ARQUIVO_ALUNO, "turma", "aluno")
            elif escolha == "TURMAS":
                incluir_relacao(arquivo, ARQUIVO_DISCIPLINA, ARQUIVO_PROFESSOR, "disciplina", "professor")
            else:
                incluir(arquivo, campo_id, campo_int, campo_str)
        elif action == '2': # Listar
            listar(arquivo)
        elif action == '3': # Atualizar
            if escolha == "MATRICULAS":
                editar_relacao(arquivo, ARQUIVO_TURMA, ARQUIVO_ALUNO, "turma", "aluno")
            elif escolha == "TURMAS":
                editar_relacao(arquivo, ARQUIVO_DISCIPLINA, ARQUIVO_PROFESSOR, "disciplina", "professor")
            else:
                editar(arquivo, campo_id, campo_int, campo_str)
        elif action == '4': # Excluir
            if escolha == "MATRICULAS":
                excluir_matricula(arquivo)
            else: excluir(arquivo)
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

def verificar_relacao(lista_relacao: list, id1: int, id2: int, key1, key2) -> bool:
    for relacao in lista_relacao:
        if id2 == relacao.get(key2) and id1 == relacao.get(key1):
            return True
    return False


# [x]: mudar a função excluir() e generalizar AAAAAAAA (acabou virando outra função: excluir_relacao())
# [x]: mudar a função editar() para incluir matricula (virou outra função também: editar_relacao())
# [x]: generalizar a função incluir_matricula() (só adicionar a turma nele)
# [x]: generalizar a função varificar_matricula() (também adicionar a turma nele)
# TODO: adicionar turma na função editar_relacao()
# TODO: dar uma olhada na função gerenciamento_operacoes() pra ver se tem algo pra mudar lá
# TODO: tentar achar um jeito de generalizar tudo

################# inclusão #################
def incluir(arquivo: str, campo_id: str, campo_int: list = [], campo_str: list = []) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)

    while True:
        id = verifica_inteiro(campo_id)
        if same_id(lista, id):
            print("CÓDIGO JÁ CADASTRADO!")
            print("INSIRA OUTRO CÓDIGO!")
        else: break

    novos_dados = {campo_id:id}

    for campo in campo_int:
        novos_dados[campo] = verifica_inteiro(campo)

    for campo in campo_str:
        novos_dados[campo] = input(f"{campo}: ")

    lista.append(novos_dados)

    escrever_arquivo(lista, arquivo)

def incluir_relacao(arquivo_relacao: str, arquivo1, arquivo2, key1, key2) -> None:
    print("===== Inclusão =====")
    lista_relacao = ler_arquivo(arquivo_relacao)
    lista1 = ler_arquivo(arquivo1)
    lista2 = ler_arquivo(arquivo2)
    relacao = {}

    if arquivo_relacao == ARQUIVO_TURMA:
        while True:
            relacao_id = verifica_inteiro("codigo")
            if same_id(lista_relacao, relacao_id):
                print(f"!!!Turma já existe!!!")
            else: 
                relacao["codigo"] = relacao_id
                break

    id1 = verifica_inteiro(f"Codigo da {key1}")
    if not same_id(lista1, id1):
        print(f"{key1} não existe")
        return
    
    id2 = verifica_inteiro(f"Codigo do {key2}")
    if not same_id(lista2, id2):
        print(f"{key2} não existe")
        return
    
    if not verificar_relacao(lista_relacao, id1, id2, key1, key2):
        relacao[key1] = id1
        relacao[key2] = id2
        lista_relacao.append(relacao)
        escrever_arquivo(lista_relacao, arquivo_relacao)
    else:
        print(f"\n!!{key2.upper()} JÁ CADASTRADO NA {key1.upper()}!!")


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
        while True:
            id_novo = verifica_inteiro(campo_id)
            if id_novo != id_antigo and same_id(lista, id_novo):
                print("!!!CÓDIGO JÁ CADASTRADO!!!")
                continue
            break
        objeto_atualizar[campo_id] = id_novo
        for campo in campo_int:
            objeto_atualizar[campo] = verifica_inteiro(campo)
        for campo in campo_str:
            objeto_atualizar[campo] = input(f"{campo}: ")
    else:
        print(f"{campo_id} não existe")
    
    escrever_arquivo(lista, arquivo)

def editar_relacao(arquivo_relacao: str, arquivo1, arquivo2, key1, key2) -> None:
    print("===== Inclusão =====")
    lista_relacao = ler_arquivo(arquivo_relacao)
    if not lista_relacao:
        print("Sem cadastros")
        return
    lista1 = ler_arquivo(arquivo1)
    lista2 = ler_arquivo(arquivo2)

    id1_antigo = verifica_inteiro(f"Código da {key1}")
    id2_antigo = verifica_inteiro(f"Código do {key2}")

    objeto_atualizar = None
    for objeto in lista_relacao:
        if objeto.get(key1) == id1_antigo and objeto.get(key2) == id2_antigo:
            objeto_atualizar = objeto
    
    if objeto_atualizar:
        print("Insira os dados novos")
        id1_novo = verifica_inteiro(f"Codigo da {key1}")
        if not same_id(lista1, id1_novo) and id1_novo != id1_antigo:
            print(f"{key1} não existe")
            return
        
        id2_novo = verifica_inteiro(f"Codigo do {key2}")
        if not same_id(lista2, id2_novo) and id2_novo != id2_antigo:
            print(f"{key2} não existe")
            return
        
        relacao_nova = {key1:id1_novo, key2:id2_novo}
        if (relacao_nova != objeto_atualizar and not verificar_relacao(lista_relacao, id1_novo, id2_novo, key1, key2)) or relacao_nova == objeto_atualizar:
            objeto_atualizar[key1] = id1_novo
            objeto_atualizar[key2] = id2_novo
            escrever_arquivo(lista_relacao, arquivo_relacao)
        else:
            print(f"\n!!{key2.upper()} JÁ CADASTRADO NA {key1.upper()}!!")
    else:
        print("Não existe")

################# exclusão #################
def excluir(arquivo: str, key: str = "codigo") -> None:
    print("===== Exclusão =====")

    id_excluir = verifica_inteiro(key)
    
    lista = ler_arquivo(arquivo)
    aluno_remover = None
    for aluno in lista:
        if aluno.get(key) == id_excluir:
            aluno_remover = aluno
    if aluno_remover:
        lista.remove(aluno_remover) 
    else:
        print("\nCódigo não existe")
    
    escrever_arquivo(lista, arquivo)

def excluir_matricula(arquivo: str) -> None:
    print("===== Inclusão =====")
    lista = ler_arquivo(arquivo)

    turma = verifica_inteiro("Código da turma")
    aluno = verifica_inteiro("Código do aluno")
    matricula_remover = None
    for matricula in lista:
        if matricula.get("turma") == turma and matricula.get("aluno") == aluno:
            matricula_remover = matricula
    if matricula_remover:
        lista.remove(matricula_remover)
    else:
        print("\nMatricula não existe")

    escrever_arquivo(lista, arquivo)


################# loop menu principal #################   
while True:
   
    option = menu_principal()

    if option == '1':
        gerenciamento_operacoes("ESTUDANTES", ARQUIVO_ALUNO, "codigo", [], ["nome", "cpf"])
    elif option == '2':
        gerenciamento_operacoes("PROFESSORES", ARQUIVO_PROFESSOR, "codigo", [], ["nome", "cpf"])
    elif option == '3':
        gerenciamento_operacoes("DISCIPLINAS", ARQUIVO_DISCIPLINA, "codigo", [], ["disciplina"])
    elif option == '4':
        gerenciamento_operacoes("TURMAS", ARQUIVO_TURMA)
    elif option == '5':
        gerenciamento_operacoes("MATRICULAS", ARQUIVO_MATRICULA)
    elif option == '9':
        print("Finalizando aplicação...")
        break
    else:
        print("Opção inválida")
