from block import Block

class Blockchain:  
    OP_OPEN_ACCOUNT = "open-account"
    OP_DEPOSIT = "deposit"
    OP_WITHDRAWAL = "withdrawal"
  
    def __init__(self, owner, initialValue):
        firstBlock = Block(owner, self.OP_OPEN_ACCOUNT, initialValue)
        self.head = firstBlock
        self.tail = firstBlock

    def addBlock(self, operation, value):
        if operation == self.OP_WITHDRAWAL and value > self.calculateBalance():
            print("Erro: retirada inválida (saldo insuficiente)")
            return -1
    
        newBlock = Block(self.tail.owner, operation, value, self.tail.hash)
        self.tail.next = newBlock
        self.tail = newBlock
        return 1
    
    def printBlockchain(self):
        currentBlock = self.head
        while currentBlock:
            print(f"Operação: {currentBlock.operation}, Valor: {currentBlock.value}, Hash: {currentBlock.hash[:10]}")
            currentBlock = currentBlock.next
  
    def calculateBalance(self):
        balance = self.head.value

        currentBlock = self.head.next
        while currentBlock:
            if currentBlock.operation == self.OP_DEPOSIT:
                balance += currentBlock.value
            elif currentBlock.operation == self.OP_WITHDRAWAL:
                balance -= currentBlock.value
            currentBlock = currentBlock.next
    
        return balance