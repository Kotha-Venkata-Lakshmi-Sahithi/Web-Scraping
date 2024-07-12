import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    
    # Find product containers (adjust these selectors based on the website's structure)
    product_containers = soup.find_all('div', class_='product-container')
    
    for container in product_containers:
        name = container.find('h2', class_='product-name').text.strip()
        price = container.find('span', class_='product-price').text.strip()
        rating = container.find('div', class_='product-rating').text.strip()
        
        products.append({
            'name': name,
            'price': price,
            'rating': rating
        })
    
    return products

def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'price', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def main():
    base_url = 'https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2'
    num_pages = 5  # Number of pages to scrape
    
    all_products = []
    
    for page in range(1, num_pages + 1):
        url = f'{base_url}?page={page}'
        print(f'Scraping page {page}...')
        
        products = scrape_product_info(url)
        all_products.extend(products)
        
        # Be respectful to the website by adding a delay between requests
        time.sleep(2)
    
    save_to_csv(all_products, 'product_data.csv')
    print(f'Scraped {len(all_products)} products and saved to product_data.csv')

if __name__ == '__main__':
    main()