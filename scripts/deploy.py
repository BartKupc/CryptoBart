from brownie import DodoCoin, accounts, network, config
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Load private key from .env
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY not found in .env file")

    # Ensure network is Base Sepolia
    if network.show_active() != "base-sepolia":
        raise ValueError("Please switch to the Base Sepolia network in Brownie configuration")

    # Add account using private key
    account = accounts.add(private_key)
    print(f"Using account: {account.address}")
    print(f"Wallet balance: {account.balance() / 10**18} ETH")

    # Deploy the contract
    print("Deploying DodoCoin contract...")
    token = DodoCoin.deploy(
        {"from": account, "gas_price": "auto"}
    )

    # Post-deployment details
    print(f"Contract deployed at: {token.address}")
    print(f"Token name: {token.name()}")
    print(f"Token symbol: {token.symbol()}")
    print(f"Max supply: {token.MAX_SUPPLY() / (10 ** token.decimals())} DODO")
    print(f"Initial total supply: {token.totalSupply() / (10 ** token.decimals())} DODO")
