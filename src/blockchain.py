'''
Classe "Corrente de blocos"
Autoras:
  NOME                    | LOGIN | GRR 
- Bianca Mendes Francisco | bmf23 | 20234263
- Nathália Nogueira Alves | nna23 | 20232349
'''

from block import Block

class Blockchain:  
    # "constantes" com nomes de operações
    OP_OPEN_ACCOUNT = "open-account"
    OP_DEPOSIT = "deposit"
    OP_WITHDRAWAL = "withdrawal"
  
    # Construtor
    def __init__(self, owner, initialValue):
        firstBlock = Block(owner, self.OP_OPEN_ACCOUNT, initialValue)
        self.head = firstBlock
        self.tail = firstBlock

    # Adiciona bloco
    def addBlock(self, operation, value):
        # Se for saque, verifica se é possível
        if operation == self.OP_WITHDRAWAL and value > self.calculateBalance():
            print("\033[31mErro: retirada inválida (saldo insuficiente)\033[0m")
            return 0
    
        # Cria e adiciona
        newBlock = Block(self.tail.owner, operation, value, self.tail.hash)
        self.tail.next = newBlock
        self.tail = newBlock
        return 1
    
    # Imprime os blocos da blockchain - usada para debug
    def printBlockchain(self):
        currentBlock = self.head
        while currentBlock:
            print(f"Operação: {currentBlock.operation}, Valor: {currentBlock.value}, Hash: {currentBlock.hash[:10]}")
            currentBlock = currentBlock.next
  
    # Calcula o saldo da conta
    def calculateBalance(self):
        balance = self.head.value

        # Percorre a blockchain somando movimentações
        currentBlock = self.head.next
        while currentBlock:
            if currentBlock.operation == self.OP_DEPOSIT:
                balance += currentBlock.value
            elif currentBlock.operation == self.OP_WITHDRAWAL:
                balance -= currentBlock.value
            currentBlock = currentBlock.next
    
        return balance