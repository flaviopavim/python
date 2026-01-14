# Example values
invested_brl = 100
buy_price = 658000
sell_price = 666000
tax = 0.25 / 100  # 0.25% tax rate

# Function to calculate profit from a trade after taxes
def calc(buy_price, sell_price, invested_brl):
    net_investment = invested_brl * (1 - tax)  # Amount after tax deducted when buying
    amount_bought = net_investment / buy_price  # BTC or asset quantity purchased
    gross_return = amount_bought * sell_price  # Value when selling before tax
    net_return = gross_return * (1 - tax)  # Value after tax deducted on selling
    profit = net_return - invested_brl  # Net profit after all operations
    return profit

# Calculate profit
profit = calc(buy_price, sell_price, invested_brl)
print(f"Profit: R$ {profit:.2f}")

# Calculate percentage difference between buy and sell price (useful for visualization)
percentage_diff = (sell_price * 100 / buy_price) - 100
print(f"Price Difference: {percentage_diff:.2f}%")