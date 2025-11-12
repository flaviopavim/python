from PIL import Image
import os

input_dir = "pasta_com_imagens/"
output_dir = "pasta_com_imagens_redimensionadas/"
background_color = (0, 0, 0)  # cor de fundo preta

sizes=[
    [320,240],
    [240,320]
]

for size in sizes:
    width = size[0]
    height = size[1]

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            with Image.open(os.path.join(input_dir, filename)) as img:
                nova_imagem = Image.new('RGB', (width, height), background_color)
                imagem_original = Image.open(os.path.join(input_dir, filename))
                imagem_original.thumbnail((width, height))
                x = (width - imagem_original.size[0]) // 2
                y = (height - imagem_original.size[1]) // 2
                nova_imagem.paste(imagem_original, (x, y))
                pre = str(width) + 'x' + str(height) + ' - '
                nova_imagem.save(os.path.join(output_dir, pre + filename))

print('Finalizado')
