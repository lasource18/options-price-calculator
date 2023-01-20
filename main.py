#!/usr/bin/env python
# coding: utf-8
# main.py

from options.options import Options
from flask import Flask
from flask import request, render_template, json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        contract_type = request.form['contract_type']
        market_price = float(request.form['market_price'])
        stock_price = float(request.form['stock_price'])
        strike = float(request.form['strike'])
        exp = int(request.form['exp'])
        rf_rate = float(request.form['rf_rate'])
        vol = float(request.form['vol'])
        div = float(request.form['div'])

        price, price_diff = pricing(contract_type, market_price, stock_price, strike, exp, rf_rate, vol, div)

        opt_price = str(round(price['value']['Option Price'], 2))
        intrinsic_value = str(round(price['value']['Intrinsic Value'], 2))
        time_value = str(round(price['value']['Time Value'], 2))

        delta = str(round(price['greeks']['Delta'], 4))
        gamma = str(round(price['greeks']['Gamma'], 4))
        vega = str(round(price['greeks']['Vega'], 4))
        theta = str(round(price['greeks']['Theta'], 4))
        rho = str(round(price['greeks']['Rho'], 4))

        if price_diff > 0:
            difference = f'The option is undervalued by {abs(price_diff):.2%}.'

        elif price_diff == 0:
            difference = f'The option is fairly valued.'

        else:
            difference = f'The option is overvalued by {abs(price_diff):.2%}.'

        return render_template('index.html',
                               opt_price=opt_price,
                               intrinsic_value=intrinsic_value,
                               time_value=time_value,
                               delta=delta,
                               gamma=gamma,
                               vega=vega,
                               theta=theta,
                               rho=rho,
                               difference=difference
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

def pricing(contract_type, market_price, stock_price, strike, exp, rf_rate, vol, div):
    # Create the option object
    option = Options(contract_type, market_price, stock_price, strike, exp, rf_rate, vol, div)

    # Calculate option's price
    price = option.option_price()

    # Calculate the price difference between observed price and theoritical price
    price_diff = (price['value']['Option Price'] - option.market_price) / option.market_price

    return price, price_diff
    
if __name__ == '__main__':
    app.run()
