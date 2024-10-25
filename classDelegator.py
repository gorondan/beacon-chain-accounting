import numpy as np

class Delegator:

    # Custom types
    Epoch : np.uint64 = 0
    Gwei : np.uint64 = 0
    BLSPubkey: str = "Validator_nr0" #bytes = b'\x00' * 48  # 48 bytes initialized to zero

    pubkey = BLSPubkey
    withdrawal_credentials: bytes = b'\x00' * 32  # Commitment to pubkey for withdrawals
    delegated_balance =  Gwei  # Balance at stake
    # Status epochs
    activation_epoch = Epoch
    exit_epoch = Epoch
