import json

balances = []

with open("balances.json") as w:
    balances = json.load(w)


def total_count() -> int:
    return len(balances)


def with_difference_count() -> int:
    """Count of all users with a difference between onchain and offchain balance"""
    return sum(1 for b in balances if b["mpxr"] != b["onchain_balance"])


def positive_withdraw_count() -> int:
    """Count of all users with a positive difference between onchain and offchain balance"""
    return sum(1 for b in balances if b["mpxr"] > b["onchain_balance"])


def negative_withdraw_count() -> int:
    """Count of all users with a negative difference between onchain and offchain balance"""
    return sum(1 for b in balances if b["mpxr"] < b["onchain_balance"])


def negative_with_zero_onchain() -> int:
    """Count of all users with a negative difference between onchain and offchain balance
    and their onchain balance is 0"""
    return sum(
        1
        for b in balances
        if b["mpxr"] < b["onchain_balance"] and b["onchain_balance"] == 0
    )


def positive_with_zero_onchain() -> int:
    """Count of all users with a positive difference between onchain and offchain balance
    and their onchain balance is 0"""
    return sum(
        1
        for b in balances
        if b["mpxr"] > b["onchain_balance"] and b["onchain_balance"] == 0
    )


if __name__ == "__main__":
    print(f"Total Count: {total_count()}")
    print(f"With Difference Count: {with_difference_count()}")
    print(f"Positive Withdraw Count: {positive_withdraw_count()}")
    print(f"Negative Withdraw Count: {negative_withdraw_count()}")
    print(
        f"Negative With Zero Onchain: {negative_with_zero_onchain()}"
    )
    print(
        f"Positive With Zero Onchain: {positive_with_zero_onchain()}"
    )
