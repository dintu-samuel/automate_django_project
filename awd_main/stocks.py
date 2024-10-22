from bs4 import BeautifulSoup
import requests





def scrape_stock_data(symbol, exchange):
    
    if exchange =='NASDAQ':
         url = f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange =='NSE':
        symbol = symbol + '.NS'
        url = f"https://finance.yahoo.com/quote/{symbol}.NS?p={symbol}.NS&.tsrc=fin-srch"
        
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    current_price = soup.find("fin-streamer", {"data-symbol": symbol})['data-value']
    previous_close = soup.find('span',{"active data-field": 'regularMarketPreviousClose'}).text
    print('previous_close ==>', previous_close)
   
    
  
    
scrape_stock_data('GOOG', 'NSE')    
    
    
    
    
