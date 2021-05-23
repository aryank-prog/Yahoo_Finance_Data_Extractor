#brings all the files together
from datetime import time
from bs4 import BeautifulSoup

from Yahoo_Closing import *
from Yahoo_Options import *
from XL import *

def main():
    #Yahoo Closing
    closing_tup = get_closing_soup_and_ticker()
    closing_soup = closing_tup[0]
    ticker = closing_tup[1]
    print("")
    print(f"--- OPTIONS INFORMATION FOR {ticker} STOCK ---")
    closing_info = get_closing_info(closing_soup)
    print(closing_info[0] + " --- " + closing_info[1])
    print("")

    ##########

    #Yahoo Options
    dates = get_dates()
    timestamps = get_unix(dates)
    options_soups = get_options_soup(timestamps, ticker)
    #print(check_date(options_soup))
    soups_lst = []
    for soup in options_soups:
        puts_dict = get_info(soup, closing_info[0])
        soups_lst.append(puts_dict)
    puts = merge(soups_lst)
    
    ##########

    #XL 
    write(puts)

main()