from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def get_news_articles():
    # Scrape the website
    response = requests.get('https://elfilahanews.dz', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Use soup to find and extract the desired data
    news_articles = []
    # find all the block-post-overlay
    news_blocks = soup.find_all('div', class_='block-post-overlay')
    # save a tags in a list
    news_links = [block.find('a') for block in news_blocks]
    # iterate over the list of a tags
    for link in news_links:
        # save the link in a dictionary
        article = {
            'title': link.get('aria-label'),
            'url': link.get('href')
        }
        news_articles.append(article)
    return news_articles

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Use soup to find and extract the desired data
    # e.g., news_articles = soup.find_all('div', class_='news-article')
    # get the news articles
    news_articles = get_news_articles()
    # add dictionary to the list
    extracted_data = []
    for article in news_articles:
        # get the title and url of the article
        title = article['title']
        url = article['url']
        # append the dictionary to the list
        extracted_data.append({
            'title': title,
            'url': url
        })
        
    return extracted_data

# Call the scrape_website function with the desired URLs

news = Blueprint('news', __name__, template_folder='dist', static_folder='static')

@news.route('/')
def home():
    news_data = scrape_website('https://elfilahanews.dz')
    return render_template('index.html',news=news_data)

def get_news():
    return scrape_website('https://elfilahanews.dz')