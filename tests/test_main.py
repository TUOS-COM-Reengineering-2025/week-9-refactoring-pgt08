import unittest
import io
import contextlib

from main import CustomerManager

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        # COVERAGE: covers add_purchases
        cm.add_purchases(name, [purchase, purchase])
        # COVERAGE: covers the branch of add_purchase when the customer name already exists
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()

        cm.add_customer("Bob", [
            {'price': 600},
            # COVERAGE: Covers branch for when an item is below the taxable threshold
            {'price': 50},
            # COVERAGE: Total cost of all items makes them a VIP customer
            {'price': 400},
        ])

        # COVERAGE: Customer that does not have enough purchases for a discount
        cm.add_customer("Steve", [
            {'price': 50},
        ])

        # COVERAGE: Customer that may have a potential future discount
        cm.add_customer("Rebecca", [
            {'price': 400},
        ])

        # COVERAGE: Customer that is a priority customer but not a VIP
        cm.add_customer("Gemma", [
            {'price': 800},
        ])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 70, 'fragile': True}]

        fee = cm.calculate_shipping_fee(purchases, default=25)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = cm.calculate_shipping_fee(purchases, default=25)
        self.assertEqual(fee_fragile, 25)

if __name__ == "__main__":
    unittest.main()
