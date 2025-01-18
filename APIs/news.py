"""
This script retrieves news articles related to a specific search term using the NewsAPI. 
It fetches the data in JSON format and extracts the title and URL of each article. 
The script is designed to display the titles of the articles and can optionally print the links for further exploration.

Requirements:
- An active API key from NewsAPI.
- The `requests` library for making HTTP requests.

Functionality:
1. Builds a search query URL using the search term and API key.
2. Sends a GET request to the NewsAPI to fetch articles.
3. Parses the JSON response to extract article titles and URLs.
4. Displays the titles of the articles in the console.
"""

import requests

# Define the search term for news articles
search_term = 'novidades tecnologia'  # Search query for news related to technology updates

# Build the API URL with the search term and API key
url = f"https://newsapi.org/v2/everything?q={search_term}&apiKey=12424ff576ad48689135366445704f71"

# Send a GET request to the NewsAPI endpoint
response = requests.get(url)

# Parse the JSON response to extract the list of articles
news_articles = response.json()['articles']

# Iterate over the articles and extract their titles and URLs
for article in news_articles:
    title = article['title']  # Extract the article title
    link = article['url']    # Extract the article URL

    # Print the article title
    print(title)

    # Uncomment the line below to also print the article link
    # print(link)
