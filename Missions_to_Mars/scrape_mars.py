# Import Splinter, BeautifulSoup, and Pandas
import time
import pandas as pd
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    
    #browser = Browser("chrome", executable_path="chromedriver", headless=True)

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

   
    

    # ------------------- Scrape Mars News
    browser.visit('https://redplanetscience.com')
    time.sleep(2)

    # Create BeautifulSoup Object and parse with HTML

    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = news_soup.find("div", class_='content_title').get_text()
    news_title

    # Use the parent element to find the paragraph text
    news_p = news_soup.find('div', class_="article_teaser_body").get_text()
    news_p

    
    # -------------------  Scrape JPL Images

    #Visit URL
    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)
    time.sleep(2)

    # Find and click the full image button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = bs(html, 'html.parser')

    relative_image_path = img_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = image_url + relative_image_path
    featured_image_url


    # ------------------- Scrape Mars facts
   

    df_facts = pd.read_html('https://galaxyfacts-mars.com',header=0)[0]
    df_facts.set_index('Mars - Earth Comparison', inplace=True)
    facts_html = df_facts.to_html()
    facts_html = facts_html.replace('right','center')
    facts_html = facts_html.replace('dataframe','table table-striped')


    # -------------------  Scrape Hemisphere Data

   
        
    results = hems_soup.find_all('h3')[0:-1]

    hemisphere_image_urls = []

    for result in results:
        titles = result.text
        browser.links.find_by_partial_text(titles).click()
        html_en = browser.html
        soup_en = bs(html_en, 'html.parser')
        title = soup_en.find('h2', class_='title').text.replace("Enhanced","").strip()
        sample = soup_en.find('li')
        imgurl = sample.find('a')['href']
        imgurl = url + imgurl
        hemisphere_dict = {"title" : title, "img_url" : imgurl}
        hemisphere_image_urls.append(hemisphere_dict)
        browser.links.find_by_partial_text('Back').click()

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": facts_html,
        "hemispheres": hemisphere_image_urls
    
    }


    # Stop webdriver and return data
    browser.quit()
    return data


