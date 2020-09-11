from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {"executable_path": ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    # set url for browser
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Loop to get news_title and news_p
    for x in range(1):
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # Retrieve all elements that contain book information
        articles = soup.find_all('div', class_='list_text')

        # Iterate through each book
        for article in articles:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            news_title  = article.find('div', class_="content_title").text
            news_p = article.find('div', class_='article_teaser_body').text
           

        # Click the 'More' button on each page
        try:
            browser.click_link_by_partial_text('More')
            
        except:
            print("Scraping Complete")

    # Store data in a dictionary
    mars_data = {
        "min_temp": news_title,
        "max_temp": news_p
    } 

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data    
    
