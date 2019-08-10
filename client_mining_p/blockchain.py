# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
import logging
logging.basicConfig(filename='myLogs_blockchain.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

import functools
import time
import timeit



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        self.new_block(previous_hash=1, proof=99)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the BLock that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

        '''  def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm
        Find a number p such that hash(last_block_string, p) contains 6 leading
        zeroes
        """
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)

        proof = 0
        # for block 1, hash(1, p) = 000000x
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof  '''
        

    @staticmethod
    def valid_proof(last_block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?
        """
        # build string to hash
        guess = f'{last_block_string}{proof}'.encode()
        # use hash function
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        # check if 6 leading 0's in hash result
        beg = guess_hash[0:6]
             
        if beg == "000000":
            return True
        else:
            return False
 
  

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-------------------\n")
            # Check that the hash of the block is correct
            # TODO: Return false if hash isn't correct
            #if block['previous_hash'] != self.hash(last_block):
             #   return False

            # Check that the Proof of Work is correct
            # TODO: Return false if proof isn't correct
            # Check that the Proof of Work is correct
            #Delete the reward transaction
           # transactions = block['transactions'][:-1]
            # Need to make sure that the dictionary is ordered. Otherwise we'll get a different hash
            #transaction_elements = ['sender_address', 'recipient_address', 'value']
            #transactions = [OrderedDict((k, transaction[k]) for k in transaction_elements) for transaction in transactions]

            #if not self.valid_proof(transactions, block['previous_hash'], block['nonce'], MINING_DIFFICULTY):
            #    return False

            last_block = block
            current_index += 1

        return True


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    #proof = blockchain.proof_of_work(blockchain.last_block)
    values = request.get_json()
    #last_block = blockchain.chain[-1]
    
    #url = 'https://localhost:5500/proof_of_work'
   # last_proof = last_block
   # server_proof = requests.post(url, json = last_proof)
    required = ['proof']
    if not all(k in values for k in required):
        return 'Missing Values', 400
        
    
    if not blockchain.valid_proof(blockchain.last_block['previous_hash'], values['proof']):
        print("Error")
        # Error Message
        response = {
            'message': "Proof is invalid. May have already been submitted"

        }
        return jsonify(response), 200
    
    #proof = blockchain.proof_of_work(blockchain.last_block)
    # We must receive a reward for finding the proof.
    # TODO:
    # The sender is "0" to signify that this node has mine a new coin
    # The recipient is the current node, it did the mining!
    # The amount is 1 coin as a reward for mining the next block
    blockchain.new_transaction(0, node_identifier, 1)
    # Forge the new Block by adding it to the chain
    # TODO
    
    #previous_hash = blockchain.hash(last_block)
    #block = blockchain.new_block(proof, blockchain.hash(blockchain.last_block))
    block = blockchain.new_block(values['proof'], blockchain.hash(blockchain.last_block))
    # Send a response with the new block
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'currentChain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

#def timer(func):
    """Print the runtime of the decorated function"""
#    @functools.wraps(func)
#    def wrapper_timer(*args, **kwargs):
#        start_time = time.perf_counter()    # 1
#        value = func(*args, **kwargs)
#        end_time = time.perf_counter()      # 2
#        run_time = end_time - start_time    # 3
#        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
#        return value
#    return wrapper_timer

#@timer
#def waste_some_time(num_times):
#    for _ in range(num_times):
#        sum([i**2 for i in range(10000)]) 

@app.route('/last_block_string', methods=['GET'])
def last_block_string():
    #print("going through last_block_string")
    response = {
        'last_block_string': blockchain.last_block 
    }         
    
    
    return jsonify(response), 200


# Run the program on port 5500
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='localhost', port=5500)
