from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# executable_path = {"executable_path": ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

###############################################################
# Scraping Script
############################################################### 

def scrape():

    browser = init_browser()

    ###############################################################
    # Mars News Article
    ############################################################### 
    # set url for browser
    news_domain = 'https://mars.nasa.gov'
    url = news_domain + '/news'
    browser.visit(url)

    # Get news_title and news_p
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')     

    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    news_title  = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_='article_teaser_body').text
    img_header =soup.find('div', class_='list_image')
    img = img_header.find('img')['src']
    news_image = 'https://mars.nasa.gov' + img
    print("Mars News Scraping Complete")

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "news_image": news_image,
        "news_domain" : url
    } 

    
    ###############################################################
    # Featured Image
    ############################################################### 
    
    # set url for browser
    Featured_domain = 'https://www.jpl.nasa.gov'
    space_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_url)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain image link
    images = soup.find_all('article')

    for img in images:
        data_link = img.find('a')['data-link']
        
        # Open data link to get full size image
        data_link_url = Featured_domain + data_link
    
        try:
            browser.visit(data_link_url)
            html = browser.html

            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Make sure to find the image url to the full size .jpg image.        
            iamge_articles = soup.find_all('article')
            
            for iamge_article in iamge_articles:
                figure = iamge_article.find('figure')
                figure_url = figure.find('a')['href']
                
                # Make sure to save a complete url string for this image.
                featured_image_url  = Featured_domain + figure_url
                mars_data["featured_image_url"] =  featured_image_url  
                mars_data["Featured_domain"]  = Featured_domain
                print("Featured Image Complete")  
            
        except:
            print("Featured Image Scraping Error")  

    ###############################################################
    # Mars  Facts
    ############################################################### 

    # Visit the Mars Facts webpage here 
    mars_url = 'https://space-facts.com/mars/'

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    import pandas as pd

    # Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(mars_url)

    df = tables[0]
    df.columns = ['Topic', 'Value']

    # render dataframe as html
    html = df.to_html(table_id="table")
    mars_data["html"] =  html 

    # render dataframe as dictionary
    table = df.values.tolist()
    mars_data["table"] =  table    
    print("Mars Facts Complete")


    ###############################################################
    # Mars  Hemispheres
    ############################################################### 

    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    usgs_site = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    usgs_domain = 'https://astrogeology.usgs.gov'
    browser.visit(usgs_site)

    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain image section
    image_section = soup.find_all('div', class_='item')


    # Create lists to hold each title and image
    titles = []
    images = []

    # loop to append title and images to lists
    for image in image_section:
        figure_url = image.find('a')['href']
        image_url = usgs_domain + figure_url
        title = image.find('h3').text
        
        titles.append(title)
        
        try:
            browser.visit(image_url)
            html = browser.html

            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')

            # Retrieve all elements that contain image section
            thumnb_url = soup.find_all('div', class_='downloads')

            for thumb in thumnb_url:
                image_list = thumb.find('li')
                image_full_url = image_list.find('a')['href']
                images.append(image_full_url)

        except:
            print('Did not work')
 
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys img_url and title.
    image_urls = {}
    image_urls = dict(zip(titles, images))

    # Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.
    hemisphere_image_urls = [] 
    for key, value in image_urls.items(): 
        hemisphere_image_urls.append({'title' : key, 'img_url' : value}) 

    # Append to mars data 
    mars_data["hemisphere_image_urls"] =  hemisphere_image_urls   
    print("Hemisphere Complete")

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data  