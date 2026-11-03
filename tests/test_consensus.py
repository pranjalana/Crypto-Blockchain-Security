
import copy

from blocksig.consensus import Node, ConsensusNetwork


def test_nodes_start_with_independent_genesis_chains():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)

    assert len(node_a.chain) == 1
    assert len(node_b.chain) == 1
    assert node_a.chain[0].block_hash == node_b.chain[0].block_hash
    assert node_a.chain[0] is not node_b.chain[0]


def test_node_can_mine_its_own_block():
    node = Node("Node A", difficulty=1)

    block = node.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])

    assert len(node.chain) == 2
    assert node.chain[-1].block_hash == block.block_hash
    assert node.blockchain.is_chain_valid()


def test_nodes_can_create_competing_chains():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])

    node_b.mine_block([
        {"sender": "Alice", "recipient": "Carol", "amount": 20}
    ])

    assert len(node_a.chain) == len(node_b.chain)
    assert node_a.chain[-1].block_hash != node_b.chain[-1].block_hash


def test_node_adopts_a_longer_valid_chain():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])
    node_a.mine_block([
        {"sender": "Bob", "recipient": "Carol", "amount": 5}
    ])

    adopted = node_b.receive_chain(node_a.blockchain)

    assert adopted is True
    assert len(node_b.chain) == 3
    assert node_b.blockchain.is_chain_valid()


def test_node_rejects_invalid_chain():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])
    node_a.mine_block([
        {"sender": "Bob", "recipient": "Carol", "amount": 5}
    ])

    invalid_chain = copy.deepcopy(node_a.blockchain)
    invalid_chain.chain[1].transactions[0]["amount"] = 999

    adopted = node_b.receive_chain(invalid_chain)

    assert adopted is False
    assert len(node_b.chain) == 1


def test_node_does_not_replace_chain_with_equal_length_chain():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])
    node_b.mine_block([
        {"sender": "Alice", "recipient": "Carol", "amount": 20}
    ])

    original_hash = node_b.chain[-1].block_hash
    adopted = node_b.receive_chain(node_a.blockchain)

    assert adopted is False
    assert node_b.chain[-1].block_hash == original_hash


def test_network_converges_on_unique_longest_valid_chain():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)
    node_c = Node("Node C", difficulty=1)

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])
    node_b.mine_block([
        {"sender": "Alice", "recipient": "Carol", "amount": 20}
    ])

    # Node A extends its competing chain.
    node_a.mine_block([
        {"sender": "Bob", "recipient": "Dave", "amount": 5}
    ])

    network = ConsensusNetwork([node_a, node_b, node_c])
    network.synchronize()

    expected_hashes = [block.block_hash for block in node_a.chain]

    for node in network.nodes:
        assert [block.block_hash for block in node.chain] == expected_hashes
        assert node.blockchain.is_chain_valid()


def test_nodes_do_not_share_adopted_block_objects():
    node_a = Node("Node A", difficulty=1)
    node_b = Node("Node B", difficulty=1)

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 10}
    ])
    node_a.mine_block([
        {"sender": "Bob", "recipient": "Carol", "amount": 5}
    ])

    node_b.receive_chain(node_a.blockchain)

    assert node_a.chain[1] is not node_b.chain[1]
