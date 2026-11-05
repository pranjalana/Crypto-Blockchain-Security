# BlockSig: A Hands-On Demonstration of Cryptographic Foundations and Blockchain Security

This repository contains the implementation demonstration accompanying our SE6003 survey paper, **“Cryptographic Foundations of Blockchain Security: A Comparative Survey of Bitcoin, Ethereum and XRP Ledger”** (working title; final title to be confirmed).

The project demonstrates selected cryptographic and blockchain-security mechanisms through interactive and command-line experiments. It brings together ECDSA signatures, transaction validation, a Bitcoin-style UTXO ledger, blockchain structure, Merkle Trees, Proof of Work, and a simplified multi-node consensus simulation.

> **Educational scope only:** This project is not a production blockchain, cryptocurrency, wallet, or secure transaction system. Do not use real private keys or real funds.

## 1. Project Overview

The implementation makes selected cryptographic and blockchain-security concepts observable through executable experiments.

| No. | Demonstration | What it does | Security concept |
|---|---|---|---|
| 1 | ECDSA Signature Verification and Tampering | Alice signs a transaction. The recipient, amount, or signature is modified and verification is repeated. | A signature authenticates the signed message; changing signed data causes verification to fail. |
| 2 | Conflicting Transactions / Double-Spending | Two validly signed transactions attempt to spend the same UTXO. | Signature validity alone does not prevent double-spending. Ledger rules must check whether an output has already been spent. |
| 3 | ECDSA Nonce Reuse | Two different messages are signed using the same nonce, and the private key is recovered. | Reusing an ECDSA nonce can reveal the signing private key. |
| 4 | Blockchain Structure and Hash Linking | Creates a genesis block and subsequent blocks containing transactions, a previous-block hash, a Merkle root, and a block hash. | Changing block data changes its calculated hash and can cause chain validation to fail. |
| 5 | Merkle Tree | Hashes transactions, calculates a Merkle root, generates an inclusion proof, and verifies the proof. | A transaction can be checked against a Merkle root using a proof; a modified transaction fails the original proof. |
| 6 | Proof of Work | Searches for a nonce that produces a SHA-256 block hash with a configured number of leading zeroes. | Mining requires repeated hashing; higher difficulty generally increases expected work. |
| 7 | Multi-Node Consensus Simulation | Three logical nodes create competing chains, exchange chain information, and adopt a longer valid chain. | Nodes can converge on the same valid chain under the simplified longest-valid-chain rule implemented here. |

The browser interface provides interactive controls for the demonstrations. These controls invoke the Python implementation and display the resulting outputs.

## 2. How the Demonstrations Fit Together

The demonstrations illustrate different components of a simplified blockchain workflow:

1. Transactions are represented as data. ECDSA signatures demonstrate transaction authorisation and integrity.
2. Transactions are hashed and combined into a Merkle Tree. The Merkle root is stored in a block.
3. Blocks contain transaction data, the Merkle root, a previous-block hash, a nonce, and other metadata.
4. Proof of Work searches for a nonce that makes the block hash satisfy the configured difficulty.
5. Chain validation checks the block hash, Merkle root, previous-hash link, block numbering, and Proof of Work condition.
6. The consensus simulation allows three logical nodes to exchange candidate chains and adopt a longer valid chain.

These mechanisms provide different security properties and are not interchangeable. For example, a valid digital signature does not by itself prevent double-spending, and hash linking alone does not establish agreement among distributed participants.

## 3. Technology and Cryptographic Mechanisms

- **Programming language:** Python
- **Web interface:** HTML, CSS, and JavaScript
- **Local web server:** Python standard-library `http.server`
- **Hashing:** SHA-256
- **Digital signatures:** ECDSA over secp256k1
- **Ledger model:** Simplified Bitcoin-style UTXO ledger
- **Automated testing:** pytest
- **ECDSA cross-checking:** `cryptography` / OpenSSL in the test suite

The implementation includes elliptic-curve arithmetic, ECDSA signing and verification, deterministic nonce support based on RFC 6979, low-S normalisation, and a nonce-reuse key-recovery demonstration.

## 4. Architecture and Project Structure

