from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# 🚀 Step 1: Connect to bitcoind using RPC
rpc_user = "Allies"
rpc_password = "Allies4321@"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443", timeout=120)

# 🚀 Step 2: Create or load the wallet
wallet_name = "testwallet"
try:
    rpc_connection.loadwallet(wallet_name)
except JSONRPCException as e:
    if "Wallet file not found" in str(e):
        rpc_connection.createwallet(wallet_name)

# Select the wallet
wallet_rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}", timeout=120)

# 🚀 Step 3: Generate P2SH-SegWit Addresses
address_Ap = wallet_rpc.getnewaddress("", "p2sh-segwit")
address_Bp = wallet_rpc.getnewaddress("", "p2sh-segwit")
address_Cp = wallet_rpc.getnewaddress("", "p2sh-segwit")

print(f"Address A': {address_Ap}")
print(f"Address B': {address_Bp}")
print(f"Address C': {address_Cp}")

# 🚀 Step 4: Fund Address A' (Mine some regtest BTC first)
wallet_rpc.generatetoaddress(101, address_Ap)  # Mine 101 blocks to fund the wallet
txid_fund_Ap = wallet_rpc.sendtoaddress(address_Ap, 10)  # Send 10 BTC to A'
print(f"Transaction ID for funding A': {txid_fund_Ap}")

# Mine a block to confirm the funding transaction
wallet_rpc.generatetoaddress(1, address_Ap)
print("Mined a block to confirm funding.")

# 🚀 Step 5: Create Transaction A' → B'
# Get an unspent output from A'
utxos_Ap = wallet_rpc.listunspent(1, 9999999, [address_Ap])
if not utxos_Ap:
    raise Exception("No UTXOs found for Address A'. Ensure funding transaction is confirmed.")

unspent_Ap = utxos_Ap[0]
input_txid_Ap = unspent_Ap['txid']
vout_Ap = unspent_Ap['vout']

# Create raw transaction sending 5 BTC from A' to B'
outputs_Ap_Bp = {address_Bp: 5}
raw_tx_Ap_Bp = wallet_rpc.createrawtransaction([{"txid": input_txid_Ap, "vout": vout_Ap}], outputs_Ap_Bp)

# Fund the transaction (adjust fee)
funded_tx_Ap_Bp = wallet_rpc.fundrawtransaction(raw_tx_Ap_Bp, {"subtractFeeFromOutputs": [0]})
decoded_tx_Ap_Bp = wallet_rpc.decoderawtransaction(funded_tx_Ap_Bp["hex"])
print("Decoded A' → B' Transaction:", decoded_tx_Ap_Bp)

# Sign the transaction
signed_tx_Ap_Bp = wallet_rpc.signrawtransactionwithwallet(funded_tx_Ap_Bp["hex"])
signed_hex_Ap_Bp = signed_tx_Ap_Bp['hex']

# Broadcast the transaction
txid_Ap_Bp = wallet_rpc.sendrawtransaction(signed_hex_Ap_Bp)
print(f"Broadcasted A' → B' Transaction ID: {txid_Ap_Bp}")

# Mine a block to confirm A' → B' transaction
wallet_rpc.generatetoaddress(1, address_Ap)
print("Mined a block to confirm A' → B' transaction.")

# 🚀 Step 6: Create Transaction B' → C'
# Get an unspent output from B'
utxos_Bp = wallet_rpc.listunspent(1, 9999999, [address_Bp])
if not utxos_Bp:
    raise Exception("Address B' did not receive funds. Check transaction status.")

unspent_Bp = utxos_Bp[0]
input_txid_Bp = unspent_Bp['txid']
vout_Bp = unspent_Bp['vout']

# Create raw transaction sending 3 BTC from B' to C'
outputs_Bp_Cp = {address_Cp: 3}
raw_tx_Bp_Cp = wallet_rpc.createrawtransaction([{"txid": input_txid_Bp, "vout": vout_Bp}], outputs_Bp_Cp)

# Fund the transaction (adjust fee)
funded_tx_Bp_Cp = wallet_rpc.fundrawtransaction(raw_tx_Bp_Cp, {"subtractFeeFromOutputs": [0]})
decoded_tx_Bp_Cp = wallet_rpc.decoderawtransaction(funded_tx_Bp_Cp["hex"])
print("Decoded B' → C' Transaction:", decoded_tx_Bp_Cp)

# Sign the transaction
signed_tx_Bp_Cp = wallet_rpc.signrawtransactionwithwallet(funded_tx_Bp_Cp["hex"])
signed_hex_Bp_Cp = signed_tx_Bp_Cp['hex']

# Broadcast the transaction
txid_Bp_Cp = wallet_rpc.sendrawtransaction(signed_hex_Bp_Cp)
print(f"Broadcasted B' → C' Transaction ID: {txid_Bp_Cp}")

# Mine a block to confirm B' → C' transaction
wallet_rpc.generatetoaddress(1, address_Ap)
print("Mined a block to confirm B' → C' transaction.")

# 🚀 Step 7: Extract & analyze scriptSig
decoded_Bp_Cp = wallet_rpc.decoderawtransaction(signed_hex_Bp_Cp)
print("ScriptSig for B' → C':", decoded_Bp_Cp["vin"][0]["scriptSig"])
