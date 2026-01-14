# Example values
coin = 658000     # Current price of the coin (e.g., Bitcoin)
investment = 100  # How much do you want to invest?
profit_goal = 0   # Desired profit in BRL (not in %)
fee = 0.21         # Exchange fee (%)

#############################################################################
# Magic ✨
purchased = investment - ((investment * fee) / 100)  # Net amount after fee on buying

# Function to search for the selling price (target) that gives the desired profit
def findTarget(coin, investment, profit_goal):
    net_profit = target = 0
    while net_profit < investment:
        gross_return = (target * purchased) / coin  # Value obtained when selling
        net_profit = gross_return - profit_goal - ((gross_return * fee) / 100)  # After subtracting fees and desired profit
        target += coin / 10000  # Increment target slightly
    return [target - (coin / 10000), net_profit]  # Subtract last increment to get actual target

# Get target selling price and real profit after fee
result = findTarget(coin, investment, profit_goal)
target_sell = result[0]
net_profit = result[1]

# Display results
print('Coin Price:              ' + str(coin))
print('Investment:              ' + str(investment))
print('Amount after Fee:        ' + str(purchased))
print('Desired Profit:          ' + str(profit_goal))
print('Target Sell Price:       ' + str(target_sell))
print('Gross Return:            ' + str(target_sell * purchased / coin))
print('Net Profit after Fees:   ' + str(net_profit + profit_goal))

### Reverse Calculation #####################################################
# If you force a different sell target, this shows what the new buy price would be
# Useful to track price movement and adjust buying strategy accordingly
#############################################################################

# target_sell = 170000  # Uncomment to test with a custom sell target

reverse = purchased * target_sell / (net_profit + profit_goal)
target_buy = reverse - (reverse * fee / 100)

print('Target Buy Price:        ' + str(target_buy))

# Optional: show how much % increase from original coin price to target sell
print('Sell Target (% up):      ' + str((target_sell * 100 / coin)))
