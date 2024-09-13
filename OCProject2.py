import os
import csv
import requests
from bs4 import BeautifulSoup
#Welcome Code
print("Welcome to BookScraper5000")
# Function to extract book details from a single book page
def extract_book_data(book_url):
    book_page = requests.get(book_url)
    book_soup = BeautifulSoup(book_page.content, 'html.parser')

    product_page_url = book_url
    upc = book_soup.find('th', string="UPC").find_next_sibling('td').text
    title = book_soup.find('h1').text
    price_including_tax = book_soup.find('th', string="Price (incl. tax)").find_next_sibling('td').text
    price_excluding_tax = book_soup.find('th', string="Price (excl. tax)").find_next_sibling('td').text
    quantity_available = book_soup.find('th', string="Availability").find_next_sibling('td').text.strip()
    description = book_soup.find('meta', {'name': 'description'})['content'].strip() if book_soup.find('meta', {'name': 'description'}) else "No description available."
    category = book_soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    rating = book_soup.find('p', class_='star-rating')['class'][1]
    image_url = "https://books.toscrape.com" + book_soup.find('img')['src'].replace('../..', '')

    return {
        "product_page_url": product_page_url,
        "universal_product_code(UPC)": upc,
        "book_title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "quantity_available": quantity_available,
        "product_description": description,
        "category": category,
        "review_rating": rating,
        "image_url": image_url
    }

# Function to download the book's image
def download_image(image_url, title):
    response = requests.get(image_url)
    if response.status_code == 200:
        title = title.replace(':', '')  # delete ':', not valid in file name
        title = title.replace('*', '')  # delete ':', not valid in file name
        title = title.replace("'", '')  # delete ':', not valid in file name
        title = title.replace("?", '')  # delete ':', not valid in file name


        with open(f"images/{title.replace('/', '_')}.jpg", 'wb') as file:
            file.write(response.content)

# Function to scrape a single category and handle pagination
def scrape_category(category_url, category_name):
    page_number = 1
    category_data = []
    #while True:
    if True:
           #TEMPpage_url = f"{category_url}page-{page_number}.html"
        page_url = f"{category_url}"
        page = requests.get(page_url)
        print("50",page_url)
        if page.status_code != 200:
            #break  # No more pages
            return
        soup = BeautifulSoup(page.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        for n, book in enumerate(books):
            book_link = book.find('h3').find('a')['href']
            book_url = "https://books.toscrape.com/catalogue/" + book_link.replace('../../../', '')
            book_data = extract_book_data(book_url)
            category_data.append(book_data)
            #print("60",len(category_data))
            download_image(book_data['image_url'], book_data['book_title'])
            print('.', end='')
        print()
        page_number += 1
        print('  68: # of books:', n+1)