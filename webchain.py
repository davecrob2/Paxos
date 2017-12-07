from flask import Flask
from flask import request
import requests
import glob
from blockpractice import *
import time
import json
from flask import render_template

node = Flask(__name__)

#node_blocks = sync()
@node.route('/')
def login():
	return(render_template('miner.html'))

@node.route('/test',methods = ['GET','POST'])
def test():
	if request.method == 'POST':
		result = request.form
		return(render_template('result.html',id = result))


@node.route('/blockchain',methods=['GET'])
def blockchain():
    make_chain()
    with open("D:\\Coding\\Python\chaindata\\chain\\blockchain.json",'r') as ch:
    	chain = json.load(ch)
    return("Chain =" + json.dumps(chain))



node_updates = []
peer_nodes = []
this_nodes_patients = []

#Method to receive data as a POST request. This is how patient data will be submited
#for now. In the future, this will have to interact with an API to pull database
#updates ever-so-often.
@node.route('/ehr_update',methods=['POST'])
def ehr_update():
	if request.method == 'POST':
		ehr_update = request.get_json()
		this_nodes_patients.append(ehr_update)
		print("Update data submitted" + json.dumps(ehr_update))
		return("EHR submission successful")


#applicable to multiple nodes later
@node.route('/blocks',methods=['GET'])
def get_blocks():
	chain_to_send = json.dumps(sync())
	return(chain_to_send)
#Applicable to multiple nodes later
def find_new_chains():
	other_chains = []
	for node_url in peer_nodes:
		block = requests.get(node_url+"/blocks").content
		other_chains.append(block)
	return(other_chains)
#applicable to multiple nodes later
def consensus():
	other_chains = find_new_chains()
	longest_chain = blockchain()
	for chain in other_chains:
		if len(longest_chain) < len(chain):
			longest_chain = chain
	node_blocks = longest_chain

#The paxos_client function takes the blocks as a list input and determines the block that 
#was mined first through iterating through the nonces produced. The output of this function
#is the block that contains the id of the miner. This will be the client in the Paxos system.
def paxos_client(blocks):
	blocks = blocks
	rank_list = []
	for b in blocks:
		rank_list.append(b['nonce'])
	client_block_nonce = min(rank_list)

	for b in blocks:
		if b['nonce'] == client_block_nonce:
			client = b
	return(client)



#Proof of work function. Easy way to test the blockchain for now.
#If the nonce of the last block divided by 1 is > 0, a block will be mined.
def proof_of_work(last_proof):
	incrementor = last_proof + 1
	while not (incrementor > 0):
		incrementor +=1
	return(incrementor)


#Method to mine the block. Opens the last block file on the local machine
#Stores the nonce of the last_block as the last_proof and starts the proof_of_work function.
#When the node completes the PoW, the data from this node is stored in the new block data,
#the index is incremented, and the hash of the previous block is added as Previous_hash for
#the new block. Finally, the mined block is stored in a json in the block directory.
#How often should we mine? If we grab updates every 10 minutes, maybe mine every 15?
@node.route('/mine',methods = ['GET','POST'])
def mine():
	
	if request.method == 'POST':
		result = request.form
		ident = result['ID']

		list_of_block_files = glob.glob("D:\\Coding\\Python\\chaindata\\blocks\\*.json")
		last_block_file = max(list_of_block_files, key=os.path.getctime)
		with open(last_block_file,'r') as lb:
			last_block = json.load(lb)
		last_proof = last_block['nonce']
		proof = proof_of_work(float(last_proof))
		this_nodes_patients.append(result)
		print("Mine successful.")
		#Will have to work in the Paxos_client function
		new_block_data = this_nodes_patients
		new_block_index_int = int(last_block['index']) + 1
		new_block_index = str(new_block_index_int)
		last_block_hash = last_block['hash']
		
		mined_block = Block(new_block_index,new_block_data,last_block_hash)

		#this_nodes_patients[:] = []

		mined_block_file =mined_block.__dict__()

		with open('D:\\Coding\\Python\chaindata\\blocks\\block%s.json' % new_block_index,'w') as f:
			block_dump = json.dumps(mined_block_file)
			f.write(block_dump)

		return (render_template('result.html',block = block_dump,id = ident))
	

if __name__ == '__main__':
    node.run()


