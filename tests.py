import unittest

from accounting import DelegatedValidator

class TestSum(unittest.TestCase):
    def test_add_delegate(self):
        """
        I should be able to add a delegator and set its balance
        """
        delegatedvalidator = DelegatedValidator()
        delegatedvalidator.delegate('Delegator_no1', 12)
        value = delegatedvalidator.delegators[0].balance

        self.assertEqual(value, 12)

    def test_add_multiple_delegates(self):
        """
        I should be able to add multiple delegators and set their balance
        """
        delegatedvalidator = DelegatedValidator()
        delegatedvalidator.delegate('Delegator_no1', 12)
        delegatedvalidator.delegate('Delegator_no2', 55)
        valueDelegator_no1 = delegatedvalidator.delegators[0].balance
        valueDelegator_no2 = delegatedvalidator.delegators[1].balance

        self.assertEqual(valueDelegator_no1, 12)    
        self.assertEqual(valueDelegator_no2, 55)  

    def test_adjust_DelegatedValidator_value(self):
        """
        I should be able to adjust the DelegatedValidator value and have the delegators balance updated
        """

        delegatedvalidator = DelegatedValidator()
        delegatedvalidator.delegate('Delegator_no1', 12)
        delegatedvalidator.delegate('Delegator_no2', 12) 

        delegatedvalidator.adjust_DelegatedValidator_balance(100)

        valueDelegator_no1 = delegatedvalidator.delegators[0].balance
        self.assertEqual(valueDelegator_no1, 62) 

    def test_adjust_DelegatedValidator_value_quota(self):
        """
        I should be able to adjust the DelegatedValidator value and have the delegators quota unchanged
        """

        delegatedvalidator = DelegatedValidator()
        delegatedvalidator.delegate('Delegator_no1', 10)
        delegatedvalidator.delegate('Delegator_no2', 10)
        quotaDelegator_no1 = delegatedvalidator.delegators[0].quota
        self.assertEqual(quotaDelegator_no1, 0.5)    

        delegatedvalidator.adjust_DelegatedValidator_balance(100)

        quotaDelegator_no1 = delegatedvalidator.delegators[0].quota
        self.assertEqual(quotaDelegator_no1, 0.5)


if __name__ == '__main__':
    unittest.main()