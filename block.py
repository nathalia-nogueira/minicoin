import hashlib
import datetime

class Block:
  def __init__(self, owner, operation, value, previousHash='0'):
    self.owner = owner
    self.operation = operation
    self.value = value 
    self.timestamp = datetime.datetime.now()
    self.previousHash = previousHash
    self.hash = self.calculateHash() 
    self.next = None 

  def calculateHash(self):
    data = f"{self.owner}{self.operation}{self.value}{self.timestamp}{self.previousHash}"
    return hashlib.sha256(data.encode()).hexdigest()