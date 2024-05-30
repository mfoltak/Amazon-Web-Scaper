import requests
from bs4 import BeautifulSoup
import webbrowser

def get_amazon_products(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 
        'Accept-Language': 'en-US,en;q=0.5'
    }
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    products = []
    
    for item in soup.find_all("div", attrs={'data-component-type': 's-search-result'}):
        name = item.h2.text
        link = item.h2.a['href']
        try:
            price = float(item.find("span", "a-offscreen").text.replace("€", "").replace(",", "."))
        except AttributeError:
            continue
        try:
            stars = float(item.find("span", "a-icon-alt").text.split()[0].replace(",", "."))
        except AttributeError:
            continue
        products.append({
            'name': name,
            'link': "https://amazon.de" + link,
            'price': price,
            'stars': stars,
            'ratio': price / stars if stars != 0 else float('inf')
        })
    
    return products

def find_best_product(products):
    return min(products, key=lambda x: x['ratio'])

def main():
    url = input("Enter the Amazon URL: ")
    products = get_amazon_products(url)
    
    if not products:
        print("No products found.")
        return
    
    best_product = find_best_product(products)
    print(f"Best Product: {best_product['name']}")
    print(f"Price: €{best_product['price']}")
    print(f"Stars: {best_product['stars']}")
    print(f"Link: {best_product['link']}")
    
    # Open the product page in the web browser
    webbrowser.open(best_product['link'])

if __name__ == "__main__":
    main()
