from bs4 import BeautifulSoup
import requests
 
def scrape_stock_data(symbol, exchange):
    if exchange == 'NASDAQ':
        url = f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange == 'NSE':
        url = f"https://finance.yahoo.com/quote/{symbol}.NS"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    current_price = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})['data-value']
    previous_close = soup.find("fin-streamer", {"data-field": "regularMarketPreviousClose"})['data-value']
  
    print('Current Price:', current_price)
    print('Previous Close:', previous_close)
 
scrape_stock_data('GOOG', 'NASDAQ') 
    
    
    
    
