#
# Simple class to create a template to model European option contracts
# Author: Claude-Micael Guinan
# Date: 2021-10-12
#

import math
from scipy.stats import norm

class Option:
    """
        This is a class for Options contract for pricing European options on stocks without dividends.
        Attributes:
        spot : int or float
        strike : int or float
        rate : float
        dte : int or float [days to expiration in number of years]
        vol : float
        div : float
    """
    def __init__(self, spot, strike, rate, dte, vol, div):
        # Spot Price
        self.spot = spot
        # Option Strike
        self.strike = strike
        #Interest rate
        self.rate = rate / 100
        # Days To Expiry
        self.dte = dte
        # Volatility
        self.vol = vol / 100
        # Dividend
        self.div = div / 100
        # Utility
        self._a_ = self.vol * self.dte ** 0.5
        
        if self.strike == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            self._d1_ = (math.log((self.spot/self.strike) + (self.rate - self.div + (self.vol)**2) / 2) * self.dte) / self._a_
        
        self._d2_ = self._d1_ - self._a_
        self._b_ = math.e ** (-self.rate * self.dte)
        self._c_ = math.e ** (-self.div * self.dte)
        
        # The __dict__ attribute
        '''
            Contains all the attributes defined for the object itself. It maps the attribute name to its value
        '''
        for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', 'callTheta', 'putTheta', 'callRho', 'putRho', 'vega', 'gamma']:
            self.__dict__[i] = None
            
            [self.callPrice, self.putPrice] = self._price
            [self.callDelta, self.putDelta] = self._delta
            [self.callTheta, self.putTheta] = self._theta
            [self.callRho, self.putRho] = self._rho
            [self.callDivSens, self.putDivSens] = self._div_sens
            self.vega = self._vega
            self.gamma = self._gamma
            
    # Option Price
    @property
    def _price(self):
        ''' Returns the option price: [Call price, Put price]'''
        if self.vol == 0 or self.dte == 0:
            call = max(0.0, self.spot - self.strike)
            call = max(0.0, self.strike - self.spot)
        else:
            call = self.spot * self._c_ * norm.cdf(self._d1_) - self.strike * self._b_ * norm.cdf(self._d2_)
            put = self.strike * self._b_ * norm.cdf(-self._d2_) - self.spot * self._c_ * norm.cdf(-self._d1_)

        return [call, put]

    # Option Delta
    @property
    def _delta(self):
        ''' Returns the option delta: [Call delta, Put delta]'''
        if self.vol == 0 or self.dte == 0:
            call = 1.0  if self.spot > self.strike else 0.0
            put = -1.0 if self.spot < self.strike else 0.0

        else:
            call = self._c_ * norm.cdf(self._d1_)
            put = - self._c_ * norm.cdf(-self._d1_)

        return [call, put]

    # Option Gamma
    @property
    def _gamma(self):
        ''' Returns the option gamma'''
        return self._c_ * norm.pdf(self._d1_) / (self.spot * self._a_)

    # Option Vega
    @property
    def _vega(self):
        ''' Returns the option vega'''
        if self.vol == 0 or self.dte == 0:
            return 0.0
        else:
            return self.spot * self._c_ * norm.pdf(self._d1_) * self.dte**0.5 / 100

    # Option Theta
    @property
    def _theta(self):
        ''' Returns the option theta: [Call theta, Put theta]'''
        call =  (-1 * (self._c_ * self.spot * norm.pdf(self._d1_) * self.vol) / (2*self.dte**0.5)) + (self.div * self.spot * self._c_) - (self.rate * self.strike * self._b_ * norm.cdf(self._d2_))
        put = (-1 * (self._c_ * -self.spot * norm.pdf(self._d1_) * self.vol) / (2*self.dte**0.5)) - (self.div * self.spot * self._c_) + (self.rate * self.strike * self._b_ * norm.cdf(self._d2_))

        return [call / 365, put / 365]

    # Option Rho
    @property
    def _rho(self):
        ''' Returns the option rho: [Call rho, Put rho]'''
        call = self.strike * self.dte * self._b_ * norm.cdf(self._d2_) / 100
        put = -self.strike * self.dte * self._b_ * norm.cdf(-self._d2_) / 100

        return [call, put]

    @property
    def _div_sens(self):
        ''' Returns the option sensitivity to the dividend yield: [Call div_sens, Put div_sens]'''
        call = -self.dte * self.spot * self._c_ * norm.cdf(self._d1_)
        put = self.dte * self.spot * self._c_ * norm.cdf(-self._d1_)

        return [call, put]

