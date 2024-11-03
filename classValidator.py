import numpy as np

class Validator:
    def __init__(self, validator_id):
        self.validator_id = validator_id  # Unique identifier for each validator
        
        # Custom types
        Epoch : np.uint64 = 0
        Gwei : np.uint64 = 0
        BLSPubkey : str
    
        # pubkey = BLSPubkey # for the purpose of this pyproject, we work with validator_id instead of BLSPubkey, which will be used in the specs
        self.withdrawal_credentials: bytes = b'\x00' * 32  # Commitment to pubkey for withdrawals
        self.effective_balance = Gwei  # Balance at stake
        self.slashed: bool
        # Status epochs
        self.activation_eligibility_epoch = Epoch  # When criteria for activation were met
        self.activation_epoch = Epoch
        self.exit_epoch = Epoch
        self.withdrawable_epoch = Epoch  # When validator can withdraw funds
        self.delegated: bool # new in eODS