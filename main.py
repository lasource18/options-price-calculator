#!/usr/bin/env python
# coding: utf-8
# main.py

from options.bs import BlackScholesOption
from options.monte_carlo import MonteCarloOption
from options.fdm import EuFdm
from flask import Flask
from flask import request, render_template, json
from werkzeug.exceptions import HTTPException
from datetime import datetime
from utils import graph, valuation

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/vanilla', methods=['GET'])
def vanilla():
    return render_template('vanilla.html')

@app.route('/exotic', methods=['GET'])
def exotic():
    return render_template('exotic.html')

@app.route('/bs', methods=['GET', 'POST'])
def bs():
    if request.method == 'POST':
        contract_type = request.form['contract_type']
        market_price = float(request.form['market_price'])
        spot = float(request.form['stock_price'])
        strike = float(request.form['strike'])
        dte = (datetime.strptime(request.form['exp'], '%Y-%m-%d') - datetime.today()).days/252
        rate = float(request.form['rf_rate'])
        vol = float(request.form['vol'])
        div = float(request.form['div'])

        if contract_type == 'C':
            option = BlackScholesOption(spot, strike, rate, dte, vol, div, mktCallPrice=market_price)
        else:
            option = BlackScholesOption(spot, strike, rate, dte, vol, div, mktPutPrice=market_price)

        opt_price = round(option.callPrice, 2) if contract_type == 'C' else round(option.putPrice, 2)
        intrinsic_value = round(max(spot - strike, 0), 2) if contract_type == 'C' else round(max(strike - spot, 0), 2)
        time_value = round(abs(intrinsic_value - opt_price), 2)

        delta = str(round(option.callDelta, 4)) if contract_type == 'C' else str(round(option.putDelta, 4))
        gamma = str(round(option.gamma, 4))
        vega = str(round(option.vega, 4))
        theta = str(round(option.callTheta, 4)) if contract_type == 'C' else str(round(option.putTheta, 4))
        rho = str(round(option.callRho, 4)) if contract_type == 'C' else str(round(option.putRho, 4))
        div_sens = str(round(option.callDivSens, 4)) if contract_type == 'C' else str(round(option.putDivSens, 4))
        imp_vol = str(round(option.callImpliedVol(), 2)) if contract_type == 'C' else str(round(option.putImpliedVol(), 2))

        difference = valuation(opt_price, market_price)

        data = graph('BlackScholesOption', contract_type, int(spot * 1.2), int(spot * 0.8), strike, rate, vol, dte, div, market_price)

        # print(data)

        return render_template('bs.html',
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
                               imp_vol=imp_vol,
                               difference=difference,
                               data=data
                )
                                
    elif request.method == 'GET':
        return render_template('bs.html')
    
@app.route('/fdm', methods=['GET', 'POST'])
def fdm():
    if request.method == 'POST':
        contract_type = request.form['contract_type']
        market_price = float(request.form['market_price'])
        spot = float(request.form['stock_price'])
        strike = float(request.form['strike'])
        dte = (datetime.strptime(request.form['exp'], '%Y-%m-%d') - datetime.today()).days/252
        rate = float(request.form['rf_rate'])
        vol = float(request.form['vol'])
        steps = int(request.form['steps'])

        if contract_type == 'C':
            option = EuFdm(strike, vol, rate, dte, steps)
        else:
            option = EuFdm(strike, vol, rate, dte, steps)

        opt_price = round(option.callPrice, 2) if contract_type == 'C' else round(option.putPrice, 2)
        intrinsic_value = round(max(spot - strike, 0), 2) if contract_type == 'C' else round(max(strike - spot, 0), 2)
        time_value = round(abs(intrinsic_value - opt_price), 2)

        difference = valuation(opt_price, market_price)

        return render_template('fdm.html', 
                                opt_price=opt_price,
                                market_price=market_price,
                                intrinsic_value=intrinsic_value,
                                time_value=time_value,
                                difference=difference)

    elif request.method == 'GET':
        return render_template('fdm.html')

@app.route('/monte-carlo/<category>', methods=['GET', 'POST'])
def monte_carlo(category):
    if request.method == 'POST':
        contract_type = request.form['contract_type']
        market_price = float(request.form['market_price'])
        spot = float(request.form['stock_price'])
        strike = float(request.form['strike'])
        sigma = float(request.form['sigma'])
        mu = float(request.form['mu'])
        horizon = (datetime.strptime(request.form['horizon'], '%Y-%m-%d') - datetime.today()).days/252
        timesteps = int(request.form['timesteps'])
        n_sims = int(request.form['n_sims'])

        option = MonteCarloOption(spot, strike, mu, sigma, horizon, timesteps, n_sims, category)
        print(option.callPrice, option.putPrice)
        opt_price = round(option.callPrice, 2) if contract_type == 'C' else round(option.putPrice, 2)
        intrinsic_value = round(max(spot - strike, 0), 2) if contract_type == 'C' else round(max(strike - spot, 0), 2)
        time_value = round(abs(intrinsic_value - opt_price), 2)

        difference = valuation(opt_price, market_price)

        return render_template('monte_carlo.html', 
                               opt_price=opt_price,
                               market_price=market_price,
                               intrinsic_value=intrinsic_value,
                               time_value=time_value,
                               difference=difference,
                               category=category)

    elif request.method == 'GET':
        return render_template('monte_carlo.html', category=category)

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
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
