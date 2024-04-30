# Option Price Calculator

## Project details

This a simple web application allowing the user to quickly obtain the price of a European option contract (call/put) along with the option's Greeks and implied volatility. The option's price can be calculated using one of three methods: Black-Scholes, Finite Difference Method and Monte-Carlo simulations. Two types of exotic options are also supported: Asian and Lookback using Monte-Carlo.

The main script generates a minimal interface to collect and validate user's input and returns a breakdown of the option's price along with its Greeks. It also indicates whether or not the option is over/under-valued according to the model. Finally, the Greeks are plotted for range of -/+20% of stock prices from the current strike.

Website: https://options-price-calculator-kg6d9kzkl-lasource18s-projects.vercel.app/

## Prerequisites

Before running this application, ensure you have the following installed:

- Python (version 3.x)

## Steps to Run

1. Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/options-price-calculator.git
```

2. Navigate to the project directory:
```bash
cd options-price-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (if necessary):
```bash
export FLASK_APP=main.py
export FLASK_ENV=development
```

4. Run the Flask application:
```bash
flask run
```

5. Open a web browser and go to http://127.0.0.1:5000 to view the application.

### Next Steps (subject to change)

* [x] Refactor the code to convert the console app to a Flask web app 
* [x] Add HTML to improve user experience
* [x] Deploy the app 

#### Changelog

##### 2024-04-29

* Added bisection method method to caluculate implied volatility
* Added Finite-difference method and Monte-Carlo simulations 
* Added support for Asian and Lookback options
* Minor bug fixes and reformatting

*Inspired from: https://github.com/hashABCD/opstrat*

