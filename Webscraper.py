# Import necessary libraries
from bs4 import BeautifulSoup as bs
import requests
import pandas
import httplib2

# Define the URL of the Flipkart page you want to scrape
url = "https://www.flipkart.com/television-store?otracker=nmenu_sub_TVs%20and%20Appliances_0_Televisions&otracker=nmenu_sub_TVs%20%26%20Appliances_0_Television"

# Define CSS classes for various elements you want to extract from the page
ticlass = "_4rR01T"
raclass = "_3LWZlK"
prclass = "_30jeq3 _1_WHN1"
reclass = "_2_R_DZ"

# Create an HTTP object to make a request to the URL
http = httplib2.Http()
response, content = http.request(url)

# Create an empty list to store extracted URLs
urls = []

# Parse the HTML content using BeautifulSoup and find all links (anchor tags with 'href' attribute)
for link in bs(content).find_all('a', href=True):
    # Append the complete URL to the list of URLs
    urls.append("https://www.flipkart.com" + link['href'])

# Create empty lists to store product information
title = []
rating = []
review = []
price = []

# Loop through a subset of the URLs (from 70 to 109)
for link in urls[70:110]:
    print(link)
    url = link
    r = requests.get(url)

    # Parse the HTML content of the product page
    soup = bs(r.content, 'html.parser')

    # Find all elements with specified CSS classes for title, rating, price, and review
    ti = soup.findAll('div', class_=ticlass)
    ra = soup.findAll('div', class_=raclass)
    pr = soup.findAll('div', class_=prclass)
    rev = soup.findAll('span', class_=reclass)

    # Iterate through the lists of elements and append the text to respective lists
    for t, r, p, re in zip(ti, ra, pr, rev):
        title.append(t.text)
        rating.append(r.text)
        price.append(p.text)
        review.append(re.text)

# Display a menu for user interaction
print("1. Select Products\n2. Exit\n")

# Create empty lists to store filtered product information
while True:
    t = []
    r = []
    p = []
    rat = []
    
    # Prompt the user for input
    n = int(input())
    
    if n == 1:
        z = str(input("Enter item name:"))
        
        # Iterate through the product titles and filter based on user input
        for j in range(len(title)):
            if z in title[j].lower():
                t.append(title[j].lower())
                r.append(rating[j])
                p.append(price[j])
                rat.append(review[j])
        
        # Create a DataFrame from the filtered data and save it to a CSV file
        datae = {'title': t, 'rating': r, 'price': p, 'review': rat}
        pys = pandas.DataFrame(data=datae)
        pys.to_csv(input('Enter file name: ') + '.csv')

    elif n == 2:
        exit()
    else:
        print('Enter a valid option')
