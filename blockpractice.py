import hashlib as hasher
import time
import uuid
import os
import json
import glob
#This is a class that defines what a Block contains.
#Blocks must have an index, data, previous_hash, and a timestamp (or nonce)
class Block:
	def __init__(self,index,data,previous_hash):
		self.nonce = time.time()
		self.data = data
		self.index = index
		self.previous_hash = previous_hash
		self.hash=self.hash_block()
	#This allows us to take the class attributes and assemble them into a dictionary if we want
	#All the elements are stored as strings and returned as a dictionary
	def __dict__(self):
		records = {}
		records['index'] = str(self.index)
		records['previous_hash'] = str(self.previous_hash)
		records['data'] = repr(self.data)
		records['nonce'] = str(self.nonce)
		records['hash']=str(self.hash)
		return(records)

	#This function hashes the current block data, nonce, index, and previous hash
	def hash_block(self):
		sha = hasher.sha256()
		sha.update(str(self.index).encode('utf-8')+
			str(self.nonce).encode('utf-8')+
			str(self.data).encode('utf-8')+
			str(self.previous_hash).encode('utf-8'))
		return(sha.hexdigest())


#This generates unique ids for users that would like to join the network
#I need to have the user request an API-key and store the username and their key in a database 
#so that when they want to access the network, they can identify themselves
def id_gen(number):
	number = number
	ids = []
	for times in range (0,number):
		ids.append(str(uuid.uuid4()))
	return(ids)


#Creating the Genesis Block and adding it to the block chain
#This takes no arguments and returns the following block {'index':0,'data':'This is the Genesis Block', 'previous_hash':None,'nonce':TBD}   
def genesis_block():
	block_data = {}
	block_data['index']=0
	block_data['previous_hash']=None
	block_data['data']='This is the Genesis Block'
	block = Block(block_data['index'],block_data['data'],block_data['previous_hash'])
	return(block)
	

#This needs to be updated in the future. This is the directory in which to store the blockchain locally.
#The function checks if the directory exists, then creates the directory.
#Next, the genesis block is added as a json file to the directory.
#If a genesis block is created already, it returns the message 'Genesis block already created.'
chaindata_dir = 'blocks'
if not os.path.exists(chaindata_dir):
	os.mkdir(chaindata_dir)

first_block = genesis_block()
if os.listdir(chaindata_dir)==[]:
	with open('D:\\Coding\\Python\chaindata\\'+chaindata_dir+'\\block%s.json' % first_block.index,'w') as f:
			  data = json.dumps(first_block.__dict__())
			  f.write(data)
else:
	print("Genesis block already created.")
#End of Genesis block creation


#Pulling the individual block files and assembling them into a chain
#on this particular node by storing the chain in local_chain.
#So basically the blockchain for this particular node is 'local_chain'
#The function looks in the chaindata directory, finds all json files and opens
#the second to last file and last file. Next, it appends the last file to the 
#second to last file to update the chain    
def make_chain():
	local_chain = []
	list_of_block_files = glob.glob("D:\\Coding\\Python\chaindata\\blocks\\*.json")
	last_block = max(list_of_block_files, key=os.path.getctime)

	if len(list_of_block_files) == 1:
		with open(last_block,'r') as lb:
			lb_data = json.load(lb)
			local_chain=[lb_data]
		os.makedirs(os.path.dirname('D:\\Coding\\Python\\chaindata\\chain\\blockchain.json'))
		with open('D:\\Coding\\Python\\chaindata\\chain\\blockchain.json','w') as f:
			data = json.dumps(local_chain)
			f.write(data)
	else: 
		with open(last_block,'r') as lb, open("D:\\Coding\\Python\\chaindata\\chain\\blockchain.json",'r') as ch:
			lb_data = json.load(lb)
			ch_data = json.load(ch)
			ch_data.append(lb_data)
		with open('D:\\Coding\\Python\\chaindata\\chain\\blockchain.json','w') as f:
			updated_chain = json.dumps(ch_data)
			f.write(updated_chain)
			local_chain = updated_chain
	return("Chain updated" + str(local_chain))

# class EHR(object):
#     def __init__(self,privatekey,data):
#         self.privatekey = privatekey
#         self.data = data
