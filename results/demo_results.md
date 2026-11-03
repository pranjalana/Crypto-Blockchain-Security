| Experiment | Check | Result |
|---|---|---|
| 1 | Original transaction (signature matches): VALID | PASS |
| 1 | Tampered transaction (recipient changed): REJECTED | PASS |
| 1 | Tampered transaction (amount changed): REJECTED | PASS |
| 2 | Tx A signature (signed by Alice): VALID | PASS |
| 2 | Tx B signature (signed by Alice): VALID | PASS |
| 2 | Tx A (Bob gets 100, the coin is now spent): ACCEPTED | PASS |
| 2 | Tx B (coin already spent): REJECTED | PASS |
| 3 | Attacker recovers the exact private key | PASS |
| 3 | With RFC 6979 the r values differ, so the attack cannot start | PASS |
