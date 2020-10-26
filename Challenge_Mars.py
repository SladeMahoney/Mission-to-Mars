
#Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as SOUP
# Add Pandas to use .read_html() function
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

def scrape_all():
    #Initiate headless driver for deloyment
    browser = Browser("chrome", executable_path= "chromedriver", headless = True)
    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser), 
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # End the browser and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visist the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    #Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html
    html= browser.html
    news_soup= SOUP(html, 'html.parser')
    
    #Add try/except for error handling
    try: 
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        #Use the parent element to find the first 'a' tag and save it
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):    
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

    #Add try/except for error handling
    try: 

        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        # find table on website and convert to DF using pd.read_html then pd.to_html()
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None
    
    #Assign columns and set index of dataframe 
    df.columns = ['description','value']
    df.set_index('description', inplace=True)
    
    #Convert dataFrame into HTML format, add bootstrap
    return df.to_html(classes = "table table-striped")

def mars_hemispheres(browser):
    #https://stackoverflow.com/questions/46933679/scraping-text-in-h3-and-div-tags-using-beautifulsoup-python
    #https://www.dataquest.io/blog/web-scraping-beautifulsoup/
    #scrape images from website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)      
    
   
    hemisphere_images = []
        
    #loop through the images 4-8 not 1-4 -- found that those are not the correct images we are looking for 
    for item in range(4,8):
       
       image_thumbnail = browser.find_by_tag('img')
       image_thumbnail[item].click()

        #HTML object and parse through the website with SOUP
        html= browser.html
        hemis_soup = SOUP(html, 'html.parser')

        # Get all the items from the mars hemisphere
        hemis_items = hemis_soup.find('a', text = 'Sampple').get('href')
        hemis_title = hemis_soup.find('h2', 'title').text 

        #store link that takes you to full website image
        hemisphere_images.apped({"title": hemis_title, "url": hemis_items})
        browser.visit(url + )
        #must return to page to iterate again
        browser.back()
    return hemisphere_images

if __name__== "__main__":
    # If running as script, print scraped data
    print(scrape_all())

#Quit browser at the end
    browser.quit
