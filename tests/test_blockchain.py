
from blocksig.blockchain import Blockchain


def test_genesis_block_creation():
    chain = Blockchain()

    assert len(chain.chain) == 1
    assert chain.chain[0].index == 0
    assert chain.chain[0].previous_hash == "0" * 64


def test_add_new_block():
    chain = Blockchain()

    chain.add_block([
        {"sender": "Alice", "receiver": "Bob", "amount": 100}
    ])

    assert len(chain.chain) == 2
    assert chain.chain[1].index == 1


def test_blocks_are_linked():
    chain = Blockchain()

    chain.add_block([{"sender": "Alice", "receiver": "Bob", "amount": 100}])
    chain.add_block([{"sender": "Bob", "receiver": "Carol", "amount": 50}])

    assert chain.chain[1].previous_hash == chain.chain[0].block_hash
    assert chain.chain[2].previous_hash == chain.chain[1].block_hash


def test_valid_blockchain():
    chain = Blockchain()

    chain.add_block([{"sender": "Alice", "receiver": "Bob", "amount": 100}])
    chain.add_block([{"sender": "Bob", "receiver": "Carol", "amount": 50}])

    assert chain.is_chain_valid()


def test_detect_modified_transaction():
    chain = Blockchain()

    chain.add_block([
        {"sender": "Alice", "receiver": "Bob", "amount": 100}
    ])

    chain.chain[1].transactions[0]["amount"] = 999

    assert not chain.is_chain_valid()


def test_detect_modified_previous_hash():
    chain = Blockchain()

    chain.add_block([{"sender": "Alice", "receiver": "Bob", "amount": 100}])

    chain.chain[1].previous_hash = "123456789"

    assert not chain.is_chain_valid()


def test_detect_modified_genesis_block():
    chain = Blockchain()

    chain.chain[0].transactions.append(
        {"sender": "Eve", "receiver": "Mallory", "amount": 999}
    )

    assert not chain.is_chain_valid()


def test_detect_wrong_block_index():
    chain = Blockchain()

    chain.add_block([{"sender": "Alice", "receiver": "Bob", "amount": 100}])

    chain.chain[1].index = 5

    assert not chain.is_chain_valid()
