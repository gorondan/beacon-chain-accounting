import numpy as np

class Validator:
    
    # Custom types
    Epoch : np.uint64 = 0
    Gwei : np.uint64 = 0
    BLSPubkey : bytes = b'\x00' * 48  # 48 bytes initialized to zero
    
    pubkey = BLSPubkey
    withdrawal_credentials: bytes = b'\x00' * 32  # Commitment to pubkey for withdrawals
    effective_balance = Gwei  # Balance at stake
    slashed: bool
    # Status epochs
    activation_eligibility_epoch = Epoch  # When criteria for activation were met
    activation_epoch = Epoch
    exit_epoch = Epoch
    withdrawable_epoch = Epoch  # When validator can withdraw funds
    delegated: bool # new in eODS