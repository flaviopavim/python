#sorteio de amigo secreto

import random

amigos=[
    'flavio',
    'leo',
    'patrick',
    'jabá',
    'kicko',
    'cego',
    'nightmare',
    'hasan'
]

random.shuffle(amigos)

for contador_1 in range(len(amigos)):
    contador_2=contador_1+1
    if (contador_2==len(amigos)):
        contador_2=0
    print(amigos[contador_1]+' -> '+amigos[contador_2])
