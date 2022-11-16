import os
import shutil
import re
from termcolor import cprint

class Manager(object):
	def __init__(self, output_directory, force, compiler_version, contract_name):
		super(Manager, self).__init__()
		self.output_directory = output_directory
		self.force = force
		self.compiler_version = compiler_version
		self.contract_name = contract_name
		self.is_library = False
		try:
			#os.makedirs(self.output_directory, exist_ok= self.force)
			cprint("Creating project %s at %s" % (self.contract_name, self.output_directory),"blue",attrs=["bold"])
			shutil.copytree('FoundryTemplate/', '%s/' % (self.output_directory), dirs_exist_ok=self.force)
		except OSError as error: 
			cprint("[ERROR] The output directory is already existing, use the -f or --force argument to overwwrite it","red",attrs=["bold"])
			exit(1)
	def create(self, filename, content):
		if(filename.startswith('@')):
			self.is_library = True
			filename = filename.split('contracts/')[1]
		else:
			try:
				filename = filename.split('contracts/')[1]
			except:
				if not ".sol" in filename:
					filename += ".sol"
		path = '%s/src/%s' % (self.output_directory, filename)
		basedir = os.path.dirname(path)
		if not os.path.exists(basedir):
			os.makedirs(basedir)
		# edit libraries from remote to local by removing the @ in the import
		content_parsed = ""
		for line in content.split('\n'):
			if('import "@' in str(line)):
				line = 'import "./%s' % line.split('contracts/')[1]
			content_parsed += "%s\n" % line
		# dirty tweak to remove any non UTF-8 char
		content_parsed = content_parsed.encode('ascii', 'ignore').decode('utf-8', 'ignore')
		with open(path, 'w') as f:
			f.write(content_parsed)
		if not self.is_library:
			script_path = "%s/script/%s" % (self.output_directory, filename.replace('.sol', '.s.sol'))
			test_path = "%s/test/%s" % (self.output_directory, filename.replace('.sol', '.t.sol'))
			basedir = os.path.dirname(script_path)
			if not os.path.exists(basedir):
				os.makedirs(basedir)
			with open(script_path, 'w') as f:
				f.write(self.generate_script_files(filename))
			basedir = os.path.dirname(test_path)
			if not os.path.exists(basedir):
				os.makedirs(basedir)
			with open(test_path, 'w') as f:
				f.write(self.generate_test_files(filename))
	def generate_script_files(self, filename):
		solidity_version = re.findall(r'\d{0,2}\.\d{0,2}\.\d{0,2}',self.compiler_version)[0]
		return("""// SPDX-License-Identifier: UNLICENSED
pragma solidity ^%s;

import "forge-std/Script.sol";

contract %sScript is Script {
    function setUp() public {}

    function run() public {
        vm.broadcast();
    }
}
		""" % (solidity_version, self.contract_name))
	def generate_test_files(self, filename):
		solidity_version = re.findall(r'\d{0,2}\.\d{0,2}\.\d{0,2}',self.compiler_version)[0]
		return("""// SPDX-License-Identifier: UNLICENSED
pragma solidity ^%s;

import "forge-std/Test.sol";
import "../src/%s.sol";

contract %sTest is Test {
    %s public my_contract;
    function setUp() public {
       my_contract = new %s();
    }
}
		""" % (solidity_version, self.contract_name, self.contract_name, self.contract_name, self.contract_name))



