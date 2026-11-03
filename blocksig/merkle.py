
"""
Merkle Tree implementation using SHA-256.

Features:
1. Transaction hashing
2. Merkle root generation
3. Handling odd numbers of transactions
4. Merkle inclusion proof generation
5. Merkle proof verification
"""

import hashlib
import json


def hash_data(data: bytes) -> str:
    """Return SHA-256 hash as hexadecimal."""
    return hashlib.sha256(data).hexdigest()


def transaction_hash(transaction: dict) -> str:
    """Generate a deterministic hash for a transaction."""

    encoded = json.dumps(
        transaction,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    return hash_data(encoded)


def merkle_root(transactions: list) -> str:
    """Calculate the Merkle root of a transaction list."""

    if not transactions:
        return hash_data(b"")

    current_level = [
        transaction_hash(tx) for tx in transactions
    ]

    while len(current_level) > 1:

        # Duplicate the final hash when the number is odd.
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        next_level = []

        for i in range(0, len(current_level), 2):

            left = bytes.fromhex(current_level[i])
            right = bytes.fromhex(current_level[i + 1])

            combined = left + right

            next_level.append(hash_data(combined))

        current_level = next_level

    return current_level[0]


def generate_merkle_proof(transactions: list, index: int) -> list:
    """
    Generate an inclusion proof for a transaction.

    Each proof entry contains:
    (sibling_hash, sibling_is_left)
    """

    if not 0 <= index < len(transactions):
        raise IndexError("Transaction index out of range")

    current_level = [
        transaction_hash(tx) for tx in transactions
    ]

    proof = []
    position = index

    while len(current_level) > 1:

        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        if position % 2 == 0:
            sibling_position = position + 1
            sibling_is_left = False
        else:
            sibling_position = position - 1
            sibling_is_left = True

        proof.append(
            (current_level[sibling_position], sibling_is_left)
        )

        next_level = []

        for i in range(0, len(current_level), 2):
            left = bytes.fromhex(current_level[i])
            right = bytes.fromhex(current_level[i + 1])

            next_level.append(hash_data(left + right))

        current_level = next_level
        position //= 2

    return proof


def verify_merkle_proof(transaction: dict, proof: list,
                        expected_root: str) -> bool:
    """Verify that a transaction belongs to a Merkle tree."""

    current_hash = transaction_hash(transaction)

    for sibling_hash, sibling_is_left in proof:

        current_bytes = bytes.fromhex(current_hash)
        sibling_bytes = bytes.fromhex(sibling_hash)

        if sibling_is_left:
            combined = sibling_bytes + current_bytes
        else:
            combined = current_bytes + sibling_bytes

        current_hash = hash_data(combined)

    return current_hash == expected_root
