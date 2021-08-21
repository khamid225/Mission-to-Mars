from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


# "mongodb+srv://cluster0.9b2o3.mongodb.net/myFirstDatabase" --username user1

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = { "news_title": news_title, "news_paragraph": news_paragraph,
             "featured_image": featured_image(browser),
             "facts": mars_facts(),
             "hemispheres": hemisphere_img(browser),
             "last_modified": dt.datetime.now(),
           }
    browser.quit()
    return data

def mars_news(browser):
    """
    Scrape Mars News
    Visit the mars nasa news site
    """
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_="fancybox-image").get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    htmldf = df.to_html()
    htmldf = htmldf.replace('class="dataframe"', 'class="dataframe table-striped"')
    return htmldf

def hemisphere_img(browser):
    # Visit the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # Code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with soup
    html = browser.html
    main_page_soup = soup(html, 'html.parser')
    hemisphere_links = browser.find_by_css("div.description a.itemLink.product-item")
    #l = hemisphere_links[0]
    links_to_visit = [l._element.get_attribute("href") for l in hemisphere_links]
    # For each link, visit the page and gather the image link and title
    for l in links_to_visit:
        browser.visit(l)
        jpeg_link = browser.find_by_css("ul").first.find_by_css("a").first._element.get_attribute("href")
        title = browser.find_by_css(".title").first.text
        hemisphere_image_urls.append({
            'img_url': jpeg_link,
            'title': title})
        browser.back()
    # Return the list that holds the dictionary of each image url and title
    return hemisphere_image_urls


if __name__ == "__main__":
    # When as script, print scraped data
    print(scrape_all())
