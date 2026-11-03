
import pytest

from blocksig.merkle import (
    hash_data,
    transaction_hash,
    merkle_root,
    generate_merkle_proof,
    verify_merkle_proof
)

from blocksig.blockchain import Blockchain


@pytest.fixture
def transactions():
    return [
        {"sender": "Alice", "receiver": "Bob", "amount": 100},
        {"sender": "Bob", "receiver": "Carol", "amount": 50},
        {"sender": "Carol", "receiver": "David", "amount": 25},
        {"sender": "David", "receiver": "Eve", "amount": 10}
    ]


def test_transaction_hash_is_64_characters(transactions):
    result = transaction_hash(transactions[0])

    assert len(result) == 64


def test_merkle_root_is_generated(transactions):
    root = merkle_root(transactions)

    assert len(root) == 64


def test_merkle_root_is_deterministic(transactions):
    assert merkle_root(transactions) == merkle_root(transactions)


def test_merkle_root_changes_when_transaction_changes(transactions):
    original_root = merkle_root(transactions)

    transactions[0]["amount"] = 999

    changed_root = merkle_root(transactions)

    assert original_root != changed_root


def test_empty_merkle_tree():
    assert merkle_root([]) == hash_data(b"")


def test_odd_number_of_transactions():
    transactions = [
        {"sender": "A", "receiver": "B", "amount": 10},
        {"sender": "B", "receiver": "C", "amount": 20},
        {"sender": "C", "receiver": "D", "amount": 30}
    ]

    assert len(merkle_root(transactions)) == 64


def test_merkle_proof_verifies_transaction(transactions):
    root = merkle_root(transactions)

    proof = generate_merkle_proof(transactions, 1)

    assert verify_merkle_proof(
        transactions[1],
        proof,
        root
    )


def test_merkle_proof_rejects_modified_transaction(transactions):
    root = merkle_root(transactions)

    proof = generate_merkle_proof(transactions, 1)

    modified = transactions[1].copy()
    modified["amount"] = 999

    assert not verify_merkle_proof(
        modified,
        proof,
        root
    )


def test_block_contains_merkle_root(transactions):
    chain = Blockchain()

    block = chain.add_block(transactions)

    assert block.merkle_root == merkle_root(transactions)


def test_block_detects_transaction_tampering(transactions):
    chain = Blockchain()

    block = chain.add_block(transactions)

    assert chain.is_chain_valid()

    block.transactions[0]["amount"] = 999

    assert not chain.is_chain_valid()


def test_invalid_merkle_proof_index(transactions):
    with pytest.raises(IndexError):
        generate_merkle_proof(transactions, 99)
