"""
This script calculates income, expenses, and savings to determine the timeline for purchasing items from a predefined shopping list. 

Key Features:
1. Converts numerical values into Brazilian reais format for better readability.
2. Calculates total monthly, annual, weekly, and daily expenses based on categorized inputs.
3. Simulates monthly savings by deducting expenses from income and accumulates the remaining balance.
4. Determines when items on the shopping list can be purchased based on available savings.
5. Outputs a detailed timeline for purchases, including the remaining balance after each transaction.
"""

import math

# Converts a decimal value into a currency string in Brazilian reais
def to_currency(value):
    result = 'R$ '
    result += '{0:.2f}'.format(value)
    return str(result)

# Sums all items in an array
def sum_array(array):
    total = 0
    for val in array:
        total += val
    return total

# Your monthly income
monthly_income_array = [
    9200  # Example: Monthly income
    # 4000,
    # 4800,
    # 5200
]

monthly_income = sum_array(monthly_income_array)

print("Monthly Income:  " + to_currency(monthly_income) + "")
print("--------------------------")

# Your annual expenses
annual_expenses_array = [
    420,  # Example: Motorbike expenses
]

# Your monthly expenses
monthly_expenses_array = [
    750,  # Rent
    120,  # Internet
    200,  # Electricity
    60,   # Water
]

# Your weekly expenses
weekly_expenses_array = [
    450,  # Groceries
    350,  # Delivery
    50,   # Herbs
    50,   # Cat food/litter
]

# Add all expenses to calculate monthly expenses for subsequent calculations
monthly_expenses = sum_array(monthly_expenses_array)
monthly_expenses += (sum_array(annual_expenses_array) / 12)
monthly_expenses += (sum_array(weekly_expenses_array) / 7 * 30)

# Break down expenses into annual, monthly, weekly, and daily categories
annual_expenses = monthly_expenses * 12
daily_expenses = monthly_expenses / 30
weekly_expenses = daily_expenses * 7

print("Annual Expenses:   " + to_currency(annual_expenses))
print("Monthly Expenses:  " + to_currency(monthly_expenses))
print("Weekly Expenses:   " + to_currency(weekly_expenses))
print("Daily Expenses:    " + to_currency(daily_expenses))
print("----------------------------------")

if monthly_income < monthly_expenses:
    print("Your expenses exceed your income")
    print("Total Expenses: " + to_currency(monthly_expenses))
    print("----------------------------------")

# Items you want to buy
shopping_list = [
    {"item": "house", "price": 200000},
    # {"item": "harley davidson", "price": 80000},
    {"item": "car", "price": 40000},
    {"item": "drum kit", "price": 7000},
    {"item": "vacuum cleaner", "price": 650},
    {"item": "washing machine", "price": 2700},
    {"item": "refrigerator", "price": 3000},
    {"item": "stove", "price": 600},
    {"item": "fountain for cats", "price": 120},
    {"item": "graphics card", "price": 3800},
    # {"item": "trip", "price": 15000},
]

total_savings = 0
for month in range(10000):
    total_savings += (monthly_income - monthly_expenses)
    can_afford = False
    output = ""
    for item in shopping_list:
        if total_savings >= item["price"]:
            can_afford = True
    if can_afford:
        years = math.floor((month + 1) / 12)
        months = (month + 1) - (years * 12)
        output = ""
        if years == 1:
            output += f"In {years} year"
        elif years > 1:
            output += f"In {years} years"
        if years > 0 and months > 0:
            output += " and "
        if months == 1:
            output += f"{months} month"
        elif months > 1:
            output += f"{months} months"
        print(output)

    # Adjust savings after purchases
    temp_savings = total_savings
    shopping_list_copy = []
    output = ""
    for item in shopping_list:
        if temp_savings >= item["price"]:
            output += f"Buy {item['item']} {to_currency(temp_savings)} - {to_currency(item['price'])} = {to_currency(temp_savings - item['price'])}\n"
            temp_savings -= item["price"]

    for item in shopping_list:
        if total_savings >= item["price"]:
            total_savings -= item["price"]
        else:
            shopping_list_copy.append(item)
    shopping_list = shopping_list_copy
    if output != "":
        print(output + "----------------------------------")
