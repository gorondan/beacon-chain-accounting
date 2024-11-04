from typing import List
import numpy as np
from classDelegator import Delegator
from classValidator import Validator

# State list lengths
VALIDATOR_REGISTRY_LIMIT = 100  # Validator registry size limit
DELEGATOR_REGISTRY_LIMIT = 100  # Delegator registry size limit


# Custom types
Gwei = np.uint64
Fee =  np.uint
Quota =  np.uint
delegator_index = np.uint
validator_index = np.uint

class DelegatorsRegistry:
    delegators: List[Delegator]  # Stores delegators' data as a list of Delegator instances.
    delegators_balances: List[Gwei]  # List of Gwei delegators' balances
    delegators_quotas: List[Quota]  # List of delegators' quotas
    
    def __init__(self):
        # Delegators lists initialization
        self.delegators: List[Delegator] = []     
        self.delegators_balances: List[Gwei] = [] # Max size: DELEGATOR_REGISTRY_LIMIT
        self.delegators_quotas: List[Quota] = [] 

    def register_delegator(self, delegator_id):
        """Registers a delegator if not already registered and returns the delegator index."""
        for index, delegator in enumerate(self.delegators):
            if delegator.delegator_id == delegator_id:
                return index  # Delegator already exists; return the index

        # Register new delegator with a zero balance
        new_delegator = Delegator(delegator_id)
        self.delegators.append(new_delegator)
        self.delegators_balances.append(0)  # Initial balance is 0
        return len(self.delegators) - 1  # Return the index of the newly added delegator

    def deposit(self, delegator_id, amount):
        """Adds an amount to the balance of an existing or newly registered delegator."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        # Register the delegator if they don't exist and get their index
        delegator_index = self.register_delegator(delegator_id)
        # Add the deposit amount to the delegator's balance
        self.delegators_balances[delegator_index] += amount
        return delegator_index


class DelegatedValidator:
    delegators_balances: List[Gwei]  # List of Gwei delegators' balances

    validators: List[Validator]  # Stores validators' data as a list of Validator instances.
    validators_balances: List[Gwei]  # List of Gwei validators' balances
    validators_fees: List[Fee]  # List of Gwei validators' balances
    
    def __init__(self, validator_id):
        # Valaidators lists initialization
        self.validators: List[Validator] = [] 
        self.validators_balances: List[Gwei] = 0 # Max size: VALIDATOR_REGISTRY_LIMIT
        #BROKEN self.validators_fees: List[Fee] = []
        self.validator = Validator(validator_id)
        
        self.delegators_balances = []  # Track delegated balances for each delegator in this validator

    def delegate(self, delegator_index, amount):
        """Transfers capital from a delegator to the validator, updating both balances."""
        if amount <= 0:
            raise ValueError("Delegation amount must be positive.")
        
        # Ensure the validator's balance list is large enough to accommodate the delegator
        while len(self.delegators_balances) <= delegator_index:
            self.delegators_balances.append(0)

        # Deduct from the delegator's balance and add to the validator's balance
        self.delegators_balances[delegator_index] += amount
        self.validators_balances += amount

        # Return updated quotas for this validator
        return self.calculate_quotas()

    def withdraw(self, delegator_index, amount):
        """Withdraws a specified amount from a delegator's balance in this validator,
           returning it to the delegator's available balance."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        # Ensure the withdrawal amount does not exceed the delegator's balance in the validator
        if amount > self.delegators_balances[delegator_index]:
            raise ValueError("Withdrawal amount exceeds the delegator's delegated balance in this validator.")

        # Add to the delegator's balance and deduct from the validator's balance
        self.delegators_balances[delegator_index] -= amount
        self.validators_balances -= amount

        # Recalculate and return updated quotas after the withdrawal
        return self.calculate_quotas()

    def calculate_quotas(self):
        """Calculate and return the quota for each delegator in this validator."""
        total_balance = self.validators_balances
        
        # Avoid division by zero if there is no balance
        if total_balance == 0:
            return [(index, 0.0) for index in range(len(self.delegators_balances))]
        
        # Calculate quotas for each delegator
        quotas = [(index, balance / total_balance) for index, balance in enumerate(self.delegators_balances)]
        return quotas

