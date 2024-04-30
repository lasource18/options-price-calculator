import numpy as np

class MonteCarloOption(object):
    """
        This class uses Monte-Caro simulation to compute the price of an option.
        It can be used for Vanilla European, Asian and Barrier options.
        
        Attributes:
        s0 : int|float [underlying asset current price]
        strike : int|float [strike price]
        sigma : float [underlying asset volatility]
        r : float [interest rate]
        timesteps : int [# of timesteps]
        horizon : int [time horizon]
        n_sims : int [# of simulations]
        category : str [option category]
    """
    def __init__(self, s0, K, mu, sigma, horizon, timesteps, n_sims, category='eu') -> None:
        self.s0 = s0
        self.K = K
        self.mu = round(mu/100, 4)
        self.sigma = round(sigma/100, 4)
        self.horizon = round(horizon, 2)
        self.timesteps = timesteps
        self.n_sims = n_sims
        self.category = category
        self.S = self._simulate_path()

        # The __dict__ attribute
        '''
            Contains all the attributes defined for the object itself. It maps the attribute name to its value
        '''
        for i in ['callPrice', 'putPrice']:
            self.__dict__[i] = None
            
            if self.category == 'eu':
                [self.callPrice, self.putPrice] = self._eu_option_price
            elif self.category == 'asian':
                [self.callPrice, self.putPrice] = self._asian_option_price
            elif self.category == 'lookback':
                [self.callPrice, self.putPrice] = self._lookback_option_price

    @property
    def _eu_option_price(self):
        call = np.exp(-self.mu*self.horizon) * np.mean(np.maximum(0, self.S[-1]-self.K))
        put = np.exp(-self.mu*self.horizon) * np.mean(np.maximum(0, self.K-self.S[-1]))
        return [call, put]

    @property
    def _asian_option_price(self):
        A = self.S.mean(axis=0)

        call = np.exp(-self.mu*self.horizon) * np.mean(np.maximum(0, A-self.K))
        put = np.exp(-self.mu*self.horizon) * np.mean(np.maximum(0, self.K-A))
        return [call, put]
    
    @property
    def _lookback_option_price(self):
        _max = self.S.max(axis=0)
        _min = self.S.min(axis=0)

        call = np.exp(-self.mu*self.horizon) * np.mean(np.maximum(0, _max-self.K))
        put = np.exp(-self.mu*self.horizon) * np.mean(np.maximum(0, self.K-_min))
        return [call, put]

    def _simulate_path(self):
        np.random.seed(2024)
        
        s0 = self.s0
        r = self.mu
        T = self.horizon
        t = self.timesteps
        n = self.n_sims
        
        dt = T/t
        
        S = np.zeros((t,n))
        S[0] = s0
        
        for i in range(t-1):
            W = np.random.standard_normal(n)
            S[i+1] = S[i] * (1 + r*dt + self.sigma*np.sqrt(dt) * W)
            
        return S
    
    def __str__(self) -> str:
        return f'Option[Spot={self.s0}, Strike={self.K}, Rate={self.mu}, Horizon={self.horizon}, Vol={self.sigma}, timesteps={self.timesteps}, simulations={self.n_sims}]'
