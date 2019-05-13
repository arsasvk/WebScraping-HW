

# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import re



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)





def scrape_mars():
	browser = init_browser()

	# Visit mars.nasa.gov/news
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	html = browser.html


	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(html, 'html.parser')

	# Examine the results, then determine element that contains sought info
	#print(soup.prettify())

	# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.

	news_title = soup.find('div', class_='content_title').text
	news_p = soup.find('div', class_='article_teaser_body').text

	#print("News Title:"+ news_title)
	#print("Paragraph:"+ news_p)

#-----------------------------------------------------------------------------------------------------
	
	# Visit the url for JPL Featured Space Image
	featured_image_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(featured_image_url)
	image_html = browser.html

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(image_html, 'html.parser')

	# Navigate the site and find the image url for the current Featured Mars Image 
	image_article = soup.find_all('a', class_ = 'button fancybox')
	image_url = image_article[0]['data-fancybox-href']
	home_url = 'https://www.jpl.nasa.gov'  
	featured_image_url = home_url + image_url

	#print('Featured Image URL: '+ featured_image_url)
#------------------------------------------------------------------------------------------------------
	
	# Visit the Mars Weather twitter account
	twitter_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(twitter_url)
	twitter_html = browser.html

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(twitter_html, 'html.parser')

	# Scrape the latest Mars weather tweet from the page
	mars_weather = soup.find('div',class_="js-tweet-text-container").text
	mars_weather = re.sub(r"pic.twitter.com\S+","", mars_weather)
	#print("Current weather on Mars is: "+mars_weather)

#-------------------------------------------------------------------------------------------------------
	# Visit the Mars Facts webpage
	space_facts_url = 'https://space-facts.com/mars/'

	# Use Pandas to scrape the table containing facts about the planet 
	mars_facts = pd.read_html(space_facts_url)
	#mars_facts
	mars_df = mars_facts[0]
	mars_df.columns = ['Mars Facts', 'Details']

	#mars_df.head()
#-------------------------------------------------------------------------------------------------------
	# Visit the USGS Astrogeology site 
	astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(astrogeology_url)
	astrogeology_html = browser.html

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(astrogeology_html, 'html.parser')

	description = soup.find_all('div', class_ = 'description')

	# Obtain high resolution images for each of Mar's hemispheres.
	hem_title= []

	for title in description:
	    main_url = 'https://astrogeology.usgs.gov' + title.find('a')['href']
	    browser.visit(main_url)
	    title_html = browser.html
	    soup1 = bs(title_html, 'html.parser')
	    images = 'https://astrogeology.usgs.gov' + soup1.find_all('img', class_='wide-image')[0]['src']
	    imgDict = {}
	    imgDict['title'] = title.find('h3').text.strip()
	    imgDict['img_url'] = images
	    hem_title.append(imgDict)

	browser.quit()

#---------------------------------------------------------------------------------------------------------
 # Store data in a dictionary
	result = {}

	result['NewsTitle'] = news_title
	result['Paragraph'] = news_p
	result['Weather'] = mars_weather
	result['MarsFacts'] = mars_df.to_html()
	result['FeaturedImage'] = featured_image_url
	result['Hemispheres'] = hem_title

	return result

