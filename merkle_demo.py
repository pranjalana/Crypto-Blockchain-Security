
from blocksig.merkle import (
    merkle_root,
    transaction_hash,
    generate_merkle_proof,
    verify_merkle_proof
)

from blocksig.blockchain import Blockchain


# Four sample transactions
transactions = [
    {"sender": "Alice", "receiver": "Bob", "amount": 100},
    {"sender": "Bob", "receiver": "Carol", "amount": 50},
    {"sender": "Carol", "receiver": "David", "amount": 25},
    {"sender": "David", "receiver": "Eve", "amount": 10}
]


print("\n========== MERKLE TREE DEMONSTRATION ==========")

# STEP 1: Hash individual transactions
print("\nSTEP 1: TRANSACTION HASHING")

for i, tx in enumerate(transactions):
    print(f"T{i + 1}: {tx}")
    print(f"Hash: {transaction_hash(tx)}\n")


# STEP 2: Generate Merkle Root
print("\nSTEP 2: MERKLE ROOT GENERATION")

root = merkle_root(transactions)

print(f"Merkle Root: {root}")


# STEP 3: Generate inclusion proof for T2
print("\nSTEP 3: MERKLE INCLUSION PROOF")

target_index = 1

proof = generate_merkle_proof(
    transactions,
    target_index
)

print(f"Transaction: {transactions[target_index]}")
print(f"Proof levels: {len(proof)}")

for level, (sibling, is_left) in enumerate(proof, start=1):
    position = "LEFT" if is_left else "RIGHT"
    print(f"Level {level}: sibling is on {position}: {sibling}")


# STEP 4: Verify inclusion proof
print("\nSTEP 4: VERIFY TRANSACTION INCLUSION")

valid = verify_merkle_proof(
    transactions[target_index],
    proof,
    root
)

print(f"Transaction belongs to tree: {valid}")


# STEP 5: Simulate transaction tampering
print("\nSTEP 5: SIMULATE TRANSACTION TAMPERING")

modified_transaction = transactions[target_index].copy()
modified_transaction["amount"] = 500

print(f"Original: {transactions[target_index]}")
print(f"Modified: {modified_transaction}")

tampered_result = verify_merkle_proof(
    modified_transaction,
    proof,
    root
)

print(f"Modified transaction accepted by proof: {tampered_result}")

new_root = merkle_root([
    transactions[0],
    modified_transaction,
    transactions[2],
    transactions[3]
])

print(f"Original Merkle Root: {root}")
print(f"Modified Merkle Root: {new_root}")
print(f"Roots match: {root == new_root}")


# STEP 6: Integrate Merkle Root into a block
print("\nSTEP 6: BLOCKCHAIN INTEGRATION")

chain = Blockchain()

block = chain.add_block(transactions)

print(f"Block index: {block.index}")
print(f"Block Merkle Root: {block.merkle_root}")
print(f"Blockchain valid: {chain.is_chain_valid()}")


# STEP 7: Modify a transaction inside the block
print("\nSTEP 7: BLOCK-LEVEL TAMPERING")

block.transactions[1]["amount"] = 500

print(f"Blockchain valid after tampering: {chain.is_chain_valid()}")

print("\n========== DEMONSTRATION COMPLETE ==========")
