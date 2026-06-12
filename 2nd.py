from web3 import Web3
from collections import Counter
import json

RPC = "http://127.0.0.1:8545"

w3 = Web3(Web3.HTTPProvider(RPC))

with open("Lottery.json") as f:
    artifact = json.load(f)

abi = artifact["abi"]

contract = w3.eth.contract(
    address="",
    abi=abi
)

owner = w3.eth.accounts[0]

wins = Counter()

ROUNDS = 1000
PLAYERS = 10

ticket_price = contract.functions.ticketPrice().call()

for _ in range(ROUNDS):

    for i in range(1, PLAYERS + 1):

        tx = contract.functions.enter().transact({
            "from": w3.eth.accounts[i],
            "value": ticket_price
        })

        w3.eth.wait_for_transaction_receipt(tx)

    tx = contract.functions.pickWinner().transact({
        "from": owner
    })

    w3.eth.wait_for_transaction_receipt(tx)

    winner = contract.functions.lastWinner().call()

    wins[winner] += 1

print()

for addr, count in wins.items():
    print(addr, count)

print()
print("Percentages")

for addr, count in wins.items():
    print(addr, round(count * 100 / ROUNDS, 2), "%")
