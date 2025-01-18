"""
This script is designed to scrape images from the internet based on a search query and save them to a specified directory. 
It uses the `requests` library to fetch web pages and images, the `BeautifulSoup` library for parsing HTML, 
and `os` to manage file directories. The script allows users to specify the number of images to download and 
automates the process of extracting image URLs from a given webpage.

Functions:
1. `download_image`: Downloads an image from a given URL and saves it to a specified path.
2. `scrape_images`: Searches for images using a query, extracts the image URLs, and downloads them into a designated folder.

Libraries Used:
- `os`: For file and directory management.
- `requests`: For making HTTP requests to fetch webpages and images.
- `BeautifulSoup` (from `bs4`): For parsing HTML content.
- `time`: For adding delays between downloads (optional).
"""

import os
import requests
from bs4 import BeautifulSoup
import time

# Function to download a single image
def download_image(url, save_path):
    """
    Downloads an image from a given URL and saves it to the specified path.

    Args:
        url (str): The URL of the image to download.
        save_path (str): The file path where the image will be saved.
    """
    response = requests.get(url, stream=True)  # Fetch the image in chunks
    if response.status_code == 200:  # Check if the request was successful
        with open(save_path, 'wb') as file:  # Open the file in write-binary mode
            for chunk in response.iter_content(1024):  # Write chunks of data to the file
                file.write(chunk)

# Function to scrape images based on a query
def scrape_images(query, num_images, save_directory):
    """
    Searches for images based on a query and saves them to a specified directory.

    Args:
        query (str): The search query for finding images.
        num_images (int): The number of images to download.
        save_directory (str): The directory where images will be saved.
    """
    # Create the directory if it doesn't already exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Format the query for use in a URL
    query = query.replace(' ', '+')

    # Construct the search URL
    search_url = f'https://www.shopify.com.br/burst/{query}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <img> tags on the search results page
    image_tags = soup.find_all('img')

    count = 0  # Counter for downloaded images
    for image_tag in image_tags:
        if count >= num_images:  # Stop if the desired number of images is downloaded
            break

        # Extract the image URL from the <img> tag
        image_url = image_tag['src']

        # Verify the image URL is valid
        if image_url.startswith('http'):
            # Set the full path for saving the image
            save_path = os.path.join(save_directory, f'image{count + 1}.jpg')

            # Download the image
            download_image(image_url, save_path)

            count += 1  # Increment the counter

        # Pause briefly before the next download (optional)
        time.sleep(0.1)

    print(f'{count} images downloaded and saved in {save_directory}.')

# Example usage
num_images_to_download = 100  # Number of images to download
save_directory = 'computador'  # Directory to save images

scrape_images(save_directory, num_images_to_download, save_directory)
