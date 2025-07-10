from abc import ABC, abstractproperty, abstractmethod  # importa classes abstratas
from datetime import datetime # para registrar data e hora das transações

# sistema de banco em POO

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente): # classe herda os atributos (endereco)
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco) # acesso a classe pai
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, saldo, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

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
            print("\n Operação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso ===")
            return True

        else:
            print("\n Operação falhou! O valor informado é inválido")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n Operação falhou! o valor informado é inválido.")
            return False

        return True

class ContaCorrente(Conta): # herança de (conta)
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor): # conta quantos saques já foram realizados
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\n Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome
        }"""

class Historico:
    def __init__(self):
        self._transacoes = [] # lista de transações

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # adiciona um dicionário com os dados da transação
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__, # nome da classe: Saque ou Deposito
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"), # Data e hora formatados
            }
        )

class Transacao(ABC):# classe abstrata para qualquer tipo de transação (interface)
    @property
    @abstractmethod
    def valor(self):
        # métdo obrigatório para retornar o valor da transação
        pass

    @abstractmethod
    def registrar(self, conta):
        # métdo obrigatório que deve ser implementado na subclasse
        pass

class Saque(Transacao): # precisa conter os metodos herdados de (transacao)
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor) # tenta sacar

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self) # adiciona ao histórico se True

class Deposito(Transacao): # precisa conter os metodos herdados de (transacao)
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


