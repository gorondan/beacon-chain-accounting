import unittest

from beacon_chain_accounting import DelegatorsRegistry, DelegatedValidator, BeaconChainAccounting

class TestSum(unittest.TestCase):
    def test_initiate_Delegator(self):
        """
        I should be able to add a delegator and set its balance
        """
        delegatorsregistry = DelegatorsRegistry()

        delegatorsregistry.register_delegator('Delegator_no1')
        delegatorsregistry.deposit('Delegator_no1', 12)
        value = delegatorsregistry.delegators_balances[0]

        self.assertEqual(value, 12)

    def test_initiate_multiple_Delegator(self):
        """
        I should be able to add multiple delegators and set their balance (deposit)
        """
        delegatorsregistry = DelegatorsRegistry()

        delegatorsregistry.register_delegator('Delegator_no1')
        #delegatorsregistry.register_delegator('Delegator_no2') # Intentionally left the first one un-registered to test if `deposit` correctly registers delegators, even if they don't exist
        delegatorsregistry.deposit('Delegator_no1', 12)
        delegatorsregistry.deposit('Delegator_no2', 12)
        value_for_delegator_no1 = delegatorsregistry.delegators_balances[0]
        value_for_delegator_no2 = delegatorsregistry.delegators_balances[1]

        self.assertEqual(value_for_delegator_no1, 12)
        self.assertEqual(value_for_delegator_no2, 12)

    def test_delegate(self):
        """
        I should be able to delegate to a delegated validator and update the quotas of the delegators that delegated towards that particular validator.
        """
        accounting = BeaconChainAccounting()
     
        for _ in range(2): 
            accounting.add_validator('Validator_no'+ f'{str(_ + 1)}')

        accounting.deposit('Delegator_no1', 500)
        accounting.deposit('Delegator_no2', 400)
        
        # Delegate funds from delegators to validators
        accounting.delegate("Delegator_no1", "Validator_no1", 100)  # Delegator 1 delegates 100 to Validator 1
        accounting.delegate("Delegator_no2", "Validator_no1", 200)
        accounting.delegate("Delegator_no1", "Validator_no2", 50)
        accounting.delegate("Delegator_no2", "Validator_no2", 150)

        value = accounting.validators[0].validators_balances
        self.assertEqual(value, 300)

        value = accounting.delegators_registry.delegators_balances[0]
        self.assertEqual(value, 350)

        value = accounting.delegators_registry.delegators_balances[1]
        self.assertEqual(value, 50)

        # Get quotas by delegator across all validators
        print(accounting.get_all_quotas_by_delegator())
    
    def test_adjust_accounting(self):
        """
        I should be able to adjust the validator's balance (due to profit / loss) and have the delegators' balances updated
        """
        accounting = BeaconChainAccounting()
     
        for _ in range(2): 
            accounting.add_validator('Validator_no'+ f'{str(_ + 1)}')

        accounting.deposit('Delegator_no1', 150)
        accounting.deposit('Delegator_no2', 350)
        
        # Delegate funds from delegators to validators
        accounting.delegate("Delegator_no1", "Validator_no1", 100)  # Delegator 1 delegates 100 to Validator 1
        accounting.delegate("Delegator_no2", "Validator_no1", 200)
        accounting.delegate("Delegator_no1", "Validator_no2", 50)
        accounting.delegate("Delegator_no2", "Validator_no2", 150)

        accounting.adjust_DelegatedValidator_balance('Validator_no1', 100)

        valueDelegator_no1 = accounting.delegators_registry.delegators_balances[0]
        self.assertEqual(valueDelegator_no1, 0) 
    
    def test_adjust_accounting_value_quota(self):
        """
        I should be able to adjust the accounting value and have the delegators quota unchanged
        """

        accounting = BeaconChainAccounting()
        accounting.delegate('Delegator_no1', 10)
        accounting.delegate('Delegator_no2', 10)
        quotaDelegator_no1 = accounting.delegators[0].quota
        self.assertEqual(quotaDelegator_no1, 0.5)    

        accounting.adjust_accounting_balance(100)

        quotaDelegator_no1 = accounting.delegators[0].quota
        self.assertEqual(quotaDelegator_no1, 0.5)


if __name__ == '__main__':
    unittest.main()