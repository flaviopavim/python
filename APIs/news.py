import requests

search_term = 'novidades tecnologia'
url = f"https://newsapi.org/v2/everything?q={search_term}&apiKey=12424ff576ad48689135366445704f71"
response = requests.get(url)
news_articles = response.json()['articles']

for article in news_articles:
    title = article['title']
    link = article['url']
    #print('')
    print(title)
    #print(link)
