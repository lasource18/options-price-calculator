#!/usr/bin/env python
# coding: utf-8
# main.py

import pyinputplus as pyip
from options.options import Options

def main():
    while True:
        print('  Start Option Price Calculator app  ')
        print('=====================================\n')

        # Get input from the user
        contract_type = pyip.inputChoice(['c', 'p'], prompt="Enter the contract type ('p' = put; 'c'= call): ")
        market_price = pyip.inputFloat(prompt='Enter the current market price of the option: ', min=0.01)
        stock_price = pyip.inputFloat(prompt='Enter the current stock price: ', min=0.5)
        strike = pyip.inputFloat(prompt='Enter the strike price: ', min=0.5)
        exp = pyip.inputInt(prompt='Enter the number of days to expiry: ', min=1)
        rf_rate = pyip.inputFloat(prompt='Enter the risk free rate: ', min=0.0)
        vol = pyip.inputFloat(prompt='Enter the volatility: ', min=0.5)
        div = pyip.inputFloat(prompt='Enter the dividend yield: ', min=0.0, default=0.0)

        # Create the option object
        option = Options(contract_type, market_price, stock_price, strike, exp, rf_rate, vol, div)

        # Calculate price
        price = option.option_price()

        # Print each item on a different line
        print()
        formatted_output(price)

        # Calculate the price difference between observed price and theoritical price
        price_diff = (price['value']['Option Price'] - option.market_price) / option.market_price

        if price_diff > 0:
            print(f'The option is undervalued by {price_diff:.2%}.')

        elif(price_diff == 0):
            print(f'The option is fairly valued.')

        else:
            print(f'The option is overvalued by {price_diff:.2%}.')

        loop = pyip.inputChoice(['y', 'n'], prompt="\nWould you like to get the price of another contract [y/n]? ", default='n')

        if loop.lower() == 'y':
            continue

        else:
            print('\n===================================')
            print('  End Option Price Calculator app  ')
            break

def formatted_output(obj):
    for outer_key in obj.keys():
        for inner_key, value in obj[outer_key].items():
            print(f'{inner_key}: {value: .5f}')
        print()
    
if __name__ == '__main__':
    main()

