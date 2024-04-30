import numpy as np
import pandas as pd

class EuFdm(object):
    """
        This class abstracts Vanilla European options on stocks with no dividends.
        It computes the price of the put and the call price for a specific strike,
        using an explicit finite difference scheme. 
        It also computes some greeks (delta, gamma, theta) and the implied volatility of the option.
        
        Attributes:
        strike : int|float [strike price]
        vol : float [underlying asset volatility]
        rate : float [interest rate]
        dte : int|float [days to expiry in number of years]
        NAS : int [# of asset steps]
        mktCallPrice : float [market price of the call]
        mktPutPrice : float [market price of the put]
    """
    def __init__(self, strike, vol, rate, dte, NAS=20):
        self.strike = strike
        self.vol = round(vol/100, 4)
        self.rate = round(rate/100, 4)
        self.dte = round(dte, 4)
        self.NAS = NAS
        self.calls_grid = self._eufdm_grid(1)
        self.puts_grid = self._eufdm_grid(-1)

        # The __dict__ attribute
        '''
            Contains all the attributes defined for the object itself. It maps the attribute name to its value
        '''
        for i in ['callPrice', 'putPrice']:
            self.__dict__[i] = None
            
            [self.callPrice, self.putPrice] = self._price

    @property
    def _price(self):
        call = self.calls_grid.loc[self.strike, self.dte]
        put = self.puts_grid.loc[self.strike, self.dte]
        return [call, put]
    

    def _eufdm_grid(self, flag=1):
        # Specify flag as 1 for calls and -1 for puts

        ds = 2 * self.strike / self.NAS
        dt = 0.9 / self.vol**2 / self.NAS**2
        
        NTS = int(self.dte / dt) + 1
        
        dt = self.dte / NTS
        
        s = np.arange(0, (self.NAS+1)*ds, ds)
        t = self.dte -  np.arange(NTS*dt, -dt, -dt)
        
        grid = np.zeros((len(s), len(t)))
        grid = pd.DataFrame(grid, index=s, columns=np.around(t, 4))
        
        # Set boundary condition at expiry
        grid.loc[:, 0] = abs(np.maximum(flag * (s - self.strike), 0))
        
        for k in range(1, len(t)):
            for i in range(1, len(s)-1):
                delta = (grid.iloc[i+1, k-1] - grid.iloc[i-1, k-1]) / (2*ds)
                gamma = (grid.iloc[i+1, k-1] - 2*grid.iloc[i, k-1] + grid.iloc[i-1, k-1]) / (ds**2)
                theta = (-.5 * self.vol**2 * s[i]**2 * gamma) - (self.rate * s[i] * delta) + (self.rate * grid.iloc[i, k-1])
                grid.iloc[i, k] = grid.iloc[i, k-1] - theta*dt

            # Set boundary condition at S = 0
            grid.iloc[0, k]  = grid.iloc[0, k-1] * (1-self.rate*dt) # ds = rsdt + sigma*sdx, s = 0, ds = 0

            # Set boundary condition at S = infinity # gamma = 0, so you can linearly extract
            grid.iloc[len(s)-1, k] = abs(2 * grid.iloc[len(s)-2, k] - grid.iloc[len(s)-3, k])

        return np.around(grid, 2)
