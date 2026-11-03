
"""A simplified multi-node blockchain consensus simulation."""

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List

from blocksig.blockchain import Blockchain


@dataclass
class Node:
    """A network node with its own independent blockchain copy."""

    name: str
    difficulty: int = 2
    blockchain: Blockchain = field(init=False)

    def __post_init__(self):
        self.blockchain = Blockchain(difficulty=self.difficulty)

    @property
    def chain(self):
        """Return this node's local chain."""
        return self.blockchain.chain

    def mine_block(self, transactions: list):
        """Mine a block and append it to this node's local chain."""
        return self.blockchain.add_block(transactions)

    def receive_chain(self, candidate: Blockchain) -> bool:
        """
        Validate and adopt a candidate chain only if it is
        valid and strictly longer than this node's current chain.
        """
        candidate_copy = deepcopy(candidate)

        if not candidate_copy.is_chain_valid():
            return False

        if len(candidate_copy.chain) <= len(self.blockchain.chain):
            return False

        self.blockchain = candidate_copy
        return True

    def chain_summary(self) -> dict:
        """Return basic information about this node's chain."""
        return {
            "node": self.name,
            "blocks": len(self.chain),
            "latest_hash": self.chain[-1].block_hash,
            "valid": self.blockchain.is_chain_valid(),
        }


@dataclass
class ConsensusNetwork:
    """Coordinate chain exchange between independent nodes."""

    nodes: List[Node]

    def synchronize(self) -> dict:
        """
        Exchange chain copies between nodes.

        Each node adopts the longest valid chain it receives.
        Equal-length chains do not automatically replace one another.
        """
        snapshots = [
            (node.name, deepcopy(node.blockchain))
            for node in self.nodes
        ]

        results = {}

        for node in self.nodes:
            adopted_from = None

            candidates = sorted(
                snapshots,
                key=lambda item: len(item[1].chain),
                reverse=True,
            )

            for sender_name, candidate_chain in candidates:
                if node.receive_chain(candidate_chain):
                    adopted_from = sender_name
                    break

            results[node.name] = adopted_from

        return results

    def display_status(self):
        """Print the current state of every node."""
        print("\nNETWORK STATUS")
        print("=" * 60)

        for node in self.nodes:
            summary = node.chain_summary()

            print(
                f"{summary['node']}: "
                f"{summary['blocks']} blocks | "
                f"Valid: {summary['valid']} | "
                f"Latest hash: {summary['latest_hash'][:16]}..."
            )
