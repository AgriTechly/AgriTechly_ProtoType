from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from scripts.news import get_news


news = get_news()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def get_abstract(url_abs,url_full):
    response = requests.get(url_abs, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Use soup to find and extract the desired data
    # but first find this section with this class kc-elm kc-css-243536 kc_row
    if soup.find('strong', text='Abstract:') is None:
        # get the first paragraph of the full article
        response = requests.get(url_full, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # find div with class entry-content articlebody
        entry_content = soup.find('div', class_='entry-content articlebody')
        # get the first paragraph
        abstract = entry_content.find('p')
        return abstract.text
    abstract = soup.find('strong', text='Abstract:').find_next('p')
    return abstract.text

def get_latest_articles():
    latest_articles = []
    # Scrape the website
    response = requests.get('https://www.agriculturejournal.org/current-issue/', headers=headers)
    html = response.content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Use soup to find and extract the desired data
    # find all the block-post-overlay
    latest_blocks = soup.find_all('article')
    # get the id of the block
    for block in latest_blocks:
        block_id = block.get('id')
        # delete this part in the block_id post-
        block_id = block_id.replace('post-', '')
        # select the div with the class entry-content
        entry_content = block.find('div', class_='entry-content')
        # get the title of the article
        ele_link = entry_content.find('h2')
        # get the link of the article and the title
        link = ele_link.find('a')
        url = link.get('href')
        title = link.find('strong').text
        # get the authors of the article from the span in the entry-content inside the strong select all texts
        authors = entry_content.find('span').text
        # get the abstract of the article
        abstract = get_abstract('https://www.agriculturejournal.org/abstract/?var='+block_id, url)
        # append the dictionary to the list
        latest_articles.append({
            'title': title,
            'url': url,
            'authors': authors,
            'abstract': abstract
        })
    return latest_articles

# Get the latest articles when the server starts
latest_articles = get_latest_articles()
# Sechedule the function to run once the server starts and then every 24 hours
scheduler = BackgroundScheduler()
scheduler.add_job(get_latest_articles, 'interval', hours=24)
scheduler.start()

articles = Blueprint('articles', __name__, template_folder='dist', static_folder='static')

@articles.route('/blog')
def index():
    #research_data = scrape_website('https://example.com/research')
    return render_template('blog.html', news=news, research=latest_articles)
