# Secret Santa draw script
# This script randomly shuffles a list of names and assigns each person to another as their "Secret Santa."
# The last person in the shuffled list is assigned to the first person, ensuring a complete loop.

import random

# List of participants in the Secret Santa
amigos = [
    'flavio',
    'leo',
    'patrick',
    'jabá',
    'kicko',
    'cego',
    'nightmare',
    'hasan'
]

# Shuffle the list randomly to ensure fairness
random.shuffle(amigos)

# Assign each person a recipient
for contador_1 in range(len(amigos)):
    contador_2 = contador_1 + 1  # Next person in the list
    if contador_2 == len(amigos):  # Wrap around to the first person if at the end of the list
        contador_2 = 0
    # Print the pair: giver -> recipient
    print(amigos[contador_1] + ' -> ' + amigos[contador_2])
