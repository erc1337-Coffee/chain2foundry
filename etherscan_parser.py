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
		else:
			self.etherscan_url = "api-goerli.etherscan.io"
	def get_contract(self):
		url = "https://%s/api?module=contract&action=getsourcecode&address=%s&apikey=%s" % (self.etherscan_url, self.address, self.api_key)
		json_result = json.loads(json.loads(requests.get(url).content)["result"][0]["SourceCode"][1:][:-1])
		self.contract_name = json.loads(requests.get(url).content)["result"][0]["ContractName"]
		self.compiler_version = json.loads(requests.get(url).content)["result"][0]["CompilerVersion"]
		if(json_result["language"] != "Solidity"):
			cprint("[ERROR] Contract language is not Solidity","red",attrs=["bold"])
			exit(1)
		return json_result