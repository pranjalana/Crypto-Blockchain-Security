
"""Demonstrate simplified consensus between three blockchain nodes."""

from blocksig.consensus import Node, ConsensusNetwork


def main():
    print("=" * 65)
    print("FEATURE 4: MULTIPLE-NODE CONSENSUS SIMULATION")
    print("=" * 65)

    # 1. Create three independent nodes.
    node_a = Node("Node A", difficulty=2)
    node_b = Node("Node B", difficulty=2)
    node_c = Node("Node C", difficulty=2)

    network = ConsensusNetwork([node_a, node_b, node_c])

    print("\nSTEP 1: All nodes start with the genesis block.")
    network.display_status()

    # 2. A and B independently mine competing blocks.
    print("\nSTEP 2: Node A and Node B mine different blocks.")

    node_a.mine_block([
        {"sender": "Alice", "recipient": "Bob", "amount": 100}
    ])

    node_b.mine_block([
        {"sender": "Alice", "recipient": "Carol", "amount": 80}
    ])

    print("\nNode A's latest transaction: Alice -> Bob (100)")
    print("Node B's latest transaction: Alice -> Carol (80)")
    print("Their blocks are competing alternatives.")
    network.display_status()

    # 3. Exchange chains. They are equal in length, so neither
    #    competing chain automatically replaces the other.
    print("\nSTEP 3: Nodes exchange their competing chains.")
    results = network.synchronize()
    print("Adoption results:", results)
    network.display_status()

    # 4. Node A extends its own chain.
    print("\nSTEP 4: Node A mines another block.")

    node_a.mine_block([
        {"sender": "Bob", "recipient": "Dave", "amount": 30}
    ])

    network.display_status()

    # 5. Exchange chains again. A's valid chain is now longer.
    print("\nSTEP 5: Nodes synchronize again.")
    results = network.synchronize()
    print("Adoption results:", results)
    network.display_status()

    # 6. Check whether all nodes now share the same chain.
    print("\nSTEP 6: Final consensus check.")

    all_valid = all(
        node.blockchain.is_chain_valid()
        for node in network.nodes
    )

    reference_chain = node_a.chain
    all_agree = all(
        [block.block_hash for block in node.chain]
        == [block.block_hash for block in reference_chain]
        for node in network.nodes
    )

    print("All node chains valid:", all_valid)
    print("All nodes agree on the chain:", all_agree)

    if all_valid and all_agree:
        print("\nSUCCESS: All nodes converged on the same valid chain.")
    else:
        print("\nRESULT: Nodes have not yet converged.")


if __name__ == "__main__":
    main()
