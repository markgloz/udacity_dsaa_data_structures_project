from hashlib import sha256
from time import gmtime, strftime
import json
from flask import Flask, request

class Block:
    def __init__(self, timestamp, data, previous_hash, index, nonce = 0) -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = None
        
    def calc_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True).encode('utf-8')
        return sha256(block_string).hexdigest()
    
    def __repr__(self) -> str:
        return (f"Block[Index: {self.index}, Timestamp: {self.timestamp}, Data: {self.data}, " +
                f"Previous Hash: {self.previous_hash}, Hash: {self.hash}]")


class BlockChain:
    def __init__(self, difficulty = 2) -> None:
        self.head = None
        self.difficulty = difficulty
        self.not_verified = []
        self.chain = []
        self.hashmap = {}
    
    def add_data(self, data):
        self.not_verified.append(data)
    
    def mine(self):
        if not self.not_verified:
            return False
        timestamp = strftime("%H:%M %d/%m/%Y", gmtime())
        previous_hash = self.head.hash if self.head else '0'
        block = Block(timestamp, self.not_verified, previous_hash, len(self.chain))
        hash_proof = self.proof_of_work(block)
        result = self.add_block(block, hash_proof)
        if result:
            self.not_verified = []
            return block.hash
        else:
            return False
    
    def proof_of_work(self, block: Block) -> str:
        hash = block.calc_hash()
        while not hash.startswith('0' * self.difficulty):
            block.nonce += 1
            hash = block.calc_hash()
        return hash

    def add_block(self, block: Block, hash_proof: str):
        if self.head:
            if block.previous_hash != self.head.hash:
                return False
        if self.verify(block, hash_proof):
            block.hash = hash_proof
            self.head = block
            self.chain.append(block)
            self.hashmap[block.hash] = block
            return True
        else:
            return False

    def verify(self, block: Block, hash_proof: str):
        return hash_proof.startswith('0' * self.difficulty) and hash_proof == block.calc_hash()

    def get_block_from_index(self, index):
        if not self.chain or index >= len(self.chain):
            return None
        else:
            return self.chain[index]
    
    def get_blockchain(self):
        blockchain_str = "["
        for block in self.chain:
            blockchain_str += f" {block},"
        blockchain_str += "]"
        return str(self.chain)
        # return blockchain_str
    
    def get_block_from_hash(self, hash):
        if hash in self.hashmap:
            return self.hashmap[hash]
        else:
            return None
    
    def get_blockchain_linked_list(self):
        if not self.head:
            return None
        blockchain_str = ""
        block = self.head
        while block:
            blockchain_str += f"{block} "
            previous_hash = block.previous_hash
            block = self.hashmap[previous_hash]
        return blockchain_str
            

app = Flask(__name__)
blockchain = BlockChain(difficulty=3)

@app.route('/blockchain', methods=["GET"])
def get_blockchain():
    return json.dumps(blockchain.get_blockchain())

@app.route('/add_data', methods=["POST"])
def add_data():
    data = request.json
    blockchain.add_data(data)
    return json.dumps(data)

@app.route('/mine', methods = ["GET"])
def mine():
    result = blockchain.mine()
    if result:
        return json.dumps(f"Mining succeeded. Hash of mined block: {blockchain.head.hash}")
    else:
        return json.dumps("Mining failed")

def tests():
    # Test case 1 - Normal use case.Add data, mine the block.
    # If successful, it will return a hash of the mined block added to the blockchain.
    block_chain = BlockChain(difficulty=2)
    block_chain.add_data("We are going to encode this string of data!")
    block_chain.add_data("Different data")
    mined_block_hash_1 = block_chain.mine()
    block_chain.add_data("More different data")
    mined_block_hash_2 = block_chain.mine()
    assert block_chain.get_block_from_hash(mined_block_hash_1) is not None
    assert block_chain.get_block_from_hash(mined_block_hash_2) is not None

    # Test case 2 - Null
    block_chain = BlockChain()
    block_chain.add_data(None)
    mined_block_hash = block_chain.mine()
    assert block_chain.get_block_from_hash(mined_block_hash) is not None

    # Test case 3 - Empty
    block_chain = BlockChain()
    block_chain.add_data("")
    mined_block_hash = block_chain.mine()
    assert block_chain.get_block_from_hash(mined_block_hash) is not None

    # Test case 4 - Very large values
    block_chain = BlockChain(difficulty = 4)
    block_chain.add_data("Some very large string" * 10 ** 3)
    mined_block_hash = block_chain.mine()
    assert block_chain.get_block_from_hash(mined_block_hash) is not None


if __name__ == "__main__":
    tests()
    app.run(debug = True, port = 5000)
    # curl http://127.0.0.1:5000/blockchain
    # curl -X POST -H "Content-Type: application/json" -d '"Hello World"' http://127.0.0.1:5000/add_data
    # curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/mine
    # curl http://127.0.0.1:5000/blockchain
