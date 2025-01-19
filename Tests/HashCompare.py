# A programming course student asked to create this code

# Function to compare the hashes
def compare(hash_string):
    
    # Split the hash pairs
    hashes = hash_string.split(";")
    
    # Iterate over the pairs
    for item in hashes:
        
        # Split the hashes
        pair = item.split(",")
        
        # Compare the hashes
        if pair[0] == pair[1]:
            print("Correct")
        else:
            print("Incorrect")
    
# Test the function
compare("abc123,abc123;def456,def457")