import os
import requests
from bs4 import BeautifulSoup
import time

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

def scrape_images(query, num_images, save_directory):
    # Cria o diretório para salvar as imagens, se não existir
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Formata a query para usar em uma URL de pesquisa
    query = query.replace(' ', '+')

    # Faz a pesquisa no mecanismo de busca de sua escolha (por exemplo, Google)
    #search_url = f'https://www.google.com/search?q={query}&source=lnms&tbm=isch'
    #search_url = f'https://www.google.com/search?q={query}&source=lnms&tbm=isch&tbs=isz:l'
    search_url=f'https://www.shopify.com.br/burst/imagens-hd/pesquisar?q=praia&button='
    search_url=f'https://www.shopify.com.br/burst/{query}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todas as tags <img> nas páginas de resultados da pesquisa
    image_tags = soup.find_all('img')

    count = 0
    for image_tag in image_tags:
        if count >= num_images:
            break

        # Extrai a URL da imagem
        image_url = image_tag['src']

        # Verifica se a URL da imagem é válida
        if image_url.startswith('http'):
            # Define o caminho completo para salvar a imagem
            save_path = os.path.join(save_directory, f'image{count+1}.jpg')

            # Faz o download da imagem
            download_image(image_url, save_path)

            count += 1

        # Aguarda um breve período antes de fazer o próximo download (opcional)
        time.sleep(0.1)

    print(f'{count} imagens baixadas e salvas em {save_directory}.')


# Exemplo de uso
num_images_to_download = 100
save_directory = 'computador'

scrape_images(save_directory, num_images_to_download, save_directory)
