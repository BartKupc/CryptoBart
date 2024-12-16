// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v5.1.0) (token/ERC20/ERC20.sol)

pragma solidity ^0.8.28;

import "../../node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "../../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../../node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "../../node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "../../node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import "../../node_modules/@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "../../node_modules/@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract DodoCoin is ERC20, ERC20Burnable, Ownable , ERC20Pausable, ERC20Permit, ERC20Votes, ReentrancyGuard {

    uint256 public immutable MAX_SUPPLY = 1_000_000 * 10**decimals();
    uint256 public transferFee = 5; // Default fee: 5%
    bool private initialized;

    constructor() ERC20("DodoCoin3", "DoDo3" ) ERC20Permit("DodoCoin3") Ownable(msg.sender) {
        require(!initialized, "Contract is already initialized");
        initialized = true;
        _mint(msg.sender, 100000 * 10**decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner nonReentrant {
        require(totalSupply() + amount <= MAX_SUPPLY, "ERC20: Cannot mint beyond max supply");
        _mint(to, amount);
    }

    function burn(uint256 amount) public virtual override nonReentrant {
        _burn(_msgSender(), amount);
    }

    function pause() public onlyOwner nonReentrant {
        _pause();
    }

    function unpause() public onlyOwner nonReentrant {
        _unpause();
    }

    function setTransferFee(uint256 fee) public onlyOwner nonReentrant {
        require(fee <= 10, "ERC20: Fee too high"); // Max fee is 10%
        transferFee = fee;
    }

    function _update(address from, address to, uint256 value) internal override(ERC20, ERC20Pausable, ERC20Votes){
        uint256 fee = (value * transferFee) / 100; // Calculate 2% fee
        uint256 amountAfterFee = value - fee;

        // Ensure the fee only applies to non-zero transfers
        if (from != address(0) && to != address(0) && fee > 0) {
            super._update(from, owner(), fee);      // Transfer the fee to the owner
            super._update(from, to, amountAfterFee); // Transfer the remaining amount to the recipient
        } else {
            super._update(from, to, value); // Default behavior for minting, burning, etc.
        }
    }

    
    function nonces(address owner) public view override(ERC20Permit, Nonces) returns (uint256)
    {
        return super.nonces(owner);
    }
}