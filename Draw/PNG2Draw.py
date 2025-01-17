from PIL import Image
from collections import Counter
import json

# Função para obter as cores da imagem e as coordenadas
def get_image_data(image_path):
    # Abrir a imagem
    img = Image.open(image_path)
    
    # Converte a imagem para o formato RGB
    img = img.convert('RGB')
    
    # Obter as dimensões da imagem
    width, height = img.size
    
    # Garantir que a imagem seja 32x32
    if width != 32 or height != 32:
        raise ValueError("A imagem precisa ser 32x32 pixels.")
    
    # Armazenar as cores
    color_list = []
    
    for y in range(height):
        for x in range(width):
            # Pega a cor no formato RGB
            color = img.getpixel((x, y))
            hex_color = f'{color[0]:02x}{color[1]:02x}{color[2]:02x}'  # Converte para hexadecimal
            
            # Armazena a cor
            color_list.append(hex_color)
    
    # Conta a frequência das cores
    color_count = Counter(color_list)
    
    # Ordena as cores por frequência (do mais predominante ao menos)
    sorted_colors = [color for color, _ in color_count.most_common()]
    
    # Remover cores duplicadas
    unique_colors = sorted_colors  # Já são únicas após a contagem
    
    # Criar o dicionário para armazenar os arrays
    result = {
        "colors": {idx: color for idx, color in enumerate(unique_colors)},
        "coordinates": []
    }
    
    # Preencher as coordenadas com os color_ids
    for y in range(height):
        row = []  # Nova linha para armazenar as coordenadas por `x`
        for x in range(width):
            color = img.getpixel((x, y))
            hex_color = f'{color[0]:02x}{color[1]:02x}{color[2]:02x}'
            color_id = unique_colors.index(hex_color)
            row.append(color_id)  # Atribui o color_id a posição x na linha
        result["coordinates"].append(row)  # Adiciona a linha de coordenadas ao final
    
    return result

# Função para salvar os dados em um arquivo .draw (JSON)
def save_as_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

# Caminho do arquivo de imagem
image_path = 'image.png'  # Substitua pelo caminho da sua imagem

# Obter os dados da imagem
image_data = get_image_data(image_path)

# Salvar como .draw (arquivo JSON)
output_path = 'picture.draw'
save_as_json(image_data, output_path)

print(f'Dados salvos em {output_path}')
