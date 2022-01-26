#!/usr/bin/env python
# coding: utf-8
# main.py

from options.options import Options
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    contract_type = request.args.get('contract_type', '')
    market_price = request.args.get('market_price', '')
    stock_price = request.args.get('stock_price', '')
    strike = request.args.get('strike', '')
    exp = request.args.get('exp', '')
    rf_rate = request.args.get('rf_rate', '')
    vol = request.args.get('vol', '')
    div = request.args.get('div', '')

    if contract_type != '' and market_price != '' and stock_price != '' and strike != '' and exp != '' and rf_rate != '' and vol != '':
        market_price = float(market_price)
        stock_price = float(stock_price)
        strike = float(strike)
        exp = int(exp)
        rf_rate = float(rf_rate)
        vol = float(vol)
        div = float(div)
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

    else:
        price, price_diff = '', ''
        opt_price = ''
        intrinsic_value = ''
        time_value = ''

        delta = ''
        gamma = ''
        vega = ''
        theta = ''
        rho = ''

        difference = ''

    # Generate HTML (using CSS Bootstrap for styling)
    return (
        """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
                <title>Option Price Calculator</title>
            </head>
            <body>
                <div class="jumbotron">
                    <h1 class="text-center" id="home">Option Price Calculator</h1>
                </div>
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-md-6 offset-md-3 col-sm-12">
                            <form action="" method="get">
                                <div class="form-group">
                                    <span style="display: block;">Contract Type</span>
                                    <input type="radio" name="contract_type" id="call" value="call" checked required>
                                    <label for="call">Call</label>
                                    <input type="radio" name="contract_type" id="put" value="put">
                                    <label for="put">Put</label>
                                </div>
                                <div class="form-group">
                                    <label for="market_price">Market Price (#)</label>
                                    <input type="text" class="form-control" name="market_price" id="market_price" pattern="\\d+\\.?\\d*" required>
                                </div>
                                <div class="form-group">
                                    <label for="stock_price">Stock Price (#)</label>
                                    <input type="text" class="form-control" name="stock_price" id="stock_price" pattern="\\d+\\.?\\d*" required>
                                </div>
                                <div class="form-group">
                                    <label for="strike">Strike (#)</label>
                                    <input type="text" class="form-control" name="strike" id="strike" pattern="\\d+\\.?\\d*" required>
                                </div>
                                <div class="form-group">
                                    <label for="exp">Days to Expiry (#)</label>
                                    <input type="text" class="form-control" name="exp" id="exp" pattern="\\d+" required>
                                </div>
                                <div class="form-group">
                                    <label for="rf_rate">Risk-free Rate (%)</label>
                                    <input type="text" class="form-control" name="rf_rate" id="rf_rate" pattern="\\d+\\.?\\d*" required>
                                </div>
                                <div class="form-group">
                                    <label for="vol">Volatility (%)</label>
                                    <input type="text" class="form-control" name="vol" id="vol" pattern="\\d+\\.?\\d*" required>
                                </div>
                                <div class="form-group">
                                    <label for="div">Dividend Yield (%)</label>
                                    <input type="text" class="form-control" name="div" id="div" pattern="\\d+\\.?\\d*" value="0">
                                </div>
                                <br>
                                <input type="submit" class="btn btn-primary btn-block" name="submit-form" value="Calculate">
                            </form>
                            <br>
                            <div>
                                <h3>Result</h3>
                                <h5>Price Breakdown</h5>
                                <p>Option Price: """ + opt_price + """</p>
                                <p>Intrinsic Value: """ + intrinsic_value + """</p>
                                <p>Time Value: """ + time_value + """</p>
                                <br>
                                <h5>Greeks</h5>
                                <p>Delta: """ + delta + """</p>
                                <p>Gamma: """ + gamma + """</p>
                                <p>Vega: """ + vega + """</p>
                                <p>Theta: """ + theta + """</p>
                                <p>Rho: """ + rho + """</p>
                                <br>
                                <h5>Valuation</h5>
                                <p>""" + difference + """</p>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """
    )

def pricing(contract_type, market_price, stock_price, strike, exp, rf_rate, vol, div):
    # Create the option object
    option = Options(contract_type, market_price, stock_price, strike, exp, rf_rate, vol, div)

    # Calculate option's price
    price = option.option_price()

    # Calculate the price difference between observed price and theoritical price
    price_diff = (price['value']['Option Price'] - option.market_price) / option.market_price

    return price, price_diff
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
