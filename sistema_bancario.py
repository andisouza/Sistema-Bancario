def mostrar_menu():
    """
    Função que exibe o menu principal do sistema.
    """
    
    print("""
    =-=-=-=-=-=-=-= Menu Principal =-=-=-=-=-=-=-=
          1. Depositar
          2. Sacar
          3. Consultar extrato
          4. Sair
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    """)

def depositar(saldo, depositos):
    """
    Função para realizar depósitos na conta.
    
    Parâmetros:
    saldo (int): Saldo atual da conta.
    depositos (list): Lista de depósitos realizados.
    
    Returns:
    int: Saldo após o depósito.
    """

    while True:
        try: # Validando se será um número inteiro
            valor = int(input("Digite o valor do depósito: "))
            print("")
        
            if valor <= 0: # Validando que será um número positivo
                print("Valor inválido. Não é possível depositar valores negativos ou iguais a zero.")
                continue
            if valor > 0:
                saldo += valor
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                depositos.append(valor) # Adiciona o valor do depósito à lista de depósitos
                break
            else:
                print("Valor inválido. Tente novamente.")
                continue
        except ValueError:
            print("Valor inválido. É possível depositar somente números inteiros.")
            continue
    return saldo

def saque(saldo, limite_diario, saques):
    """
    Função para realizar saques na conta.
    
    Parâmetros:
    saldo (int): Saldo atual da conta.
    limite_diario (int): Limite diário de saques.
    saques (list): Lista de saques realizados.
    
    Returns:
    int: Saldo após o saque.
    int: Limite diário de saques restantes.
    """

    while True:
        try: # Validando se será um número inteiro
            valor = int(input("Digite o valor do saque: "))
            print("")

            if valor <= 0:
                print("Valor inválido. Não é possível sacar valores negativos ou iguais a zero.")
                continue
            if valor > saldo:
                print("Valor inválido. Saldo não disponível.")
                continue
            if valor > limite_saque:
                print(f"Valor inválido. O limite de saque é de R$ {limite_saque:.2f}.")
                continue
            if limite_diario == 0:
                print("Limite diário de saques atingido.")
                break
            else:
                saldo -= valor
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                limite_diario -= 1
                print(f"Você ainda pode sacar {limite_diario} vezes hoje.")
                saques.append(valor) # Adiciona o valor do saque à lista de saques
                break
        except ValueError:
            print("Valor inválido. É possível sacar somente números inteiros.")
            continue
    return saldo, limite_diario

def extrato(saldo, depositos, saques):
    """
    Função para consultar o extrato da conta.
    Informa todos os depósitos, saques e saldo atual.
    
    Parâmetros:
    saldo (int): Saldo atual da conta.
    extrato (str): Extrato atual da conta.
    
    Returns:
    str: Extrato atualizado.
    """

    print("")
    print("=-=-=-=-=-=-=-=-= Extrato =-=-=-=-=-=-=-=-=-=-=")
    if not depositos and not saques:
        print("Não foram encontrados lançamentos.")
    else:
        if depositos:
            print("Depósitos:")
            for deposito in depositos:
                print(f"R$ {deposito:.2f}")
                print("")
        if saques:
            print("Saques:")
            for saque in saques:
                print(f"R$ {saque:.2f}")
                print("")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Saldo atual: R$ {saldo:.2f}")

saldo = 0 # Inicializa o saldo
limite_saque = 500 # Define o limite de saque
limite_diario = 3 # Define o limite diário de saques
depositos = [] # Inicializa a lista de depósitos
saques = [] # Inicializa a lista de saques

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
            saldo = depositar(saldo, depositos)

        elif opcao == 2:
            saldo, limite_diario = saque(saldo, limite_diario, saques)
        elif opcao == 3:
            extrato(saldo, depositos, saques)
            print("")
        elif opcao == 4:
            print("Saindo do sistema, até a próxima!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue
    except ValueError:
        print("Opção inválida. Digite o número de uma opção válida.")
        continue
