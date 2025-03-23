Bitcoin Transaction Simulation (P2PKH & P2SH-P2WPKH)
Overview
This project demonstrates how to create and analyze Bitcoin transactions using:

P2PKH (Legacy) Transactions
P2SH-P2WPKH (SegWit) Transactions
The program interacts with bitcoind using JSON-RPC to:

Generate Addresses (Legacy and SegWit)
Fund Addresses using sendtoaddress
Create Raw Transactions and decode scripts
Sign and Broadcast Transactions
Analyze Transactions and Compare P2PKH vs SegWit

Requirements
Before running the program, ensure you have:

Bitcoin Core (bitcoind) installed
Python 3+ installed
bitcoinrpc.authproxy library (install with pip install python-bitcoinrpc)
Bitcoin Core running in Regtest mode

Setup and Running the Program
1.Locate the File Location in the Terminal
Change directory to the Bitcoin Core binaries like for me: cd "C:\Users\thikm\Downloads\bitcoin-27.0-win64\bitcoin-27.0\bin"  

2️⃣ Start Bitcoin Core in Regtest Mode
Start bitcoind with transaction indexing enabled by running below code in the terminal:

.\bitcoind.exe -regtest -txindex  


3️⃣ Load or Create a Wallet
first create wallet like "testwallet"
load existing wallets by running below code in the another terminal:
bitcoin-cli -regtest loadwallet "testwallet"  

Running the Python Programs
4️⃣ Run the Python Programs in Separate Terminals
Run Part 1: P2PKH Transactions
Save the script as bitcoin_rpc.py and run it as 
python bitcoin_rpc.py  

Run Part 2: P2SH-P2WPKH Transactions
Save the script as p2sh_segwit.py and run it in another terminal as :
python p2sh_segwit.py 

5️⃣ Verify Transactions
Check unspent outputs: 
bitcoin-cli -regtest listunspent

View a specific transaction by running in the terminal as :

bitcoin-cli -regtest getrawtransaction <txid> 1  

Decode a scriptPubKey as:  
bitcoin-cli -regtest decodescript <scriptPubKey>  

6️⃣ Mining Blocks for Confirmation
Mine a block to confirm transactions as:
bitcoin-cli -regtest generate 1 

Check the wallet balance as: 
bitcoin-cli -regtest getbalance

7️⃣ Debugging and Transaction Analysis
Use Bitcoin Debugger to execute ScriptSig & ScriptPubKey.
Analyze scripts using getrawtransaction and decodescript.
Compare P2PKH and P2SH-P2WPKH transaction sizes and script structures.  


Final Notes
Ensure that bitcoind is always running when executing commands.
If listunspent returns empty, mine blocks to confirm transactions.
Use different terminals for running Python scripts and checking Bitcoin commands.# Allies
