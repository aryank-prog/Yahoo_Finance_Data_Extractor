#return a dictionary that contains all the required Puts data
from bs4 import BeautifulSoup
import requests, re
from datetime import date, datetime, timezone

from Yahoo_Closing import *

"""
user inputs a date which they want the Puts info for
uses the datetime package to convert the inputted date into unix time
returns the unix time (as an int)

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
"""

"""
gets all the dates that need to be analyzed (for the year 2021)
returns a list of all the dates
"""
def get_dates(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/options?p={ticker}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    div = soup.find("div", class_="Fl(start) Pend(18px)")
    lst = div.find_all("option")    

    dates = []
    for item in lst:
        if "2021" in item.text:
            dates.append(item.text)

    return dates

"""
gets the unix timestamp of each date in the imputted list
returns a list of the unix timestamps for each date
"""
def get_unix(dates):
    timestamps = []
    for date in dates:
        month_re = "(\w+\w) [\d]"
        day_re = "(\d{1,2})[,]"
        
        month_name = re.findall(month_re, date)[0]
        day = int(re.findall(day_re, date)[0])
        year = 2021

        datetime_object = datetime.strptime(month_name, "%B")
        month_num = int(datetime_object.month)

        dt = datetime(int(year),int(month_num), int(day))
        timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

        timestamps.append(int(timestamp))

    return timestamps


"""
returns the soups for all the selected date's Puts info
"""
def get_options_soup(timestamps, ticker):
    #example: https://finance.yahoo.com/quote/TSLA/options?date=1647561600&p=TSLA
    soups = []
    for item in timestamps:
        url = f"https://finance.yahoo.com/quote/{ticker}/options?date={item}&p={ticker}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        soups.append(soup)

    return soups

"""
#real date is still not being displayed!!
def check_date(soup):
    div = soup.find("div", class_="Pb(10px)")
    
    return div.find("span", class_="Fz(s) Mend(10px)").text
"""

"""
takes the selected date's soup and the ticker's closing price as an input
gets all the necessary data from the Puts table
returns a dictionary of all the received data
"""
def get_info(soup, closing_price):
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

    #creates the list that contains just the closing price
    closing_price_lst = []
    for i in range(len(contract_name_lst)):
        closing_price_lst.append(closing_price)

    puts_dict = {}

    puts_dict["Contract Name"] = contract_name_lst   
    puts_dict["Closing Price"] = closing_price_lst 
    puts_dict["Strike"] = strikes_lst
    puts_dict["Last Price"] = last_price_lst
    puts_dict["Bid"] = bid_lst
    puts_dict["Ask"] = ask_lst
    puts_dict["Volume"] = volume_lst
    puts_dict["Open Interest"] = open_interest_lst

    return puts_dict

"""
takes in the list of dictionaries that contain all the info for each timestamp
merges the dictioaries into one
returns the merged dictionary
"""
def merge(puts):
    merged = {}
    names = []
    closing_prices = []
    strikes = []
    last_prices = []
    bids = []
    asks = []
    volumes = []
    open_interests = []

    for item in puts:
        for j in item:
            if j == "Contract Name":
                names.extend(item[j])
            elif j == 'Closing Price':
                closing_prices.extend(item[j])
            elif j == "Strike":
                strikes.extend(item[j])
            elif j == "Last Price":
                last_prices.extend(item[j])
            elif j == "Bid":
                bids.extend(item[j])
            elif j == "Ask":
                asks.extend(item[j])
            elif j == "Volume":
                volumes.extend(item[j])
            elif j == "Open Interest":
                open_interests.extend(item[j])
    
    for item in puts:
        for j in item:
            if j == "Contract Name":
                merged[j] = names
            elif j == 'Closing Price':
                merged[j] = closing_prices
            elif j == "Strike":
                merged[j] = strikes
            elif j == "Last Price":
                merged[j] = last_prices
            elif j == "Bid":
                merged[j] = bids
            elif j == "Ask":
                merged[j] = asks
            elif j == "Volume":
                merged[j] = volumes
            elif j == "Open Interest":
                merged[j] = open_interests
            
    return merged

