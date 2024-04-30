import pandas as pd
import numpy as np

def graph(class_name, contract_type, upper_bound, lower_bound, strike, rate, vol, dte, div, market_price):
    df = pd.DataFrame({'Strike':np.arange(lower_bound, upper_bound)})
    df['Delta'] = df['Gamma'] = df['Vega'] = df['Theta'] = df['Rho'] = 0

    for i in range(len(df)):
        if contract_type == 'C':
            option = eval(class_name)(df.loc[i, 'Strike'], strike, rate, dte, vol, div, mktCallPrice=market_price)
            df.loc[i, 'Delta'] = option.callDelta
            df.loc[i, 'Theta'] = option.callTheta
            df.loc[i, 'Rho'] = option.callRho
        else:
            option = eval(class_name)(df.loc[i, 'Strike'], strike, rate, dte, vol, div, mktPutPrice=market_price)
            df.loc[i, 'Delta'] = option.putDelta
            df.loc[i, 'Theta'] = option.putTheta
            df.loc[i, 'Rho'] = option.putRho
        df.loc[i, 'Gamma'] = option.gamma
        df.loc[i, 'Vega'] = option.vega
    
    d = {key:list(df[key]) for key in df.columns}

    return d

def valuation(opt_price, market_price):
    price_diff = (opt_price - market_price) / market_price

    if price_diff > 0:
        difference = f'The option is undervalued by {abs(price_diff):.2%}.'

    elif price_diff == 0:
        difference = f'The option is fairly valued.'

    else:
        difference = f'The option is overvalued by {abs(price_diff):.2%}.'

    return difference