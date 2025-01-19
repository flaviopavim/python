"""
This script calculates the coordinates of a point C (Xc, Yc) that lies on the line passing through points A (Xa, Ya) and B (Xb, Yb). 
The user can specify either Xc or Yc, and the script calculates the other coordinate using the equation of the line.

Key Features:
1. Accepts coordinates of two points A and B to define a line.
2. Calculates the missing coordinate (Xc or Yc) of point C using the line equation.
3. Ensures input validation by requiring at least one coordinate (Xc or Yc) of point C to be provided.
"""
def calculate_point_c(Xa, Ya, Xb, Yb, Xc=None, Yc=None):
    # Validates that at least one coordinate (Xc or Yc) is provided
    if Xc is None and Yc is None:
        raise ValueError("At least one value for Xc or Yc must be provided.")
    
    # If Xc is provided, calculates Yc using the line equation
    if Xc is not None:
        Yc = ((Xc - Xa) * (Yb - Ya) / (Xb - Xa)) + Ya
    
    # If Yc is provided, calculates Xc using the line equation
    elif Yc is not None:
        Xc = ((Yc - Ya) * (Xb - Xa) / (Yb - Ya)) + Xa
    
    return Xc, Yc

# Example usage:
Xa, Ya = 1, 2
Xb, Yb = 4, 5

# Calculates coordinates of C based on Xc
Xc, Yc = calculate_point_c(Xa, Ya, Xb, Yb, Xc=3)
print(f"Coordinates of C: ({Xc}, {Yc})")

# Calculates coordinates of C based on Yc
Xc, Yc = calculate_point_c(Xa, Ya, Xb, Yb, Yc=4)
print(f"Coordinates of C: ({Xc}, {Yc})")
