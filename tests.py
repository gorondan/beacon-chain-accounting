import unittest

from accounting import BeaconState

class TestSum(unittest.TestCase):
    def test_initiate_Delegator(self):
        """
        I should be able to add a delegator and set its balance
        """
        beaconstate = BeaconState()
        beaconstate.initiate_Delegator('Delegator_no1', 12)
        value = beaconstate.delegators_balances[0]

        self.assertEqual(value, 12)

    def test_initiate_multiple_Delegator(self):
        """
        I should be able to add multiple delegators and set their balance
        """
        beaconstate = BeaconState()
        beaconstate.initiate_Delegator('Delegator_no1', 12)
        beaconstate.initiate_Delegator('Delegator_no2', 55)
        valueDelegator_no1 = beaconstate.delegators_balances[0]
        valueDelegator_no2 = beaconstate.delegators_balances[1]

        self.assertEqual(valueDelegator_no1, 12)    
        self.assertEqual(valueDelegator_no2, 55)  

    def test_adjust_BeaconState_value(self):
        """
        I should be able to adjust the BeaconState value and have the delegators balance updated
        """

        BeaconState = BeaconState()
        BeaconState.delegate('Delegator_no1', 12)
        BeaconState.delegate('Delegator_no2', 12) 

        BeaconState.adjust_BeaconState_balance(100)

        valueDelegator_no1 = BeaconState.delegators[0].balance
        self.assertEqual(valueDelegator_no1, 62) 

    def test_adjust_BeaconState_value_quota(self):
        """
        I should be able to adjust the BeaconState value and have the delegators quota unchanged
        """

        BeaconState = BeaconState()
        BeaconState.delegate('Delegator_no1', 10)
        BeaconState.delegate('Delegator_no2', 10)
        quotaDelegator_no1 = BeaconState.delegators[0].quota
        self.assertEqual(quotaDelegator_no1, 0.5)    

        BeaconState.adjust_BeaconState_balance(100)

        quotaDelegator_no1 = BeaconState.delegators[0].quota
        self.assertEqual(quotaDelegator_no1, 0.5)


if __name__ == '__main__':
    unittest.main()