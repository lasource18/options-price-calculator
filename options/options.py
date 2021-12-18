#
# Simple class to create a template to model European option contracts
# Author: Claude-Micael Guinan
# Date: 2021-10-12
#

import numpy as np
from scipy.special import ndtr

class Options:
    """
    This class models a vanilla European option contract.
    It provides a method called option_price() to calculate the theoritical price of the contract.
    The calculation of the contract's price relies on the Blach-Scholes framework
    to value an European option contract on a dividend paying stock.

    Useful links
    ------------
    Options: https://www.investopedia.com/options-basics-tutorial-4583012
    Black-Scholes model: https://www.investopedia.com/terms/b/blackscholes.asp
    Greeks: https://www.optionsplaybook.com/options-introduction/option-greeks/
    """
    def __init__(self, contract_type : str, market_price : float, stock_price : float, strike : float, exp : int, rf_rate : float, vol : float, div : float):
        """
        Parameters
        ----------
        contract_type (str): call or put
        stock_price (float): Current Stock Price 
        strike (float): Exercise price 
        exp (int): Time to expiration in days 
        rf_rate (float): Risk-free rate 
        vol (float): Volatility 
        """
        self.contract_type = contract_type
        self.market_price = market_price
        self.stock_price = stock_price
        self.strike = strike
        self.exp = exp / 252
        self.rf_rate = rf_rate / 100
        self.vol = vol / 100
        self.div = div / 100

    def option_price(self):
        """
        This method as the name suggests is used calculate the price of an option.
        The formula used will depend on the type of contract. That is:
        - Call: S*e^(-qt)*N(d1) - Ke(-rt)N(d2)
        - Put: Ke(-rt)N(-d2) - S*e^(-qt)*N(-d1)
        This method also calculate the options' greeks (delta, gamma, theta, rho)
        and the implied volatility.
        
        Parameters
        ----------
        None

        Returns the option's theoritical price, intrinsic value and time value
        and the greeks of the option as a dictionary.
        """
        d1 = (np.log(self.stock_price/self.strike) + (self.rf_rate - self.div + (pow(self.vol,2))/2))/(self.vol * np.sqrt(self.exp))
        d2 = d1 - self.vol * np.sqrt(self.exp)

        A = self.stock_price * np.exp(-self.div * self.exp)
        B = self.strike * np.exp(-self.rf_rate * self.exp)
        
        # If contract_type = 'call' calculate the price of a call
        if self.contract_type.lower() == 'call':
            N_d1 = ndtr(d1)
            N_d2 = ndtr(d2)
            option_price = A * N_d1 - B * N_d2
            intrinsic_val = max(self.stock_price - self.strike, 0)

        # If contract_type = 'put' calculate the price of a put
        elif self.contract_type.lower() == 'put':
             N_d1 = ndtr(-d1)
             N_d2 = ndtr(-d2)
             option_price = B * N_d2 - A * N_d1
             intrinsic_val = max(self.strike - self.stock_price, 0)

        time_val = option_price - intrinsic_val
        
        value = {'Option Price': option_price, 'Intrinsic Value': intrinsic_val, 'Time Value': time_val}

        # Calculate the greeks
        
        if self.contract_type == 'call':
            delta = N_d1 * np.exp(-self.div * self.exp)
            theta = (-(((self.stock_price * self.vol * np.exp(-self.div*self.exp))/(2*np.sqrt(self.exp))) * ((np.exp(-pow(d1, 2)/2))/(2*np.pi) ))
                     - (self.rf_rate*self.strike*np.exp(-self.exp*self.rf_rate) * N_d2 + self.stock_price * np.exp(-self.div*self.exp) * N_d1)) / 252
            rho = (self.strike * self.exp * np.exp(-self.rf_rate*self.exp) * N_d2) / 100

        else:
            delta = (N_d1 - 1) * np.exp(-self.div * self.exp)
            theta = (-(((self.stock_price * self.vol)/(2*np.sqrt(self.exp))) * ((np.exp(-pow(d1, 2)/2))/(2*np.pi) ))
                     - (self.rf_rate*self.strike*np.exp(-self.exp*self.rf_rate) * N_d2 + self.stock_price * np.exp(-self.div*self.exp) * N_d1)) / 252
            rho = -(self.strike * self.exp * np.exp(-self.rf_rate*self.exp) * N_d2) / 100

        gamma = (np.exp(-self.div*self.exp) / self.stock_price*self.vol) * (1 / np.sqrt(2*np.pi) * np.exp(-pow(d1,2)/2))
        vega = (1 / 100 * (self.stock_price*np.exp(-self.div*self.exp)*np.sqrt(self.exp))) * (1 / np.sqrt(2*np.pi) * np.exp(-pow(d1,2)/2))

        greeks = {'Delta': delta, 'Gamma': gamma, 'Theta': theta, 'Vega': vega, 'Rho': rho}

        result = {'value': value, 'greeks': greeks}

        return result

