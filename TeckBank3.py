from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime
from textwrap import dedentp

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco 
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adiconar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nov_conta(cls, cliente, numero):
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
        return self.saldo
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(f'Não foi possivel realizar a transação, saldo insuficiente\nSeu saldo é R${self.saldo}')
        elif valor > 0:
            self._saldo -= valor
            print(f'Saque no valor de R${valor} realizado com sucesso')
            return True
        else:
            print('Erro, tente novamente')
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Deposito de R${valor} realizado com sucesso')
        else:
            print('Erro, tente novamente')
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3 ):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
    
    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.
            transacoes if transacao['tipo'] = Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque >= self.limite_saque

        if excedeu_limite:
            print(f'Erro, o valor não pode ser maior que o {self.limite}')
        elif excedeu_saque:
            print('Erro, limite de saques atingido')
        else:
            return super().sacar(valor)
        
        return False
    def __str__(self):
        return f'''
            Agência: \t{self.agencia}
            Conta: \t{self.numero}
            Agência: \t{self.cliente.nome}
        '''

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.new().strftime('%d/%m%y %H:%M:%S'),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

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

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.despositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
