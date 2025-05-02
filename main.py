class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.tax_rate = 0.2
        self.tax_threshold = 100
        self.future_discount_threshold = 300
        self.discount_threshold = 500
        self.priority_threshold = 800
        self.vip_threshold = 1000

    def add_customer(self, name, purchases):
        if name in self.customers.keys():
            self.customers[name].extend(purchases)
        else:
            self.customers[name] = purchases

    def add_purchase(self, name, purchase):
        self.add_customer(name, [purchase])

    def add_purchases(self, name, purchases):
        self.add_customer(name, purchases)

    def generate_report(self):
        for customer_name, purchase_list in self.customers.items():
            price_total = 0
            for purchase in purchase_list:
                if purchase['price'] > self.tax_threshold:
                    taxed_price = purchase['price'] * (1 + self.tax_rate)
                    price_total += taxed_price
                else:
                    price_total += purchase['price']
            print(customer_name)
            if price_total > self.discount_threshold:
                print("Eligible for discount")
            else:
                if price_total > self.future_discount_threshold:
                    print("Potential future discount customer")
                else:
                    print("No discount")
            if price_total > self.vip_threshold:
                print("VIP Customer!")
            else:
                if price_total > self.priority_threshold:
                    print("Priority Customer")

    def calculate_shipping_fee(self, purchases, default: int = 20):
        heavy_item = False
        fragile_item = False

        for purchase in purchases:
            # If any item is fragile then the shipping fee is the fragile rate
            if purchase.get('fragile', False):
                fragile_item = True
                break

            # If any item exceeds the weight threshold then the shipping fee is the heavy rate
            if purchase.get('weight', 0) > 20:
                heavy_item = True
                break

        if fragile_item:
            return 60
        elif heavy_item:
            return 50
        else:
            return default
