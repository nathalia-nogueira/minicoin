from blockchain import Blockchain

bc = Blockchain("Nathália", 100)
bc.addBlock("deposito", 50)
bc.addBlock("retirada", 30)
bc.printBlockchain()
balance = bc.calculateBalance()

print(f"current balance = {balance}")