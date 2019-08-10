import hashlib
import requests
import json
from time import time
from uuid import uuid4
import sys
from flask import Flask, jsonify, request
import logging
logging.basicConfig(filename='myLog_miner.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# TODO: Implement functionality to search for a proof 


# Instantiate our Node
#app = Flask(__name__)




#@app.route('/proof_of_work', methods=['GET'])
def proof_of_work(last_block_string):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    print("Starting work on a new proof...")
    proof = 0
    
    
    while valid_proof(last_block_string, proof) is False:
        proof += 1
    print("Attempting to mine...")
    return proof
    
    
    
    ##last_block = self.chain[-1]
    #last_hash = self.hash(last_block)

    #proof = 0
    # for block 1, hash(1, p) = 000000x
    
def valid_proof(last_block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    # build string to hash
    guess = f'{last_block_string}{proof}'.encode()
    #guess = f'{last_proof}{proof}'.encode()
    
    # use hash function
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    # check if 6 leading 0's in hash result
    beg = guess_hash[0:6]
            
    if beg == "000000":
        return True
    else:
        return False   


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        #app.run(host='localhost', port=8080)
        node = "http://localhost:5500"

    coins_mined = 0
    # Run forever until interrupted

    while True:
        # TODO: Get the last proof from the server and look for a new one
        r = requests.get(url = node + '/last_block_string')
        data = r.json()
        last_block_string = data['last_block_string'] ['previous_hash']

        # TODO: When found, POST it to the server {"proof": new_proof}

        # TODO: We're going to have to research how to do a POST in Python
        print(last_block_string)
        new_proof = proof_of_work(last_block_string)
        # HINT: Research `requests` and remember we're sending our data as JSON

        # TODO: If the server responds with 'New Block Forged'

        # add 1 to the number of coins mined and print it.  Otherwise,

        # print the message from the server.
        proof_data = {'proof': new_proof}
        r = requests.post(url = node + '/mine', json = proof_data)
        data = r.json()

        
        print(data)
        if data.get('message') == "New Block Forged":
        #if data.message == "New Block Forged":
            coins_mined += 1
            print("You have: " + str(coins_mined) + " coins")
        print(data.get('message'))