import datetime

def mostrar_menu():
    """
    Função que exibe o menu principal do sistema.
    """
    
    print("""
    =-=-=-=-=-=-=-= Menu Principal =-=-=-=-=-=-=-=
          1. Depositar
          2. Sacar
          3. Consultar extrato
          4. Cadastrar usuário
          5. Criar conta
          6. Sair
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    """)

def depositar(saldo, transacoes, limite_trans):
    """
    Função para realizar depósitos na conta.
    
    Parâmetros:
    saldo (int): Saldo atual da conta.
    transacoes (list): Lista com os dicionários das transações.
    limite_trans (int): Limite diário de transações.

    Returns:
    int: Saldo após o depósito.
    int: Limite diário de transações restantes.
    """
    if limite_trans == 0:
        print("Limite diário de transações atingido.")
        return saldo, limite_trans
    
    while True:
        try: # Validando se será um número inteiro
            valor = int(input("Digite o valor do depósito: "))
            print("")
        
            if valor <= 0: # Validando que será um número positivo
                print("Valor inválido. Não é possível depositar valores negativos ou iguais a zero.")
                continue
            elif valor > 0:
                saldo += valor
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                limite_trans -= 1 # Diminui o limite de transações
                transacoes.append({
                    "tipo": "Depósito",
                    "valor": valor,
                    "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                })
                break
            else:
                print("Valor inválido. Tente novamente.")
                continue
        except ValueError:
            print("Valor inválido. É possível depositar somente números inteiros.")
            continue
    return saldo, limite_trans

def saque(saldo, limite_diario, transacoes, limite_trans, limite_saque):
    """
    Função para realizar saques na conta.
    
    Parâmetros:
    saldo (int): Saldo atual da conta.
    limite_diario (int): Limite diário de saques.
    transacoes (list): Lista com os dicionários das transações.
    limite_trans (int): Limite diário de transações.
    limite_saque (int): Limite máximo de saque.

    Returns:
    int: Saldo após o saque.
    int: Limite diário de saques restantes.
    int: Limite diário de transações restantes.
    """
    if limite_saque == 0:
        print("Limite diário de saques atingido.")
        return saldo, limite_diario, limite_trans
    
    while True:
        try: # Validando se será um número inteiro
            valor = int(input("Digite o valor do saque: "))
            print("")

            if valor <= 0:
                print("Valor inválido. Não é possível sacar valores negativos ou iguais a zero.")
                continue
            elif valor > saldo:
                print("Valor inválido. Saldo não disponível.")
                continue
            elif valor > limite_saque:
                print(f"Valor inválido. O limite de saque é de R$ {limite_saque:.2f}.")
                continue
            elif limite_diario == 0:
                print("Limite diário de saques atingido.")
                break
            else:
                saldo -= valor
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                limite_diario -= 1 # Diminui o limite diário de saques
                limite_trans -= 1 # Diminui o limite de transações
                print(f"Você ainda pode sacar {limite_diario} vezes hoje.")
                transacoes.append({
                    "tipo": "Saque",
                    "valor": valor,
                    "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                })
                break
        except ValueError:
            print("Valor inválido. É possível sacar somente números inteiros.")
            continue
    return saldo, limite_diario, limite_trans

def extrato(saldo, transacoes):
    """
    Função para consultar o extrato da conta.
    Informa todos os depósitos, saques e saldo atual.
    
    Parâmetros:
    saldo (int): Saldo atual da conta.
    transacoes (list): Lista com os dicionários das transações.
    
    Returns:
    str: Extrato atualizado.
    """

    print("\n=-=-=-=-=-=-=-=-= Extrato =-=-=-=-=-=-=-=-=-=-=")
    if not transacoes:
        print("Não foram encontrados lançamentos.")
    else:
        for t in transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f} - {t['data']}")

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Saldo atual: R$ {saldo:.2f}")

def cadastrar_usuario(usuarios):
    """
    Efetua o cadastro do usuário.

    Parâmetros:
    usuarios (list): Lista com os usuários já cadastrados.
    
    Returns:
    None
    """

    print("\n=-=-=-=-=-=-= Cadastro de Usuário =-=-=-=-=-=-=-=-=")

    cpf = input("Digite seu CPF (somente números): ").strip()

    for user in usuarios:
        if user["cpf"] == cpf:
            print("CPF já cadastrado.")
            return
    
    nome = input("Digite seu nome: ").strip()
    data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ").strip()

    print("\nEndereço:")
    rua = input("Rua: ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("Estado (sigla): ").strip()

    endereco = f"{rua}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })

    print("Usuário cadastrado com sucesso!")

def conta_bancaria(contas, usuarios):
    """
    Função principal que inicia o sistema bancário.
    
    Parâmetros:
    contas (list): Lista com as contas já cadastradas.
    usuarios (list): Lista com os usuários já cadastrados.

    Returns:
    None
    """
    
    print("=-=-=-=-=-=-=-= Cadastro de Conta =-=-=-=-=-=-=-=-=")
    cpf = input("Digite seu CPF (somente números): ").strip()

    for user in usuarios:
        if user["cpf"] == cpf:
            contas.append({
                "cpf": user["cpf"],
                "número da conta": len(contas) + 1,
                "agência": "0001",
            })

            print(f"\nOlá, {user['nome']}! Conta criada com sucesso.")
            print("Número da conta:", len(contas))
            print("Agência: 0001")
            return

    print("Usuário não encontrado. Verifique o CPF ou cadastre o usuário primeiro.")

saldo = 0 # Inicializa o saldo
limite_saque = 500 # Define o limite de saque
limite_diario = 3 # Define o limite diário de saques
limite_trans = 10 # Define o limite diário de transações
transacoes = [] # Inicializa a lista de transações
usuarios = [] # Inicializa a lista de usuários
contas = [] # Inicializa a lista de contas

# Programa principal
print("""
    =-=-=-=-=-=-=-= Sistema Bancário =-=-=-=-=-=-=-=
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    """)

while True:
    try:
        mostrar_menu() # Chama a função do menu principal
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            saldo, limite_trans = depositar(saldo, transacoes, limite_trans)
        elif opcao == 2:
            saldo, limite_diario, limite_trans = saque(saldo, limite_diario, transacoes, limite_trans, limite_saque)
        elif opcao == 3:
            extrato(saldo, transacoes)
        elif opcao == 4:
            cadastrar_usuario(usuarios)
        elif opcao == 5:
            conta_bancaria(contas, usuarios)
        elif opcao == 6:
            print("Saindo do sistema, até a próxima!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue
    except ValueError:
        print("Opção inválida. Digite o número de uma opção válida.")
        continue