class BeaconChainAccounting:
    def __init__(self):
        self.validators = []  # List of DelegatedValidator instances
        self.delegators_registry = DelegatorsRegistry()  # Registry to manage delegators

    def add_validator(self, validator_id):
        """Add a new validator with a specific ID."""
        validator = DelegatedValidator(validator_id)
        self.validators.append(validator)
        return validator_id  # Return the validator_id of the newly added validator

    def get_validator_index(self, validator_id):
        """Helper function to find a validator's index by its ID."""
        for index, validator in enumerate(self.validators):
            if validator.validator.validator_id == validator_id:
                return index
        raise ValueError("Validator not found.")

    def deposit(self, delegator_id, amount):
        """Deposit capital from outside the system to a delegator's balance."""
        return self.delegators_registry.deposit(delegator_id, amount)

    def delegate(self, delegator_id, validator_id, amount):
        """Transfer capital from a delegator's balance to a specific validator's balance."""
        # Get validator index by its ID
        validator_index = self.get_validator_index(validator_id)

        # Ensure the delegator exists and retrieve their index
        delegator_index = self.delegators_registry.register_delegator(delegator_id)

        # Ensure the delegator has sufficient balance to delegate
        if amount > self.delegators_registry.delegators_balances[delegator_index]:
            raise ValueError("Delegation amount exceeds the delegator's available balance.")

        # Deduct the delegation amount from the delegator's remaining balance
        self.delegators_registry.delegators_balances[delegator_index] -= amount

        # Delegate the amount to the validator
        return self.validators[validator_index].delegate(delegator_index, amount)
    
    def adjust_DelegatedValidator_balance(self, validator_id, change_in_value): #BROKEN
        """Adjusts the total DelegatedValidator value (profit/loss) without changing individual quotas."""
        
        # Get validator index by its ID
        validator_index = self.get_validator_index(validator_id)
        
        self.validators[validator_index].validators_balances += change_in_value
    
        if self.validators[validator_index].validators_balances < 0:
            raise ValueError("DelegatedValidator total value cannot be negative.")

        for delegator_index in enumerate(self.validators[validator_index].delegators_balances):
            self.delegators_registry.delegators_balances[delegator_index] += change_in_value * self.delegators_registry.delegators_quotas[delegator_index]
        # Quotas remain the same; balances are recalculated.

    def withdraw(self, delegator_id, validator_id, amount):
        """Withdraw capital from a validator's balance back to the delegator's available balance."""
        # Get validator index by its ID
        validator_index = self.get_validator_index(validator_id)

        # Get the delegator's index from the registry
        delegator_index = self.delegators_registry.register_delegator(delegator_id)

        # Perform the withdrawal from the specified validator
        result = self.validators[validator_index].withdraw(delegator_index, amount)

        # Add the withdrawn amount back to the delegator's balance
        self.delegators_registry.delegators_balances[delegator_index] += amount

        return result

    def get_all_quotas_by_delegator(self):
        """
        Return a list of delegators with their quotas across all validators.
        Each entry contains the delegator ID and a list of their quotas across validators.
        """
        delegators_quotas = []
        
        # Iterate over each delegator in the registry
        for delegator_index, delegator in enumerate(self.delegators_registry.delegators):
            quotas = []
            for validator in self.validators:
                # If the delegator exists in the current validator, get their quota
                if delegator_index < len(validator.delegators_balances):
                    quota = validator.calculate_quotas()[delegator_index][1]
                else:
                    quota = 0.0  # Quota is 0 if the delegator has no balance in this validator
                quotas.append(quota)
            
            # Append delegator ID and their quotas across validators
            delegators_quotas.append((delegator.delegator_id, quotas))
        
        return delegators_quotas


# Example usage
accounting = BeaconChainAccounting()

# Add multiple validators
accounting.add_validator("validator_1")
accounting.add_validator("validator_2")

# Deposit funds into delegators' accounts
accounting.deposit("delegator_A", 500)
accounting.deposit("delegator_B", 400)

# Delegate funds from delegators to validators
accounting.delegate("delegator_A", "validator_1", 100)  # Delegator A delegates 100 to Validator 1
accounting.delegate("delegator_B", "validator_1", 200)
accounting.delegate("delegator_A", "validator_2", 50)
accounting.delegate("delegator_B", "validator_2", 150)

# Withdraw funds from validators back to delegators
print(accounting.withdraw("delegator_A", "validator_1", 50))  # Withdraw 50 from Validator 1 for Delegator A
print(accounting.withdraw("delegator_B", "validator_2", 100))  # Withdraw 100 from Validator 2 for Delegator B

# Get quotas by delegator across all validators
print(accounting.get_all_quotas_by_delegator())
