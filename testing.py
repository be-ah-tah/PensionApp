import unittest
import take_home_income_components as thic
import math as m


class TestFinancialCalculations(unittest.TestCase):
    def test_income_tax_deduct_for_different_bands(self):
        self.assertEqual(0, thic.incomeTaxDeduct(12500))
        self.assertEqual(4986.00, m.ceil(thic.incomeTaxDeduct(37500)))
        self.assertEqual(22232.00, m.ceil(thic.incomeTaxDeduct(87000)))
        self.assertEqual(33682.00, m.ceil(thic.incomeTaxDeduct(112500)))
        self.assertEqual(55689.00, m.ceil(thic.incomeTaxDeduct(160000)))

    def text_National_insurance_deduct_for_different_bands(self):
        self.assertEqual(0, thic.nationalInsuranceDeduct(12500))
        self.assertEqual(2991.60, m.ceil(thic.nationalInsuranceDeduct(37500)))
        self.assertEqual(5258.60, m.ceil(thic.nationalInsuranceDeduct(87000)))
        self.assertEqual(5768.60, m.ceil(thic.nationalInsuranceDeduct(112500)))
        self.assertEqual(6718.60, m.ceil(thic.nationalInsuranceDeduct(160000)))


if __name__ == '__main__':
    unittest.main()