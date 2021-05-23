#gets the closing price of the ticker symbol inputted
from bs4 import BeautifulSoup
import requests

"""
asks user for ticker
returns the soup and ticker inputted as a tuple
"""
def get_closing_soup_and_ticker():
    ticker = input("Enter Ticker: ").upper()
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"
    #try and get the error message to display
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        print("Invalid Ticker! Try again.")
        get_closing_soup_and_ticker()

    soup = BeautifulSoup(r.content, "html.parser")
    
    return (soup, ticker)

"""
takes in the soup from get_closing_soup_and_ticker
gets both the closing price and date for the ticker selected by the user
returns the price and date as a tuple
"""
def get_closing_info(soup):
    div = soup.find("div", class_="D(ib) Mend(20px)")
    price = div.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    div2 = div.find("div", class_="C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm")
    date = div2.find("span", ).text

    return (price, date)