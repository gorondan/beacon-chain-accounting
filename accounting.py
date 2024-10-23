from classDelegator import Delegator

class DelegatedValidator:
    def __init__(self):
        self.total_balance = 0  # Validator's initial effective balance 
        self.delegators = []  # Stores delegators' data as a list of delegator objects
            
    def delegate(self, pubkey, amount):
        """delegates capital to the DelegatedValidator, updates delegator's balance, and recalculates quotas."""
        if amount <= 0:
            raise ValueError("delegate amount must be positive.")

        # Update delegator's balance
        index = self.get_delegator_index_by_pubkey(pubkey)

        if  type(index) == int:
            self.delegators[index].balance += amount
                
        else:
            # append new delegator to list
            delegator = Delegator()

            delegator.pubkey = pubkey
            delegator.balance = amount
            delegator.quota = 0
            
            self.delegators.append(delegator)

        # Update total DelegatedValidator value and recalculate quotas
        self.total_balance += amount
        self._recalculate_quotas()

    def withdraw(self, delegator_index, amount):
        """Allows a delegator to withdraw up to their balance, updating their quota."""
        if delegator_index not in self.delegators:
            raise ValueError("delegator not found.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        # Ensure the delegator has sufficient balance
        delegator_balance = self.delegators[delegator_index]['balance']
        if amount > delegator_balance:
            raise ValueError(f"Amount exceeds delegator's balance: {delegator_balance:.2f}")

        # Adjust delegator's balance and total DelegatedValidator value
        self.delegators[delegator_index]['balance'] -= amount
        self.total_balance -= amount

        # Remove delegator if balance reaches zero
        if self.delegators[delegator_index]['balance'] == 0:
            del self.delegators[delegator_index]

        # Recalculate quotas to ensure they sum to 1
        self._recalculate_quotas()

    def adjust_DelegatedValidator_balance(self, change_in_value):
        """Adjusts the total DelegatedValidator value (profit/loss) without changing individual quotas."""
        self.total_balance += change_in_value
        
        if self.total_balance < 0:
            raise ValueError("DelegatedValidator total value cannot be negative.")

        for delegator in self.delegators:
            delegator.balance += change_in_value * delegator.quota
        # Quotas remain the same; balances are recalculated.

    def _recalculate_quotas(self):
        """Recalculates and updates all delegator quotas to ensure the sum is 1."""
     
        if self.total_balance == 0:
            # If the total DelegatedValidator value is zero, reset all quotas to zero
            for delegator in self.delegators:
                delegator.quota = 0
        else:
            # Recalculate quotas as a fraction of the total DelegatedValidator value
            for delegator in self.delegators:
                delegator.quota = delegator.balance / self.total_balance

        # Confirm quotas sum to 1
               
        total_quota = sum(delegator.quota for delegator in self.delegators)
        
        if abs(total_quota - 1) > 1e-6:
            raise AssertionError("Sum of quotas should be 1 but is {:.6f}".format(total_quota))

    def get_delegator_quota(self, pubkey):
        """Returns the delegator's quota as a percentage of the total DelegatedValidator."""
        if  pubkey not in self.delegators:
            raise ValueError("delegator not found.")
        return self.delegators[self.get_delegator_index_by_pubkey(pubkey)].quota
    
    def get_delegator_index_by_pubkey(self, pubkey):
        """Returns de index of a delegator with a given pubkey"""
        
        for index, delegators in enumerate(self.delegators):
            if delegators.pubkey == pubkey:
                return index

    def get_all_quotas(self):
        """Returns a dictionary with all 'quotas."""
        return {index: data.quota for index, data in self.delegators.items()}