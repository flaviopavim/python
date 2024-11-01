def calcular_ponto_c(Xa, Ya, Xb, Yb, Xc=None, Yc=None):
    # Verifica se Xc ou Yc são fornecidos, se não, assume como None
    if Xc is None and Yc is None:
        raise ValueError("É necessário fornecer pelo menos um valor para Xc ou Yc.")
    
    # Se Xc for fornecido, calcula Yc usando a equação da reta
    if Xc is not None:
        Yc = ((Xc - Xa) * (Yb - Ya) / (Xb - Xa)) + Ya
    
    # Se Yc for fornecido, calcula Xc usando a equação da reta
    elif Yc is not None:
        Xc = ((Yc - Ya) * (Xb - Xa) / (Yb - Ya)) + Xa
    
    return Xc, Yc

# Exemplo de uso:
Xa, Ya = 1, 2
Xb, Yb = 4, 5

# Calcula as coordenadas de C com base em Xc
Xc, Yc = calcular_ponto_c(Xa, Ya, Xb, Yb, Xc=3)
print(f"Coordenadas de C: ({Xc}, {Yc})")

# Calcula as coordenadas de C com base em Yc
Xc, Yc = calcular_ponto_c(Xa, Ya, Xb, Yb, Yc=4)
print(f"Coordenadas de C: ({Xc}, {Yc})")
