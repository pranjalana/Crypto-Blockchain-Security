
"""
Local web application for blockchain and cryptography experiments.

Usage:
    python app.py

Then open:
    http://localhost:8000

Original experiments:
    /api/sign
    /api/verify
    /api/doublespend
    /api/nonce

New blockchain features:
    /api/blockchain
    /api/merkle
    /api/pow
    /api/consensus
"""

import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from blocksig import experiments
from blocksig.blockchain import Blockchain
from blocksig.merkle import (
    merkle_root,
    generate_merkle_proof,
    verify_merkle_proof,
)
from blocksig.consensus import Node, ConsensusNetwork


HOST, PORT = "127.0.0.1", 8000
PAGE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "web",
    "index.html",
)

LAB = experiments.TamperLab()


# --------------------------------------------------
# BLOCKCHAIN DATA SERIALIZATION
# --------------------------------------------------

def serialize_block(block):
    """Convert a Block object into JSON-compatible data."""
    return {
        "index": block.index,
        "timestamp": block.timestamp,
        "transactions": block.transactions,
        "previous_hash": block.previous_hash,
        "merkle_root": block.merkle_root,
        "nonce": block.nonce,
        "difficulty": block.difficulty,
        "hash": block.block_hash,
        "mining_attempts": block.mining_attempts,
        "mining_time_seconds": block.mining_time_seconds,
    }


def serialize_chain(blockchain):
    """Convert a blockchain into JSON-compatible data."""
    return {
        "valid": blockchain.is_chain_valid(),
        "blocks": [
            serialize_block(block)
            for block in blockchain.chain
        ],
    }


# --------------------------------------------------
# FEATURE 1: BLOCKCHAIN
# --------------------------------------------------

def run_blockchain_demo(body):
    difficulty = int(body.get("difficulty", 2))

    blockchain = Blockchain(difficulty=difficulty)

    transactions = [
        {
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 100,
        },
        {
            "sender": "Bob",
            "recipient": "Carol",
            "amount": 50,
        },
    ]

    blockchain.add_block(transactions)

    return serialize_chain(blockchain)


# --------------------------------------------------
# FEATURE 2: MERKLE TREE
# --------------------------------------------------

def run_merkle_demo(body):
    transactions = body.get(
        "transactions",
        [
            {
                "sender": "Alice",
                "recipient": "Bob",
                "amount": 100,
            },
            {
                "sender": "Bob",
                "recipient": "Carol",
                "amount": 50,
            },
            {
                "sender": "Carol",
                "recipient": "David",
                "amount": 25,
            },
            {
                "sender": "David",
                "recipient": "Eve",
                "amount": 10,
            },
        ],
    )

    if not isinstance(transactions, list) or not transactions:
        raise ValueError("Provide at least one transaction.")

    if not all(isinstance(tx, dict) for tx in transactions):
        raise ValueError("Every transaction must be a JSON object.")

    index = int(body.get("index", 1))

    if index < 0 or index >= len(transactions):
        raise ValueError("Transaction index is out of range.")

    root = merkle_root(transactions)
    selected = transactions[index]

    proof = generate_merkle_proof(
        transactions,
        index,
    )

    proof_data = [
        {
            "sibling_hash": sibling,
            "sibling_is_left": is_left,
        }
        for sibling, is_left in proof
    ]

    verified = verify_merkle_proof(
        selected,
        proof,
        root,
    )

    modified = dict(selected)
    modified["amount"] = modified.get("amount", 0) + 1

    tampered_verified = verify_merkle_proof(
        modified,
        proof,
        root,
    )

    return {
        "transactions": transactions,
        "root": root,
        "selected_transaction": selected,
        "proof": proof_data,
        "verified": verified,
        "tampered_verified": tampered_verified,
    }


# --------------------------------------------------
# FEATURE 3: PROOF OF WORK
# --------------------------------------------------

def run_pow_demo(body):
    difficulty = int(body.get("difficulty", 2))

    blockchain = Blockchain(difficulty=difficulty)

    block = blockchain.add_block(
        [
            {
                "sender": "Alice",
                "recipient": "Bob",
                "amount": 100,
            }
        ]
    )

    return {
        "difficulty": block.difficulty,
        "required_prefix": "0" * block.difficulty,
        "nonce": block.nonce,
        "attempts": block.mining_attempts,
        "mining_time_seconds": block.mining_time_seconds,
        "hash": block.block_hash,
        "hash_meets_difficulty": block.block_hash.startswith(
            "0" * block.difficulty
        ),
        "chain_valid": blockchain.is_chain_valid(),
        "chain": serialize_chain(blockchain),
    }


# --------------------------------------------------
# FEATURE 4: MULTI-NODE CONSENSUS
# --------------------------------------------------

