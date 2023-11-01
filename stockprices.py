import requests
from bs4 import BeautifulSoup
import json
#url is case sensitive remember this for later

MyStocks = ["VZ", "IBRX", "SNAP", "GOOGL", "MSFT", "AAPL", "AMZN", "NVDA", "META", "TSLA"]
StockData = []
def getData(symbol):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    url = f'https://finance.yahoo.com/quote/{symbol}'
    response = requests.get(url, headers = header)
    soup = BeautifulSoup(response.text, 'html.parser')
    #check bottom of page for copy and pasted code

    price = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find('fin-streamer').text
    changeInDollars = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text
    changeInPercent = soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text
    openat = soup.find('div', {'class':'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'}).find_all('td')[1].text
    marketCap = soup.find('div', {'class':'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)'}).find_all('td')[1].text
    PERatio = soup.find('div', {'class':'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)'}).find_all('td')[3].text
    dayRange = soup.find('div',{'class':'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'}).find_all('td')[9].text
    #print(dayRange)
    stock = {
            'symbol': symbol,
            'data': {
                'price': [],  # Update this with the actual price data
                'changeInDollars': [],  # Update this with the actual change in dollars data
                'changeInPercent': [],  # Update this with the actual change in percent data
                'open at': [],
                'Market Cap':[],
                'PE Ratio': [],
                'Days range':[],
            }
    }
    stock['data']['price'].append(price)
    stock['data']['changeInDollars'].append(changeInDollars)
    stock['data']['changeInPercent'].append(changeInPercent)
    stock['data']['open at'].append(openat)
    stock['data']['Market Cap'].append(marketCap)
    stock['data']['PE Ratio'].append(PERatio)
    stock['data']['Days range'].append(dayRange)

    return stock

def getSoup(symbol):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    url = f'https://finance.yahoo.com/quote/{symbol}'
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
def getPrice(symbol):
    soup = getSoup(symbol)
    return soup.find('div', {'class': 'D(ib) Mend(20px)'}).find('fin-streamer').text

def getChangeInDollars(symbol):
    soup = getSoup(symbol)
    return soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text
def getChangeInPercent(symbol):
    soup = getSoup(symbol)
    return soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text



'''''''''
for item in MyStocks:
    StockData.append(getData(item))
    print("getting data", item)

with open('stockdata.json', 'w') as f:
    json.dump(StockData, f, indent = 2)


'''''''''''

#Issues while coding: Some URLS do not work! like for GOOGL! but the ones I have chosen will work.

'''''''''
    stock = {
    'symbol': symbol,
    'price':[],# soup.find('div', {'class': 'D(ib) Mend(20px)'}).find('fin-streamer').text,
    'changeInDollars': [],#soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text,
    'changeInPercent': [], #soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text

    }
    '''''''''