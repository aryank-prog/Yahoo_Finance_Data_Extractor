from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timezone

from Yahoo_Closing import *

def get_date():
    wanted_date = input("Input a date in the following format: month-day-year\n")
    #wanted_date = input("Input a date in the following format: month-day-year\n Choices:\n 05-21-2021\n 05-28-2021\n 06-04-2021\n 06-11-2021\n 06-18-2021\n 06-25-2021\n")
    wanted_date_lst = wanted_date.split("-")
    month = wanted_date_lst[0]
    day = wanted_date_lst[1]
    year = wanted_date_lst[2]
    dt = datetime(int(year),int(month), int(day))
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    
    return int(timestamp)    

def get_options_soup(timestamp, ticker):
    #example: https://finance.yahoo.com/quote/TSLA/options?date=1647561600&p=TSLA
    url = f"https://finance.yahoo.com/quote/{ticker}/options?date={timestamp}&p={ticker}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    return soup

"""
#real date is still not being displayed!!
def check_date(soup):
    div = soup.find("div", class_="Pb(10px)")
    
    return div.find("span", class_="Fz(s) Mend(10px)").text
"""

def get_info(soup):
    #navigate to the puts table
    table = soup.find("table", class_="puts W(100%) Pos(r) list-options")

    #gets the titles of the table
    head = table.find("tr", class_="C($tertiaryColor)")

    """
    titles = []

    ths = head.find_all("th")
    for th in ths:
        titles.append(th.text)
    """
    #puts all info into a dictionary
    names = []
    strikes = []
    last_prices = []
    bids = []
    asks = []
    volumes = []
    open_interests = []

    trs = table.find_all("tr")
    for tr in trs[1:]:
        tds = tr.find_all("td")
        for td in tds:
            #contract name
            if td.find("a", class_="Fz(s) Ell C($linkColor)") != None:
                contract_name = td.find("a", class_="Fz(s) Ell C($linkColor)").text
                names.append(contract_name)

            #strike
            if td.find("a", class_="C($linkColor) Fz(s)") != None:        
                strike = td.find("a", class_="C($linkColor) Fz(s)").text
                strikes.append(strike)

        #last price
        last_prices.append(tr.find("td", class_="data-col3 Ta(end) Pstart(7px)").text)

        #bid
        bids.append(tr.find("td", class_="data-col4 Ta(end) Pstart(7px)").text)

        #ask
        asks.append(tr.find("td", class_="data-col5 Ta(end) Pstart(7px)").text)

        #volume
        volumes.append(tr.find("td", class_="data-col8 Ta(end) Pstart(7px)").text)

        #open interest
        open_interests.append(tr.find("td", class_="data-col9 Ta(end) Pstart(7px)").text)
    
    contract_name_lst = list(filter(None.__ne__, names))  
    strikes_lst = list(filter(None.__ne__, strikes))
    last_price_lst = last_prices
    bid_lst = bids
    ask_lst = asks
    volume_lst = volumes
    open_interest_lst = open_interests

    puts_dict = {}

    puts_dict["Contract Name"] = contract_name_lst    
    puts_dict["Strike"] = strikes_lst
    puts_dict["Last Price"] = last_price_lst
    puts_dict["Bid"] = bid_lst
    puts_dict["Ask"] = ask_lst
    puts_dict["Volume"] = volume_lst
    puts_dict["Open Interest"] = open_interest_lst

    return puts_dict


