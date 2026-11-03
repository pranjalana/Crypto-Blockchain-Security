
from blocksig.blockchain import Blockchain


# Create a new blockchain
my_chain = Blockchain()

print("\n1. GENESIS BLOCK CREATED")
my_chain.display_chain()


# Add first block
my_chain.add_block([
    {
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 100
    }
])

print("\n2. BLOCK 1 ADDED")
my_chain.display_chain()


# Add second block
my_chain.add_block([
    {
        "sender": "Bob",
        "receiver": "Carol",
        "amount": 50
    }
])

print("\n3. BLOCK 2 ADDED")
my_chain.display_chain()


# Validate the blockchain
print("\n4. BLOCKCHAIN VALIDATION")

if my_chain.is_chain_valid():
    print("PASS: Blockchain is valid.")
else:
    print("FAIL: Blockchain integrity compromised.")
