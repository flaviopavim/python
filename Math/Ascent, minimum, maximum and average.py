# Initial stack
stack = [3, 8, 1, 6, 4]  # Predefined list of numbers
# Alternatively, the stack can start empty (uncomment the next line)
# stack = []

# Function to return minimum, average, and maximum
def getMinAvgMax(stack):
    stack.sort()  # Sorts the stack in ascending order
    minimum = stack[0]  # The smallest value (first element in the sorted list)
    maximum = stack[-1]  # The largest value (last element in the sorted list)
    total = count = 0  # Initialize sum and counter to zero

    # Iterate through the stack
    for number in stack:
        # Add each number in the stack to the total variable
        total += number
        # Count the number of elements in the stack
        count += 1

    # Calculate the average
    average = total / count

    # Return the minimum, maximum, and average as a list
    return [minimum, maximum, average]

# Add more elements to the stack
stack.append(9)  # Add 9 to the stack
stack.append(2)  # Add 2 to the stack
stack.append(5)  # Add 5 to the stack
stack.append(0)  # Add 0 to the stack
stack.pop()      # Remove the last element from the stack

# Sort the stack in ascending order
stack.sort()  # Organize the stack in ascending order
print('Ascending order: ')
print(stack)

# Store the minimum, maximum, and average in the variable 'myStack'
myStack = getMinAvgMax(stack)

# Print the results
print('Minimum, maximum, and average: ')
print(myStack)
