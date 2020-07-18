#!/usr/bin/env python
# coding: utf-8


#Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as SOUP

# Add Pandas to use .read_html() function
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# Visist the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html= browser.html
news_soup= SOUP(html, 'html.parser')
slide_elem= news_soup.select_one('ul.item_list li.slide')


slide_elem.find("div", class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# Set up URL call
url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click on it
browser.is_element_present_by_text('more info', wait_time = 1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# Parse the resulting html with soup
html= browser.html
img_soup = SOUP(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# find table on website and convert to DF using pd.read_html then pd.to_html()
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description','value']
df.set_index('description', inplace=True)
df.to_html()
                                             

# End the browser
browser.quit()




