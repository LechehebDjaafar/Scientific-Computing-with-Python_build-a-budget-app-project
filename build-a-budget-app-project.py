class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __str__(self):
        # Title line
        result = f"{self.name:*^30}\n"
        # Ledger items
        for item in self.ledger:
            description = item["description"][:23]
            amount = f"{item['amount']:.2f}"
            result += f"{description:<23}{amount:>7}\n"
        # Total line
        result += f"Total: {self.get_balance():.2f}"
        return result


def create_spend_chart(categories):
    # Calculate total spent and percentage spent per category
    total_spent = 0
    spent_per_category = []
    for category in categories:
        spent = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        spent_per_category.append(spent)
        total_spent += spent
    
    percentages = [(spent / total_spent) * 100 for spent in spent_per_category]

    # Create chart
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}|"
        for percentage in percentages:
            chart += " o " if percentage >= i else "   "
        chart += " \n"
    
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"
    
    # Add category names vertically
    max_length = max(len(category.name) for category in categories)
    category_names = [category.name.ljust(max_length) for category in categories]
    for i in range(max_length):
        chart += "     "
        for name in category_names:
            chart += f"{name[i]}  "
        chart += "\n"
    
    return chart.rstrip("\n")


# Example Usage
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")

clothing = Category("Clothing")
clothing.deposit(500, "initial deposit")
clothing.withdraw(50.50, "jeans")
clothing.withdraw(30.00, "jacket")

auto = Category("Auto")
auto.deposit(200, "initial deposit")
auto.withdraw(50.00, "gasoline")

# Print category details
print(food)
print(clothing)
print(auto)

# Print spend chart
print(create_spend_chart([food, clothing, auto]))
