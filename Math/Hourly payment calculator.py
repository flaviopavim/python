import math

# Define the number of hours per day, number of days, and the hourly rate
hours_per_day = 8.48
days = 21
hourly_rate = 50

# Calculate the value per minute
minute_value = hourly_rate / 60

# Calculate the remainder of the hours in the decimal part
remainder = (hours_per_day - math.floor(hours_per_day)) * 100

# Calculate the value for the decimal part of the hours
sum1 = minute_value * remainder

# Calculate the value for the whole hours
sum2 = math.floor(hours_per_day) * hourly_rate

# Calculate the total value for the given number of days
total = (sum1 + sum2) * days

# Output the total value
print(total)
