from brownie import DodoCoin, accounts, network

def main():
    print(f"Active network: {network.show_active()}")
    # Deploy the contract
    account = accounts[0]
    token = DodoCoin.deploy(1000, {"from": account})

    # Check initial balance
    owner_balance = token.balanceOf(account.address) / (10 ** token.decimals())
    print(f"Owner initial balance: {owner_balance} DODO")

    # Transfer tokens
    recipient = accounts[1]
    transfer_amount = 100
    token.transfer(recipient.address, transfer_amount * (10 ** token.decimals()), {"from": account})
    recipient_balance = token.balanceOf(recipient.address) / (10 ** token.decimals())
    print(f"Transferred {transfer_amount} DODO to {recipient.address}")
    print(f"Recipient balance: {recipient_balance} DODO")

    # Approve spender
    spender = accounts[2]
    approval_amount = 50
    token.approve(spender.address, approval_amount * (10 ** token.decimals()), {"from": account})
    allowance = token.allowance(account.address, spender.address) / (10 ** token.decimals())
    print(f"Approved {spender.address} to spend {allowance} DODO")

    # Transfer using transferFrom
    transfer_from_amount = 20
    token.transferFrom(account.address, recipient.address, transfer_from_amount * (10 ** token.decimals()), {"from": spender})
    new_recipient_balance = token.balanceOf(recipient.address) / (10 ** token.decimals())
    new_allowance = token.allowance(account.address, spender.address) / (10 ** token.decimals())
    print(f"New recipient balance after transferFrom: {new_recipient_balance} DODO")
    print(f"Remaining allowance: {new_allowance} DODO")
    

    # Mint new tokens
    mint_amount = 500
    token.mint(account.address, mint_amount, {"from": account})
    new_owner_balance = token.balanceOf(account.address) / (10 ** token.decimals())
    print(f"Minted {mint_amount} DODO. New owner balance: {new_owner_balance} DODO")

    # Burn tokens
    burn_amount = 200
    token.burn(burn_amount, {"from": account})
    final_owner_balance = token.balanceOf(account.address) / (10 ** token.decimals())
    print(f"Burned {burn_amount} DODO. Final owner balance: {final_owner_balance} DODO")
