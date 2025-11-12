from PIL import Image
import os

input_dir = "pasta_com_imagens/"
output_dir = "pasta_com_imagens_redimensionadas/"

sizes=[
    [320,240],
    [240,320]
]

for size in sizes:

    width=size[0]
    height=size[1]

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            with Image.open(os.path.join(input_dir, filename)) as img:
                nova_imagem = Image.new('RGB', (width, height), (255, 255, 255))
                imagem_original = Image.open(input_dir+filename)
                imagem_original.thumbnail((width, height))
                nova_imagem.paste(imagem_original, ((width-imagem_original.size[0])//2, (height-imagem_original.size[1])//2))
                pre=str(width)+'x'+str(height)+' - '
                nova_imagem.save(output_dir+pre+filename)


print('Finalizado')
