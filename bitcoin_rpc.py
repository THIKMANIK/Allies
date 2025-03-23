from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Connect to the Bitcoin daemon (bitcoind)
rpc_user = "Allies"
rpc_password = "Allies4321@"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443", timeout=120)

# Ensure wallet is loaded (or create one if needed)
wallet_name = "testwallet"
try:
    rpc_connection.loadwallet(wallet_name)
except JSONRPCException as e:
    if "Wallet file not found" in str(e):
        rpc_connection.createwallet(wallet_name)


# Select the wallet for transactions
wallet_rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}", timeout=120)

# Generate three legacy addresses
address_A = wallet_rpc.getnewaddress("", "legacy")
address_B = wallet_rpc.getnewaddress("", "legacy")
address_C = wallet_rpc.getnewaddress("", "legacy")

print(f"Address A: {address_A}")
print(f"Address B: {address_B}")
print(f"Address C: {address_C}")

# Fund Address A (generate some regtest BTC first)
wallet_rpc.generatetoaddress(101, address_A)  # Mine 101 blocks to fund the wallet
txid_fund_A = wallet_rpc.sendtoaddress(address_A, 10)  # Send 10 BTC to A
print(f"Transaction ID for funding A: {txid_fund_A}")

# Mine a block to confirm the funding transaction
wallet_rpc.generatetoaddress(1, address_A)
print("Mined a block to confirm funding.")

# Get an unspent output from A
unspent_list = wallet_rpc.listunspent(1, 9999999, [address_A])
if not unspent_list:
    raise Exception("No UTXOs found for Address A. Ensure funding transaction is confirmed.")

unspent = unspent_list[0]
input_txid = unspent['txid']
vout = unspent['vout']

# Create a raw transaction sending 5 BTC from A to B
outputs = {address_B: 5}

# Lower the fee using fundrawtransaction
raw_tx = wallet_rpc.createrawtransaction([{"txid": input_txid, "vout": vout}], outputs)
funded_tx = wallet_rpc.fundrawtransaction(raw_tx, {"subtractFeeFromOutputs": [0]})  # Ensure fee is covered
decoded_tx = wallet_rpc.decoderawtransaction(funded_tx["hex"])
print(f"Decoded Transaction: {decoded_tx}")

# Sign the transaction
signed_tx = wallet_rpc.signrawtransactionwithwallet(funded_tx["hex"])
signed_hex = signed_tx['hex']

# Broadcast the transaction
try:
    txid_AB = wallet_rpc.sendrawtransaction(signed_hex)
    print(f"Broadcasted Transaction ID (A → B): {txid_AB}")
except JSONRPCException as e:
    print(f"Error broadcasting transaction: {e}")

# Mine a block to confirm A → B transaction
wallet_rpc.generatetoaddress(1, address_A)
print("Mined a block to confirm A → B transaction.")

# ---------------- Step 2: Send BTC from B to C ------------------

# Check if B received the funds
utxos_B = wallet_rpc.listunspent(1, 9999999, [address_B])
if not utxos_B:
    raise Exception("Address B did not receive funds. Check transaction status.")

unspent_B = utxos_B[0]
input_txid_B = unspent_B['txid']
vout_B = unspent_B['vout']

outputs_BC = {address_C: 3}
raw_tx_BC = wallet_rpc.createrawtransaction([{"txid": input_txid_B, "vout": vout_B}], outputs_BC)
funded_tx_BC = wallet_rpc.fundrawtransaction(raw_tx_BC, {"subtractFeeFromOutputs": [0]})
decoded_tx_BC = wallet_rpc.decoderawtransaction(funded_tx_BC["hex"])
print("Decoded B → C Transaction:", decoded_tx_BC)

signed_tx_BC = wallet_rpc.signrawtransactionwithwallet(funded_tx_BC["hex"])
signed_hex_BC = signed_tx_BC['hex']
txid_BC = wallet_rpc.sendrawtransaction(signed_hex_BC)
print(f"Broadcasted B → C Transaction ID: {txid_BC}")

# Mine a block to confirm B → C transaction
wallet_rpc.generatetoaddress(1, address_A)
print("Mined a block to confirm B → C transaction.")

# Step 3: Extract & analyze scriptSig
decoded_BC = wallet_rpc.decoderawtransaction(signed_hex_BC)
print("ScriptSig for B → C:", decoded_BC["vin"][0]["scriptSig"])
