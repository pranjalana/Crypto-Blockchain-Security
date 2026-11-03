import pytest

from blocksig.blockchain import Blockchain, Block


def sample_transactions():
    return [
        {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 100
        }
    ]


def test_block_can_be_mined():
    block = Block(
        index=1,
        timestamp=1000,
        transactions=sample_transactions(),
        previous_hash="0" * 64,
        difficulty=2
    )

    block.mine()

    assert block.block_hash.startswith("00")
    assert block.mining_attempts > 0


def test_mining_changes_nonce():
    block = Block(
        index=1,
        timestamp=1000,
        transactions=sample_transactions(),
        previous_hash="0" * 64,
        difficulty=2
    )

    block.mine()

    assert block.nonce >= 0
    assert block.block_hash == block.calculate_hash()


def test_mined_block_is_added_to_chain():
    blockchain = Blockchain(difficulty=2)

    block = blockchain.add_block(sample_transactions())

    assert len(blockchain.chain) == 2
    assert block.block_hash.startswith("00")


def test_mined_block_has_correct_previous_hash():
    blockchain = Blockchain(difficulty=2)

    block = blockchain.add_block(sample_transactions())

    assert block.previous_hash == blockchain.chain[0].block_hash


def test_mined_block_records_performance():
    blockchain = Blockchain(difficulty=2)

    block = blockchain.add_block(sample_transactions())

    assert block.mining_attempts > 0
    assert block.mining_time_seconds >= 0


def test_valid_pow_blockchain():
    blockchain = Blockchain(difficulty=2)

    blockchain.add_block(sample_transactions())

    assert blockchain.is_chain_valid() is True


def test_invalid_pow_is_rejected():
    blockchain = Blockchain(difficulty=2)

    block = blockchain.add_block(sample_transactions())

    # Replace the stored hash with a hash that does not meet difficulty.
    block.block_hash = "f" * 64

    assert blockchain.is_chain_valid() is False


def test_invalid_difficulty_is_rejected():
    with pytest.raises(ValueError):
        Blockchain(difficulty=0)

    with pytest.raises(ValueError):
        Blockchain(difficulty=6)


def test_block_rejects_invalid_mining_difficulty():
    block = Block(
        index=1,
        timestamp=1000,
        transactions=sample_transactions(),
        previous_hash="0" * 64,
        difficulty=0
    )

    with pytest.raises(ValueError):
        block.mine()