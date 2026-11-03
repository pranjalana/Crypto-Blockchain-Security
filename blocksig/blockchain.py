"""
Simplified blockchain with Merkle Tree and Proof of Work.

Features:
1. Genesis block creation
2. SHA-256 block hashing
3. Previous-block hash linking
4. Merkle root integration
5. Proof of Work mining
6. Mining attempt and time tracking
7. Blockchain integrity validation
"""

import hashlib
import json
import time

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from blocksig.merkle import merkle_root


@dataclass
class Block:
    index: int
    timestamp: int
    transactions: List[Dict[str, Any]]
    previous_hash: str
    nonce: int = 0
    difficulty: int = 0

    merkle_root: str = field(init=False)
    block_hash: str = field(init=False)
    mining_attempts: int = field(default=0, init=False)
    mining_time_seconds: float = field(default=0.0, init=False)

    def __post_init__(self):
        self.merkle_root = merkle_root(self.transactions)
        self.block_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
        }

        encoded_data = json.dumps(
            block_data,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

        return hashlib.sha256(encoded_data).hexdigest()

    def mine(self) -> None:
        """
        Find a nonce that produces a hash with the required
        number of leading zeroes.
        """
        if not 1 <= self.difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5.")

        target_prefix = "0" * self.difficulty
        start_time = time.perf_counter()

        self.nonce = 0
        self.mining_attempts = 0

        while True:
            self.block_hash = self.calculate_hash()
            self.mining_attempts += 1

            if self.block_hash.startswith(target_prefix):
                break

            self.nonce += 1

        self.mining_time_seconds = time.perf_counter() - start_time


class Blockchain:

    def __init__(self, difficulty: int = 2):
        if not 1 <= difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5.")

        self.difficulty = difficulty
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(
            index=0,
            timestamp=int(time.time()),
            transactions=[],
            previous_hash="0" * 64,
            difficulty=0
        )

        self.chain.append(genesis)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(
        self,
        transactions: List[Dict[str, Any]],
        difficulty: Optional[int] = None
    ):
        """
        Mine a new block before adding it to the blockchain.
        """
        selected_difficulty = (
            self.difficulty if difficulty is None else difficulty
        )

        if not 1 <= selected_difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5.")

        previous_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            timestamp=int(time.time()),
            transactions=transactions,
            previous_hash=previous_block.block_hash,
            difficulty=selected_difficulty
        )

        new_block.mine()

        # Only append after successful mining.
        self.chain.append(new_block)

        return new_block

    def is_chain_valid(self):

        if not self.chain:
            return False

        genesis = self.chain[0]

        # Genesis block checks.
        if genesis.index != 0:
            return False

        if genesis.previous_hash != "0" * 64:
            return False

        if genesis.difficulty != 0:
            return False

        if genesis.merkle_root != merkle_root(genesis.transactions):
            return False

        if genesis.block_hash != genesis.calculate_hash():
            return False

        # Validate every mined block.
        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate difficulty.
            if not 1 <= current_block.difficulty <= 5:
                return False

            # Validate transaction integrity.
            if current_block.merkle_root != merkle_root(
                current_block.transactions
            ):
                return False

            # Validate block hash.
            recalculated_hash = current_block.calculate_hash()

            if current_block.block_hash != recalculated_hash:
                return False

            # Validate Proof of Work.
            target_prefix = "0" * current_block.difficulty

            if not current_block.block_hash.startswith(target_prefix):
                return False

            # Validate previous-block connection.
            if current_block.previous_hash != previous_block.block_hash:
                return False

            # Validate block numbering.
            if current_block.index != previous_block.index + 1:
                return False

        return True

    def display_chain(self):

        for block in self.chain:

            print("\n" + "=" * 65)
            print(f"Block index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Merkle root: {block.merkle_root}")
            print(f"Previous hash: {block.previous_hash}")
            print(f"Nonce: {block.nonce}")
            print(f"Difficulty: {block.difficulty}")
            print(f"Block hash: {block.block_hash}")

            if block.index > 0:
                print(f"Mining attempts: {block.mining_attempts}")
                print(
                    f"Mining time: "
                    f"{block.mining_time_seconds:.6f} seconds"
                )