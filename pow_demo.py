from blocksig.blockchain import Blockchain


print("\n========== PROOF OF WORK DEMONSTRATION ==========")

# Create a blockchain with difficulty 3.
blockchain = Blockchain(difficulty=3)

print("\nSTEP 1: GENESIS BLOCK")
genesis = blockchain.get_latest_block()

print("Block index:", genesis.index)
print("Genesis hash:", genesis.block_hash)
print("Genesis block is not mined.")

# Add a transaction and mine a new block.
transactions = [
    {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 100
    },
    {
        "sender": "Bob",
        "receiver": "Carol",
        "amount": 50
    }
]

print("\nSTEP 2: MINING A NEW BLOCK")
print("Difficulty: 3")
print("Required hash prefix: 000")

new_block = blockchain.add_block(transactions)

print("\nSTEP 3: MINING RESULTS")
print("Block index:", new_block.index)
print("Nonce found:", new_block.nonce)
print("Mining attempts:", new_block.mining_attempts)
print(
    "Mining time:",
    f"{new_block.mining_time_seconds:.6f} seconds"
)
print("Block hash:", new_block.block_hash)
print("Hash starts with 000:", new_block.block_hash.startswith("000"))

print("\nSTEP 4: BLOCKCHAIN VALIDATION")
print("Blockchain valid:", blockchain.is_chain_valid())

print("\nSTEP 5: TAMPERING SIMULATION")

original_hash = new_block.block_hash

new_block.transactions[0]["amount"] = 999

print("Original hash:", original_hash)
print("Recalculated hash:", new_block.calculate_hash())
print("Blockchain valid after tampering:", blockchain.is_chain_valid())

print("\n========== DEMONSTRATION COMPLETE ==========")