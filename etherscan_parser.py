import json
import requests
from termcolor import cprint

class Parser(object):
	"""Etherscan Parser used to fetch verified contract source code"""
	def __init__(self, address, network, api_key):
		super(Parser, self).__init__()
		self.address = address
		self.network = network
		self.api_key = api_key
		self.contract_name = None
		self.compiler_version = None
		if(network == "mainnet"):
			self.etherscan_url = "api.etherscan.io"
		elif(network == "goerli"):
			self.etherscan_url = "api-goerli.etherscan.io"
		elif(network == "arbi-main"):
			self.etherscan_url = "arbitrum-mainnet.infura.io"
	def get_contract(self):
		url = "https://%s/api?module=contract&action=getsourcecode&address=%s&apikey=%s" % (self.etherscan_url, self.address, self.api_key)
		data = json.loads(requests.get(url).content)["result"][0]

		# Check if the contract is verified
		if(data["ABI"] == "Contract source code not verified"):
			cprint("[ERROR] Contract not verified","red",attrs=["bold"])
			exit(1)
		
		# Check if the contract is a proxy
		if(int(data["Proxy"])):
			cprint("[ERROR] Contract is a proxy.. I'll fix that asap I swear. Expect bugs :(","red",attrs=["bold"])
		#	exit(1)

		self.contract_name = data["ContractName"]
		self.compiler_version = data["CompilerVersion"]

		# Dirty tweak to manage  one-file contract & multiple files contracts
		try:
			json_result = json.loads(data["SourceCode"][1:][:-1])
			json_result["multifile"] = True
		except:
			# Yeah that's ugly af, you can judge me here (but it works hehe) 
			json_result = json.loads("""{"sources": { "%s": { "content": %s }}}""" % (self.contract_name, json.dumps(data["SourceCode"].replace('"','\"')).replace('\\r\\n','\\n')))
			json_result["multifile"] = False
		return json_result