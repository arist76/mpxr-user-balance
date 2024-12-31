""" 
A Standalone module that generates a list of all users and their balances on
the network and exports it in json.
"""

from collections.abc import Iterable
from typing import AsyncIterable, AsyncGenerator, Tuple
import asyncio
from web3 import Web3

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
    contract_address: str, user_addresses: Iterable[str]
) -> AsyncGenerator[Tuple[str, int], None]:
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
        address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI
    )

    for user_address in user_addresses:
        try:
            # Fetch the balance of the user
            balance = contract.functions.balanceOf(
                Web3.to_checksum_address(user_address)
            ).call()
            yield user_address, balance/1_000_000
        except Exception as e:
            # Handle any errors (e.g., invalid address, contract issues)
            print(f"Error fetching balance for {user_address}: {e}")
            raise e


async def main():
    async for balance in get_user_balances(
        "0x1eA03296FbA1006754014140caFA3807B6B21FC2",
        [
            "0x8A303C86448E043689b60f29aEeCEb73ac3E79D9",
            "0x17Df8A46B8e3f32E8EcdB8e0EEAd515dB427fe74",
            "0x77C8A535eB970F13717501D5Bc8D4dCe69E949DC",
            "0x9747da9F31c5C80E637619B6386DdB7ff4a6de87",
        ],
    ):
        print(balance)


if __name__ == "__main__":
    asyncio.run(main())
