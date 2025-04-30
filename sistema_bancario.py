from datetime import datetime

from abc import ABC, abstractmethod, property

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao._valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Conta:
    def __init__ (self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n Saque realizado com sucesso!")
            return True
        
        else:
            print("\n Operação falhou! O valor informado é inválido.")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Depósito realizado com sucesso!")
        else:
            print("\n Operação falhou! O valor informado é inválido.")
            
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == Saque.
             __name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operação falhou! O valor do saque excede o limite.")
        
        elif excedeu_saques:
            print("\n Operação falhou! Número máximo de saques diários excedido.")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C>\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Cliente:
    def __init__(self, endereco, contas):
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento



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
