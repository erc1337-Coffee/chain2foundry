<img src="logo.png" alt="erc1337 logo" align="right" width="120" />

# chain2foundry

**Generates a [Foundry](https://github.com/foundry-rs/foundry) project from a contract address**

[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-3/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Install
```
sudo apt install python3
sudo python3 -m pip install -r requirements.txt
```

## Usage
```
$ python3 chain2foundry.py

usage: chain2foundry.py [-h] -a ADDRESS [-n NETWORK] [-k API-KEY] [-o OUTPUT_DIR] [-f]

optional arguments:
  -h, --help            				Show this help message and exit

  -a ADDRESS, --address ADDRESS         Contract address

  -n NETWORK, --network NETWORK         Network the contract is deployed on (default:mainnet / goerli)

  -k API-KEY, --api-key API-KEY         Etherscan API key (default: a shared one)

  -o OUTPUT_DIR, --output OUTPUT_DIR    Output directory

  -f, --force                           Overwrite the output directory if it already exists
```

## Example
```
$ python3 chain2foundry.py -a 0x8A98E5c8211D20C6c1c82c78c46f5A0528062881 -f

Fetching the contract source code from Etherscan API...
Creating project ApeCoinStaking at projects/ApeCoinStaking
Done ! gl hf fren :)
```

## Todo

- [ ] Test it to find bugs and edge cases
- [ ] Automate tests creation
- [ ] Automate constructor arguments parsing
- [ ] How cool would it be if the script deployed contracts & populated them on an Anvil node with the same data as currently on-chain ?

