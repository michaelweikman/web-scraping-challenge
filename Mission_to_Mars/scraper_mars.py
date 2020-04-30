from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import re
import time

executable_path = {'executable_path': 'chromedriver'}

def quit_browser():
    Browser('chrome', **executable_path, headless=False).quit()

def get_url_soup(url):
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    return soup

#Nasa Article Scraper
def article_scraper():
    nasa_url = "https://mars.nasa.gov/news"
    soup = get_url_soup(nasa_url)

    first_article = soup.find_all('div',class_='content_title')[1]
    news_title = first_article.find('a').text
    news_paragraph = first_article.parent.find('div',class_='article_teaser_body').text
    return {"title": news_title, "paragraph": news_paragraph}

def mars_feature_img_scraper():
    #Mars JPL image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    soup = get_url_soup(jpl_url)

    featured_url = soup.find('article')['style'].split("('", 1)[1].split("')")[0]
    img_url = f'https://www.jpl.nasa.gov{featured_url}'
    return {"url": img_url}


def tweet_weather_scraper():
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    soup = get_url_soup(twitter_url)

    tweet = soup.find(string=re.compile("^InSight"))
    return {"weather": tweet}

#Mars Facts
def mars_facts_scraper():
    facts_url = 'https://space-facts.com/mars/'

    df = pd.read_html(facts_url)[0]
    df.set_index(0, inplace=True)
    df.index.name = ''
    df.rename(columns={1:'values'}, inplace=True)
    return {"facts": df.to_html()}

#Mars Hemisphere
def mars_hemisphre_scraper():
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    soup = get_url_soup(hemi_url)

    item_divs = soup.find_all('div', class_='item')
    img_data = []

    for div in item_divs:
        title = div.find('h3').text
        path = div.find('a')['href']
        
        target_url = f'https://astrogeology.usgs.gov{path}'
        soup = get_url_soup(target_url)
        img_url = soup.find('div', class_='downloads').find('a')['href']
        img_data.append({"title": title, "url": img_url})
    
    return {"hemisphere_data":img_data}

def scrape():
    data = {}
    data.update(article_scraper())
    data.update(mars_feature_img_scraper())
    data.update(tweet_weather_scraper())
    data.update(mars_facts_scraper())
    data.update(mars_hemisphre_scraper())

    quit_browser()
    return data