def run_consensus_demo(body):
    difficulty = int(body.get("difficulty", 2))

    node_a = Node("Node A", difficulty)
    node_b = Node("Node B", difficulty)
    node_c = Node("Node C", difficulty)

    network = ConsensusNetwork(
        [node_a, node_b, node_c]
    )

    def snapshot(step):
        return {
            "step": step,
            "nodes": [
                {
                    **node.chain_summary(),
                    "chain": [
                        block.block_hash
                        for block in node.chain
                    ],
                }
                for node in network.nodes
            ],
        }

    steps = [
        snapshot("Genesis: all nodes start together")
    ]

    # Node A and Node B mine competing blocks.
    node_a.mine_block(
        [
            {
                "sender": "Alice",
                "recipient": "Bob",
                "amount": 100,
            }
        ]
    )

    node_b.mine_block(
        [
            {
                "sender": "Alice",
                "recipient": "Carol",
                "amount": 80,
            }
        ]
    )

    steps.append(
        snapshot("Competing blocks mined")
    )

    # First synchronization.
    network.synchronize()

    steps.append(
        snapshot("First synchronization")
    )

    # Node A extends its chain.
    node_a.mine_block(
        [
            {
                "sender": "Bob",
                "recipient": "Dave",
                "amount": 30,
            }
        ]
    )

    steps.append(
        snapshot("Node A extends its chain")
    )

    # Final synchronization.
    network.synchronize()

    steps.append(
        snapshot("Final synchronization")
    )

    hashes = [
        [
            block.block_hash
            for block in node.chain
        ]
        for node in network.nodes
    ]

    all_valid = all(
        node.blockchain.is_chain_valid()
        for node in network.nodes
    )

    all_agree = all(
        chain == hashes[0]
        for chain in hashes
    )

    return {
        "steps": steps,
        "all_valid": all_valid,
        "all_agree": all_agree,
    }


# --------------------------------------------------
# HTTP REQUEST HANDLER
# --------------------------------------------------

class Handler(BaseHTTPRequestHandler):

    def _send(self, status, body, ctype):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == "/":
            with open(PAGE, "rb") as file:
                self._send(
                    200,
                    file.read(),
                    "text/html; charset=utf-8",
                )

        elif url.path == "/api/run":
            exp = parse_qs(url.query).get(
                "exp",
                ["all"],
            )[0]

            if exp == "all":
                data = experiments.run_all()

            elif exp.isdigit() and int(exp) in experiments.ALL:
                data = [
                    experiments.ALL[int(exp)]()
                ]

            else:
                self._send(
                    400,
                    b'{"error": "unknown experiment"}',
                    "application/json",
                )
                return

            self._send(
                200,
                json.dumps(data).encode(),
                "application/json",
            )

        else:
            self._send(
                404,
                b"Not found",
                "text/plain",
            )

    def do_POST(self):
        """Handle interactive experiment and blockchain requests."""

        path = urlparse(self.path).path

        allowed_paths = (
            "/api/sign",
            "/api/verify",
            "/api/doublespend",
            "/api/nonce",
            "/api/blockchain",
            "/api/merkle",
            "/api/pow",
            "/api/consensus",
        )

        if path not in allowed_paths:
            self._send(
                404,
                b"Not found",
                "text/plain",
            )
            return

        try:
            length = int(
                self.headers.get("Content-Length", 0)
            )

            if length > 10_000:
                raise ValueError("Request too large.")

            body = json.loads(
                self.rfile.read(length) or b"{}"
            )

            if not isinstance(body, dict):
                raise ValueError(
                    "Expected a JSON object."
                )

            # ORIGINAL EXPERIMENT 1: SIGNING
            if path == "/api/sign":
                data = LAB.sign(
                    body.get("recipient"),
                    body.get("amount"),
                )

            # ORIGINAL EXPERIMENT 1: VERIFICATION
            elif path == "/api/verify":
                data = LAB.verify(
                    body.get("recipient"),
                    body.get("amount"),
                    body.get("r"),
                    body.get("s"),
                )

            # ORIGINAL EXPERIMENT 2: DOUBLE SPENDING
            elif path == "/api/doublespend":
                data = experiments.interactive_double_spend(
                    body.get("coin"),
                    body.get("a_to"),
                    body.get("a_amount"),
                    body.get("b_to"),
                    body.get("b_amount"),
                    body.get("order", "AB"),
                )

            # ORIGINAL EXPERIMENT 3: NONCE REUSE
            elif path == "/api/nonce":
                data = experiments.interactive_nonce(
                    body.get("message1"),
                    body.get("message2"),
                    body.get("mode", "reuse"),
                )

            # NEW FEATURE 1: BLOCKCHAIN
            elif path == "/api/blockchain":
                data = run_blockchain_demo(body)

            # NEW FEATURE 2: MERKLE TREE
            elif path == "/api/merkle":
                data = run_merkle_demo(body)

            # NEW FEATURE 3: PROOF OF WORK
            elif path == "/api/pow":
                data = run_pow_demo(body)

            # NEW FEATURE 4: CONSENSUS
            elif path == "/api/consensus":
                data = run_consensus_demo(body)

            else:
                raise ValueError("Unknown API endpoint.")

        except (
            ValueError,
            json.JSONDecodeError,
            TypeError,
        ) as err:
            self._send(
                400,
                json.dumps(
                    {"error": str(err)}
                ).encode(),
                "application/json",
            )
            return

        self._send(
            200,
            json.dumps(data).encode(),
            "application/json",
        )

    def log_message(self, fmt, *args):
        # Keep the terminal quiet.
        pass


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

def main():
    server = ThreadingHTTPServer(
        (HOST, PORT),
        Handler,
    )

    url = f"http://localhost:{PORT}"

    print(f"Blockchain application running at {url}")
    print("Press Ctrl+C to stop.")

    threading.Timer(
        0.5,
        lambda: webbrowser.open(url),
    ).start()

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()
