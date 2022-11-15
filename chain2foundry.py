import json
import argparse
from etherscan_parser import Parser
from files_manager import Manager
from termcolor import cprint

# Arguments parsing
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument(
	'-a', '--address', 
	dest='address', 
	type=str, 
	default="",
	required=True,
	help="Contract address"
)
argument_parser.add_argument(
	'-n', '--network', 
	dest='network', 
	type=str, 
	default="mainnet",
	help="Network the contract is deployed on (default:mainnet / goerli)"
)
argument_parser.add_argument(
	'-k', '--api-key', 
	dest='api-key', 
	type=str, 
	default="VBX8N7APZM6Q2S4FTIRWYWRXPG4P3KG1NG",
	help="Etherscan API key (default: None)"
)
argument_parser.add_argument(
	'-o', '--output', 
	dest='output_dir', 
	type=str, 
	help="Output directory"
)
argument_parser.add_argument(
	'-f', '--force', 
	action='count',
	dest='force',
	default=0,
	help="Overwrite the output directory if it already exists"
)
args = vars(argument_parser.parse_args())

# Fetch source code from etherscan API
etherscanObj = Parser(args["address"], args["api-key"])
print("Fetching the contract source code from Etherscan API...")
try:
	json_result = etherscanObj.get_contract()
except Exception as error:
	cprint("[ERROR] Error while fetching the source code: %s" % error,"red",attrs=["bold"])

# Output directory mgmt
if(args["output_dir"] == None):
	args["output_dir"] = "projects/%s" % etherscanObj.contract_name
filesManager = Manager(args["output_dir"], args["force"], etherscanObj.compiler_version, etherscanObj.contract_name)

# Loop
for contract in json_result["sources"]:
	filesManager.create(contract, json_result["sources"][contract]["content"])

cprint("Done ! gl hf fren :)" ,"green",attrs=["bold"])