```text
blockchaincodes/
│
├── blocksig/
│   ├── __init__.py
│   ├── ec.py              # secp256k1 elliptic-curve arithmetic
│   ├── ecdsa.py           # ECDSA signing and verification
│   ├── attacks.py         # ECDSA nonce-reuse key recovery
│   ├── ledger.py          # Simplified UTXO ledger and transactions
│   ├── experiments.py     # Cryptographic and ledger demonstrations
│   ├── blockchain.py      # Block structure, hash linking, PoW, validation
│   ├── merkle.py          # Transaction hashes, Merkle root and proofs
│   └── consensus.py       # Logical nodes and chain synchronisation
│
├── tests/
│   ├── test_ec.py
│   ├── test_ecdsa.py
│   ├── test_attacks.py
│   ├── test_ledger.py
│   ├── test_app.py
│   ├── test_blockchain.py
│   ├── test_merkle.py
│   ├── test_pow.py
│   └── test_consensus.py
│
├── web/
│   └── index.html         # Interactive browser interface
│
├── results/
│   └── demo_results.md    # Recorded demonstration results
│
├── app.py                 # Local HTTP server and JSON API
├── demo.py                # Command-line demonstrations
├── blockchain_demo.py     # Blockchain demonstration
├── merkle_demo.py         # Merkle Tree demonstration
├── pow_demo.py            # Proof of Work demonstration
├── consensus_demo.py      # Multi-node consensus demonstration
├── requirements.txt
├── pytest.ini
├── conftest.py
├── Makefile
└── README.md
```

### Main Source Modules

| File | Responsibility |
|---|---|
| `blocksig/ec.py` | secp256k1 curve parameters and elliptic-curve point operations. |
| `blocksig/ecdsa.py` | ECDSA key generation, signing, and verification. |
| `blocksig/attacks.py` | Demonstrates private-key recovery when an ECDSA nonce is reused. |
| `blocksig/ledger.py` | Signed transactions, UTXO tracking, and double-spend checks. |
| `blocksig/experiments.py` | Logic for the cryptographic and ledger demonstrations and their interactive controls. |
| `blocksig/blockchain.py` | Block data structure, SHA-256 block hashes, mining, and chain validation. |
| `blocksig/merkle.py` | Transaction hashing, Merkle-root calculation, proof generation, and proof verification. |
| `blocksig/consensus.py` | Logical node objects and longest-valid-chain synchronisation. |
| `app.py` | Serves the GUI and connects browser requests to Python functions through JSON API routes. |
| `web/index.html` | Browser interface for the demonstrations. |

## 5. API Routes

The local application exposes these routes:

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Serves the web interface. |
| GET | `/api/run?exp=all` | Runs all automatic cryptographic and ledger demonstrations. |
| GET | `/api/run?exp=1` (or 2 or 3) | Runs one automatic demonstration. |
| POST | `/api/sign` | Signs a transaction for the interactive signature demonstration. |
| POST | `/api/verify` | Verifies a transaction signature. |
| POST | `/api/doublespend` | Runs the interactive double-spend demonstration. |
| POST | `/api/nonce` | Runs the interactive ECDSA nonce demonstration. |
| POST | `/api/blockchain` | Runs the blockchain structure demonstration. |
| POST | `/api/merkle` | Generates and verifies a Merkle inclusion proof. |
| POST | `/api/pow` | Mines a block at the requested difficulty. |
| POST | `/api/consensus` | Runs the three-node consensus simulation. |

The GUI panels call the Python API. Their displayed results are generated by the implementation rather than being fixed example text.

## 6. Requirements

- Windows, macOS, or Linux
- Python 3.10 or later recommended
- pip
- A modern web browser

Development and testing were performed on Windows 11 with Python 3.14.6 and pytest 9.2.0. Dependency compatibility should be checked when using a different Python version.

## 7. Installation and Setup

Run commands from the `blockchaincodes` directory.

### Windows PowerShell

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the `py` launcher is unavailable, use `python` instead.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 8. Run the Web Application

With the virtual environment activated:

```bash
python app.py
```

Open the address printed in the terminal:

```text
http://localhost:8000
```

The page contains interactive demonstrations of ECDSA signatures, double-spending, nonce reuse, blockchain structure, Merkle Trees, Proof of Work, and multi-node consensus. Use the controls in each panel to execute the corresponding Python logic and inspect the returned output.

Stop the local server with `Ctrl+C` in the terminal.

## 9. Run Command-Line Demonstrations

Run the cryptographic and ledger demonstrations using:

```bash
python demo.py
```

Run the blockchain demonstrations independently:

```bash
python blockchain_demo.py
python merkle_demo.py
python pow_demo.py
python consensus_demo.py
```

## 10. Run Automated Tests

Run the full test suite:

```bash
python -m pytest -v
```

Or display a concise summary:

```bash
python -m pytest -q
```

**Recorded development result: 131 tests passed.**

| Test file | Test count | Coverage |
|---|---:|---|
| `test_ec.py` | 12 | Elliptic-curve arithmetic and public-key calculations. |
| `test_ecdsa.py` | 24 | ECDSA signing, verification, invalid signatures, and OpenSSL cross-checks. |
| `test_attacks.py` | 15 | Nonce-reuse key recovery and related attack cases. |
| `test_ledger.py` | 10 | Transaction validation, UTXO spending, double-spending, and overspending. |
| `test_app.py` | 34 | Web application routes and interactive demonstration behaviour. |
| `test_blockchain.py` | 8 | Genesis block, block addition, hash links, and tampering detection. |
| `test_merkle.py` | 11 | Transaction hashing, Merkle roots, inclusion proofs, and tampering. |
| `test_pow.py` | 9 | Mining, nonce changes, difficulty validation, and Proof of Work checks. |
| `test_consensus.py` | 8 | Independent nodes, chain adoption, invalid-chain rejection, and convergence. |
| **Total** | **131** | |

