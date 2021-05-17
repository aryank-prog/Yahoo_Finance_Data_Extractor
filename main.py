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
    timestamp = get_date()
    options_soup = get_options_soup(timestamp, ticker)
    #print(check_date(options_soup))
    puts_dict = get_info(options_soup)

    ##########

    #XL 
    write(puts_dict)

main()