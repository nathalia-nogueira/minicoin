'''
Classe Bloco
Autoras:
  NOME                    | LOGIN | GRR 
- Bianca Mendes Francisco | bmf23 | 20234263
- Nathália Nogueira Alves | nna23 | 20232349
'''

import hashlib
import datetime

class Block:
    # Construtor
    def __init__(self, owner, operation, value, previousHash='0'):
        self.owner = owner
        self.operation = operation
        self.value = value 
        self.timestamp = datetime.datetime.now()
        self.hash = self.calculateHash(previousHash) 
        self.next = None 

    # Calcula o hash com base nos próprios dados e hash anterior
    def calculateHash(self, previousHash):
        data = f"{self.owner}{self.operation}{self.value}{self.timestamp}{previousHash}"
        return hashlib.sha256(data.encode()).hexdigest()