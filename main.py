""" 
A Standalone module that generates a list of all users and their balances on
the network and exports it in json.
"""

from collections.abc import Generator, Iterable
from typing import AsyncGenerator, Dict, Tuple, Union
import asyncio
import json
from web3 import Web3

CONTRACT_ADDRESS = "0x1eA03296FbA1006754014140caFA3807B6B21FC2"

# ERC20 ABI for the balanceOf function
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]


w3 = Web3(Web3.HTTPProvider("https://polygon-bor-rpc.publicnode.com"))
if not w3.is_connected():
    raise Exception("Not connected to a provider")


async def get_user_balances(
    user_address: str,
) -> float:
    """
    Fetch balances for a list of user addresses from an ERC20 contract lazily.

    Args:
        contract_address (str): The address of the ERC20 contract.
        user_addresses (AsyncIterable[str]): An async iterable of user addresses.

    Yields:
        Tuple[str, int]: A tuple containing the user address and their balance.
    """
    # Create a contract instance
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ERC20_ABI
    )

    try:
        # Fetch the balance of the user
        balance = contract.functions.balanceOf(
            Web3.to_checksum_address(user_address)
        ).call()
        return balance / 1_000_000
    except Exception as e:
        # Handle any errors (e.g., invalid address, contract issues)
        print(f"Error fetching balance for {user_address}: {e}")
        raise e


def user_balance_to_json(user_address: str, balance: float):
    """Converts user balance to json format"""
    return {"user_address": user_address, "balance": balance}


def load_json_array(json_file_path: str) -> Generator[Dict, None, None]:
    """
    Lazily loads JSON objects from a file containing a list of JSON objects.

    Args:
        json_file_path (str): Path to the JSON file.

    Yields:
        Dict: A single JSON object from the list.
    """
    with open(json_file_path, "r") as file:
        # Load the JSON array lazily
        data = json.load(file)
        for obj in data:
            yield obj


async def main():
    # dump to file
    balances_all: list[dict[str, Union[str, float]]] = []
    # user_addresses = ["0x8A303C86448E043689b60f29aEeCEb73ac3E79D9"]

    print(f"{'User':<15}{'Offchain':<15}{'Onchain':<15}{'Difference sync':<15}")
    print("=" * 60)
    for user in load_json_array("address-with-mpxr.json"):
        balance = await get_user_balances(user["public_address"])
        balances_all.append(
            {
                "user": user["user"],
                "public_address": user["public_address"],
                "mpxr": user["mpxr"],
                "onchain_balance": balance,
            }
        )
        with open("balances.json", "w") as f:
            json.dump(balances_all, f, indent=4)

        print(f"{user['user']:<15}{balance:<15.2f}{user['mpxr']:<15.2f}{user['mpxr'] - balance:<15.12f}")


if __name__ == "__main__":
    asyncio.run(main())
