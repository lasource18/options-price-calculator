#
# Simple class to create a template to model European option contracts
# Author: Claude-Micael Guinan
# Date: 2021-10-12
# Last update: 2024-04-12
#

import math
from utils import pdf, cdf

class BlackScholesOption(object):
    """
        This class abstracts Vanilla European options on stocks with dividends.
        It computes the price of the put and the call price for a specific strike,
        using the Black-Scholes model. 

        Attributes:
        spot : int|float [underlying asset current price]
        strike : int|float [strike price]
        rate : int|float [interest rate]
        dte : int|float [days to expiry in number of years]
        vol : int|float [underlying asset volatility]
        div : int|float [underlying asset dividend yield]
        mktCallPrice : int|float|None [market price of the call]
        mktPutPrice : int|float|None [market price of the put]
    """
    def __init__(self, spot, strike, rate, dte, vol, div=0, mktCallPrice=None, mktPutPrice=None):
        self.spot = spot
        self.strike = strike
        self.rate = round(rate / 100, 4)
        self.dte = round(dte, 4)
        self.vol = round(vol / 100, 4)
        self.div = round(div / 100, 4)
        # Utility
        self._a_ = self.vol * self.dte ** 0.5
        # Call Option market price
        self.mktCallPrice = mktCallPrice
        # Put Option market price
        self.mktPutPrice = mktPutPrice
        
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
        for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', 'callTheta', 'putTheta', 'callRho', 'putRho', 'callDivSens','putDivSens', 'vega', 'gamma']:
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
            call = self.spot * self._c_ * cdf(self._d1_) - self.strike * self._b_ * cdf(self._d2_)
            put = self.strike * self._b_ * cdf(-self._d2_) - self.spot * self._c_ * cdf(-self._d1_)

        return [call, put]

    # Option Delta
    @property
    def _delta(self):
        ''' Returns the option delta: [Call delta, Put delta]'''
        if self.vol == 0 or self.dte == 0:
            call = 1.0  if self.spot > self.strike else 0.0
            put = -1.0 if self.spot < self.strike else 0.0

        else:
            call = self._c_ * cdf(self._d1_)
            put = -self._c_ * cdf(-self._d1_)

        return [call, put]

    # Option Gamma
    @property
    def _gamma(self):
        ''' Returns the option gamma'''
        return self._c_ * pdf(self._d1_) / (self.spot * self._a_)

    # Option Vega
    @property
    def _vega(self):
        ''' Returns the option vega'''
        if self.vol == 0 or self.dte == 0:
            return 0.0
        else:
            return self.spot * self._c_ * pdf(self._d1_) * self.dte**0.5 / 100

    # Option Theta
    @property
    def _theta(self):
        ''' Returns the option theta: [Call theta, Put theta]'''
        call =  (-1 * (self._c_ * self.spot * pdf(self._d1_) * self.vol) / (2*self.dte**0.5)) + (self.div * self.spot * self._c_) - (self.rate * self.strike * self._b_ * cdf(self._d2_))
        put = (-1 * (self._c_ * -self.spot * pdf(self._d1_) * self.vol) / (2*self.dte**0.5)) - (self.div * self.spot * self._c_) + (self.rate * self.strike * self._b_ * cdf(self._d2_))

        return [call / 365, put / 365]

    # Option Rho
    @property
    def _rho(self):
        ''' Returns the option rho: [Call rho, Put rho]'''
        call = self.strike * self.dte * self._b_ * cdf(self._d2_) / 100
        put = -self.strike * self.dte * self._b_ * cdf(-self._d2_) / 100

        return [call, put]

    @property
    def _div_sens(self):
        ''' Returns the option sensitivity to the dividend yield: [Call div_sens, Put div_sens]'''
        call = -self.dte * self.spot * self._c_ * cdf(self._d1_)
        put = self.dte * self.spot * self._c_ * cdf(-self._d1_)

        return [call, put]

    def callImpliedVol(self):
        '''Derive the implied volatility for calls using the bisection method'''
        if self.mktCallPrice is None:
            return self.vol
        else:
            iv = self._bisection_iv(_type='call')
            return iv
    
    def putImpliedVol(self):
        '''Derive the implied volatility for puts using the bisection method'''
        if self.mktPutPrice is None:
            return self.vol
        else:
            iv = self._bisection_iv(_type='put')
            return iv
    
    def _bisection_iv(self, high=500.0, low=0.0, tolerance=1e-7, _type='call'):
        for i in range(1000):
            mid = (high+low) / 2
            if mid < tolerance:
                mid = tolerance

            if _type == 'call':
                price = self.mktCallPrice
                estimate = eval(self.__class__.__name__)(self.spot, self.strike, self.rate, self.dte, mid, self.div).callPrice
            
            if _type == 'put':
                price = self.mktPutPrice
                estimate = eval(self.__class__.__name__)(self.spot, self.strike, self.rate, self.dte, mid, self.div).putPrice
            
            if round(estimate, 6) == price:
                break
            elif estimate > price:
                high = mid
            elif estimate < price:
                low = mid
                
        return mid
    
    def __str__(self) -> str:
        return f'Option[Spot={self.spot}, Strike={self.strike}, Rate={self.rate}, DTE={self.dte}, Vol={self.vol}, Div={self.div}, MktCallPrice={self.mktCallPrice}, MktPutPrice={self.mktPutPrice}]'

