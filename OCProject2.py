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