The 131-test result is the recorded result from the development environment. Re-run the tests after cloning the repository to confirm the result in the current environment.

## 11. Expected Observations

- **Signature tampering:** The original signed transaction verifies; changing signed transaction data causes verification to fail.
- **Double-spending:** Two conflicting transactions can each have a valid signature, but the UTXO ledger must not accept both spends of the same output.
- **Nonce reuse:** Reusing an ECDSA nonce for different messages can expose the private key. The experiment contrasts nonce reuse with fresh deterministic nonces.
- **Block tampering:** Changing block data changes its calculated hash and causes validation to fail.
- **Merkle inclusion:** The original selected transaction verifies against the Merkle root, while a modified transaction fails the original proof.
- **Proof of Work:** The mined hash satisfies the configured leading-zero prefix. Nonce, attempts, and elapsed mining time are recorded.
- **Consensus:** The simulation ends with all three logical nodes holding the same valid chain under the implemented longest-valid-chain rule.

Mining attempts and elapsed time vary between runs. They are observations from this local demonstration, not fixed benchmark results.

## 12. Limitations

The implementation is intentionally simplified and should be interpreted within its educational scope:

1. It is not a production blockchain, cryptocurrency, wallet, or payment system.
2. The UTXO ledger is simplified. It does not implement full Bitcoin Script, multiple transaction inputs, change outputs, transaction fees, or a complete wallet.
3. The blockchain is maintained locally; the project does not implement a full peer-to-peer network.
4. Proof of Work uses a simplified SHA-256 leading-zero puzzle. It does not reproduce all Bitcoin block-header fields, difficulty retargeting, or real mining-network behaviour.
5. The consensus module implements a simplified longest-valid-chain adoption rule. It is not a complete implementation of Bitcoin Nakamoto consensus, Ethereum Proof of Stake, or XRP Ledger consensus.
6. The three nodes are logical objects running in one Python process, not independent machines communicating over a network.
7. The implementation is not constant-time and is not suitable for protecting real private keys or funds.
8. Transactions, identities, and amounts are sample data.

These limitations must be considered when comparing the demonstration with deployed blockchain systems.

## 13. Relationship to the Survey Research Questions

| Survey research question | Related implementation components | Contribution of the demonstration |
|---|---|---|
| RQ1: How do cryptographic primitives establish integrity, authenticity, and transaction authorisation in blockchain systems? | ECDSA demonstrations, transaction verification, hashing, and Merkle Tree. | Demonstrates signature verification, tampering detection, transaction hashes, and inclusion proofs. |
| RQ2: How do cryptographic mechanisms interact with consensus protocols to establish a trustworthy distributed ledger? | UTXO double-spend demonstration, block linking, Proof of Work, and consensus simulation. | Illustrates why signatures alone do not prevent double-spending and why ledger validation and agreement between nodes matter. |
| RQ3: What security limitations remain despite cryptographic mechanisms? | ECDSA nonce-reuse demonstration and tampering experiments. | Demonstrates nonce-reuse key compromise. Other limitations, such as private-key compromise, signature malleability, consensus attacks, and quantum threats, are analysed in the survey rather than fully implemented here. |

## 14. Implementation References

The following specifications are relevant to the cryptographic mechanisms described in this repository:

- Certicom Research, **SEC 1: Elliptic Curve Cryptography**, Version 2.0, May 2009. https://www.secg.org/sec1-v2.pdf
- Certicom Research, **SEC 2: Recommended Elliptic Curve Domain Parameters**, Version 2.0, January 2010. https://www.secg.org/sec2-v2.pdf
- T. Pornin, **RFC 6979: Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA)**, August 2013. https://www.rfc-editor.org/rfc/rfc6979.html

The survey paper should contain the complete bibliography for all research sources. Cite each specification in the paper only where the corresponding mechanism is discussed or implemented.

## 15. Acknowledgements and Contributions

This repository is maintained as part of the SE6003 Cryptography project.

Any source code or design adapted from an existing repository must be acknowledged here in accordance with its licence and the course's academic-integrity requirements. The project contribution statement should identify the team members and their actual contributions to implementation, integration, testing, documentation, and research.

---

**Project:** SE6003 Cryptography  
**Scope:** Educational demonstration of cryptographic mechanisms and blockchain-security concepts