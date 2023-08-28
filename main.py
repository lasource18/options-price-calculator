#!/usr/bin/env python
# coding: utf-8
# main.py

from options.options import Option
from flask import Flask
from flask import request, render_template, json
from werkzeug.exceptions import HTTPException
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        contract_type = request.form['contract_type']
        market_price = float(request.form['market_price'])
        spot = float(request.form['stock_price'])
        strike = float(request.form['strike'])
        dte = (datetime.strptime(request.form['exp'], '%Y-%m-%d') - datetime.today()).days/365
        rate = float(request.form['rf_rate'])
        vol = float(request.form['vol'])
        div = float(request.form['div'])

        option = Option(spot, strike, rate, dte, vol, div)

        opt_price = round(option.callPrice, 2) if contract_type == 'C' else round(option.putPrice, 2)
        intrinsic_value = round(max(spot - strike, 0), 2) if contract_type == 'C' else round(max(strike - spot, 0), 2)
        time_value = round(abs(intrinsic_value - opt_price), 2)

        delta = str(round(option.callDelta, 4)) if contract_type == 'C' else str(round(option.putDelta, 4))
        gamma = str(round(option.gamma, 4))
        vega = str(round(option.vega, 4))
        theta = str(round(option.callTheta, 4)) if contract_type == 'C' else str(round(option.putTheta, 4))
        rho = str(round(option.callRho, 4)) if contract_type == 'C' else str(round(option.putRho, 4))
        div_sens = str(round(option.callDivSens, 4)) if contract_type == 'C' else str(round(option.putDivSens, 4))

        price_diff = (opt_price - market_price) / market_price

        if price_diff > 0:
            difference = f'The option is undervalued by {abs(price_diff):.2%}.'

        elif price_diff == 0:
            difference = f'The option is fairly valued.'

        else:
            difference = f'The option is overvalued by {abs(price_diff):.2%}.'

        opt_price = str(opt_price)
        intrinsic_value = str(intrinsic_value)

        data = graph(contract_type, int(spot * 1.2), int(spot * 0.8), strike, rate, vol, dte, div)

        print(data)

        return render_template('index.html',
                               opt_price=opt_price,
                               market_price=market_price,
                               intrinsic_value=intrinsic_value,
                               time_value=time_value,
                               delta=delta,
                               gamma=gamma,
                               vega=vega,
                               theta=theta,
                               rho=rho,
                               div_sens=div_sens,
                               difference=difference,
                               data=data
                )
                                
    elif request.method == 'GET':
        return render_template('index.html')

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response   

def graph(contract_type, upper_bound, lower_bound, strike, rate, vol, dte, div):
    df = pd.DataFrame({'Strike':np.arange(lower_bound, upper_bound)})
    df['Delta'] = df['Gamma'] = df['Vega'] = df['Theta'] = df['Rho'] = df['Dividend Sensitivity'] = 0

    for i in range(len(df)):
        option = Option(df.loc[i, 'Strike'], strike, rate, dte, vol, div)
        if contract_type == 'C':
            df.loc[i, 'Delta'] = option.callDelta
            df.loc[i, 'Theta'] = option.callTheta
            df.loc[i, 'Rho'] = option.callRho
            df.loc[i, 'Dividend Sensitivity'] = option.callDivSens
        else:
            df.loc[i, 'Delta'] = option.putDelta
            df.loc[i, 'Theta'] = option.putTheta
            df.loc[i, 'Rho'] = option.putRho
            df.loc[i, 'Dividend Sensitivity'] = option.putDivSens
        df.loc[i, 'Gamma'] = option.gamma
        df.loc[i, 'Vega'] = option.vega
    
    d = {key:list(df[key]) for key in df.columns}

    return d
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
