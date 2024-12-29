

# função pra comparar os hash
def compare(hashs_string):
    
    # Separa os pares de hash
    hashs = hashs_string.split(";")
    
    # Itera sobre os pares
    for item in hashs:
        
        # Separa os hashes
        pair = item.split(",")
        
        # Compara os hashes
        if pair[0] == pair[1]:
            print("Correto")
        else:
            print("Incorreto")
    
# Testa a função
compare("abc123,abc123;def456,def457")