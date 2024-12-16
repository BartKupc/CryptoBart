import pytest
from brownie import accounts, DodoCoin, reverts ,config
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

@pytest.fixture(scope="module")
def dodocoin():
    # Load the private key from .env
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY not found in .env file")

    print(f"Loaded PRIVATE_KEY: {private_key}")

    # Add account using private key
    owner = accounts.add(private_key)
    print(f"Using account: {owner.address}")

    # Interact with deployed contract
    return DodoCoin.at("0xF2332E75B622C66fcaFC9240fC3A9877016d1d06")


def test_initial_state(dodocoin):
    """Test initial contract state."""
    assert dodocoin.name() == "DodoCoin3"
    assert dodocoin.symbol() == "DoDo3"
    assert dodocoin.decimals() == 18
    assert dodocoin.MAX_SUPPLY() == 1000000 * 10 ** dodocoin.decimals()


def test_transfer_to_known_wallet(dodocoin):
    """Test transferring DodoCoin to a specific wallet address."""
    owner = accounts[0]  # Loaded from private key
    recipient = "0x674D354827388821798DB803dCB849c3192702c2"  # Coinbase wallet
    balanceBefore = dodocoin.balanceOf(recipient)
    # Transfer tokens
    amount = 50 * 10 ** dodocoin.decimals()
    transfer_fee = (amount * dodocoin.transferFee()) // 100  # 2% fee
    dodocoin.transfer(recipient, amount, {"from": owner})

    # Check balances after transfer
    assert dodocoin.balanceOf(recipient) - balanceBefore  == amount - transfer_fee



def test_mint_exceeds_max_supply(dodocoin):
    """Ensure minting beyond max supply fails."""
    owner = accounts[0]
    recipient = "0x674D354827388821798DB803dCB849c3192702c2"
    # Calculate the exact excess amount to exceed MAX_SUPPLY
    excess_amount = dodocoin.MAX_SUPPLY() - dodocoin.totalSupply() + (1 * 10 ** dodocoin.decimals())
    # Try to mint more than max supply
    with reverts("ERC20: Cannot mint beyond max supply"):
        dodocoin.mint(recipient, excess_amount, {"from": owner, "allow_revert": True, "gas_limit": 200000})

def test_burn(dodocoin):
    """Test burning functionality."""
    owner = accounts[0]
    burn_amount = 200000 * 10 ** dodocoin.decimals()
    balanceBefore = dodocoin.balanceOf(owner)
    totalBefore = dodocoin.totalSupply()
    # Burn tokens
    dodocoin.burn(burn_amount, {"from": owner,"allow_revert": True, "gas_limit": 200000})

    # Check balances and supply
    assert dodocoin.balanceOf(owner) == balanceBefore - burn_amount
    assert dodocoin.totalSupply() == totalBefore - burn_amount

def test_mint(dodocoin):
    """Test minting functionality."""
    owner = accounts[0]
    recipient = "0x674D354827388821798DB803dCB849c3192702c2"
    balanceBefore = dodocoin.balanceOf(recipient)
    totalBefore = dodocoin.totalSupply()
    # Mint new tokens
    mint_amount = 100000 * 10 ** dodocoin.decimals()
    dodocoin.mint(recipient, mint_amount, {"from": owner,"allow_revert": True, "gas_limit": 200000})

    # Check balances and supply
    assert dodocoin.balanceOf(recipient) - balanceBefore == mint_amount
    assert dodocoin.totalSupply() == totalBefore + mint_amount



def test_pause_and_unpause(dodocoin):
    """Test pause and unpause functionality."""
    owner = accounts[0]
    recipient = "0x674D354827388821798DB803dCB849c3192702c2"
    amount = 1 * 10 ** dodocoin.decimals()
    balanceBefore = dodocoin.balanceOf(recipient)
    # Pause contract
    dodocoin.pause({"from": owner})

    # Attempt transfer while paused
    with reverts():
        dodocoin.transfer(recipient, amount, {"from": owner,"allow_revert": True, "gas_limit": 200000})

    # Unpause contract
    dodocoin.unpause({"from": owner})
    
    assert dodocoin.balanceOf(recipient) == balanceBefore
    
    transfer_fee = (amount * dodocoin.transferFee()) // 100  # 2% fee
    dodocoin.transfer(recipient, amount, {"from": owner})

    # Check balances after transfer
    assert dodocoin.balanceOf(recipient) - balanceBefore  == amount - transfer_fee



def test_set_transfer_fee(dodocoin):
    """Test updating the transfer fee."""
    owner = accounts[0]
    new_fee = 6  # 6%

    # Update transfer fee
    dodocoin.setTransferFee(new_fee, {"from": owner})
    assert dodocoin.transferFee() == new_fee

    # Try setting fee too high
    with reverts("ERC20: Fee too high"):
        dodocoin.setTransferFee(11, {"from": owner,"allow_revert": True, "gas_limit": 200000})  # Fee > 10%


def test_voting(dodocoin):
    """Test ERC20Votes functionality."""
    owner = accounts[0]
    delegatee = "0x674D354827388821798DB803dCB849c3192702c2"

    # Delegate votes
    dodocoin.delegate(delegatee, {"from": owner})
    assert dodocoin.delegates(owner) == delegatee

    # Check voting power
    votes = dodocoin.getVotes(delegatee)
    assert votes == dodocoin.balanceOf(owner)


def test_permit(dodocoin, web3):
    """Test ERC20Permit functionality."""
    owner = accounts[0]
    spender = "0x674D354827388821798DB803dCB849c3192702c2"
    amount = 1000 * 10 ** dodocoin.decimals()
    deadline = web3.eth.get_block("latest")["timestamp"] + 3600  # 1 hour from now

    # Generate permit signature
    nonce = dodocoin.nonces(owner)
    chain_id = web3.eth.chain_id
    message = {
        "owner": owner.address,
        "spender": spender,
        "value": amount,
        "nonce": nonce,
        "deadline": deadline,
    }

    # Generate signature using web3.eth.sign
    # Replace this with proper EIP712 signing logic
    # signature = web3.eth.sign(owner, message)  # Example

    # Call permit function (pseudo-code example below)
    # dodocoin.permit(owner, spender, amount, deadline, v, r, s, {"from": spender})
    # assert dodocoin.allowance(owner, spender) == amount
