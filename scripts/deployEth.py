from brownie import DodoCoin, accounts, network, config
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():

    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY not found in .env file")
    
    account = accounts.add(private_key)
    print(f"Using account: {account.address}")
    print(f"Wallet balance: {account.balance() / 10**18} ETH")
    # Load the deployer's account

    # Deploy the contract
    token = DodoCoin.deploy({"from": account, "gas_price": "auto"})

    # Post-deployment details
    print(f"Contract deployed at: {token.address}")
    print(f"Token name: {token.name()}")
    print(f"Token symbol: {token.symbol()}")
    print(f"Max supply: {token.MAX_SUPPLY() / (10 ** token.decimals())} DODO")
    print(f"Initial total supply: {token.totalSupply() / (10 ** token.decimals())} DODO")

    
