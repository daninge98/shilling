from web3 import Web3, HTTPProvider
import time
import setup as s
#import pdp
import json
import os

w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

IS_OUTSOURCING_PROOFS = False

import sys
sys.path.append('./posw')
from posw.posw import *

#####################################################################
#Logic starts here

print('Initialising PoT')
chi = verifier_init()
G = prover_init(chi)
challenge_gamma = verifier_challenge()
tau = prover_challenge(chi, G, challenge_gamma)
print(verifier_check(chi, G.node[BinaryString(0, 0)]['label'], challenge_gamma, tau))

prover_id = w3.eth.accounts[5]

#Get the genesis contract
genesis_contract = s.get_contract_instance(w3, s.genesis_address, "GenesisContract")

print("Waiting for a contract:")

#print(genesis_contract.getAvailableContracts())

# print(s.genesis_address)

# print(genesis_contract.getContract())
#genesis_contract.submitContract(storer_id,transact={'from': storer_id})
#print(genesis_contract.getContract())
contract_address = genesis_contract.getContract()
while contract_address == None:
    print(genesis_contract.getContract())
    time.sleep(1)
    contract_address = genesis_contract.getContract()

print("Accepting storage contract at address "+str(contract_address))

#Get an instance of the contract at the accepted address
current_contract = s.get_contract_instance(w3, contract_address, "RequestStorageContract")
current_contract.setStorer(storer_id, transact={'from': storer_id})

#records the number of proofs we have submitted so far
num_proofs_so_far = 0

print("Waiting for proof requests")
#respond to requests for proofs of storage
while True:
    time.sleep(1)
    proof_request_list = current_contract.getProofs()
    print(proof_request_list)
    if len(proof_request_list) > num_proofs_so_far:
        print("Proof requested at address "+str(num_proofs_so_far))
        #print(get_tags(60))
        time.sleep(4)
        #print("prove")
        #print(proof_request_list[num_proofs_so_far])
        proof = prove(proof_request_list[num_proofs_so_far], storer_id)
        
        #get this proof request
        this_proof = s.get_contract_instance(w3, proof_request_list[num_proofs_so_far], "StorageProof")
        this_proof.submitProof(proof, transact={'from': storer_id})
        num_proofs_so_far += 1
        print("Proof submitted for approval")
        exit()
        assert(False)

