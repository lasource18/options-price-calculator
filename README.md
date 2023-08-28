# Option Price Calculator

This a simple web application allowing the user to quickly obtain the price of a European option contract (call/put) along with the option's Greeks.

## Project details

The source code is contained in the options.py file. It contains the class definition used to model European option contracts. The design choice of implementing the code using a class was made with the motive of using an object-oriented design in a real-world setting.

This class contains a function used to determine the theoritical price of the option using the Black-Scholes formula.

It also returns the calculated option's Greeks (delta, gamma, theta, vega, rho and dividend sensitivity).

The main script generates a minimal interface to collect and validate (using regex pattern matching) user's input and returns a breakdown of the option's price along with its Greeks. It also indicates whether or not the option is over/under-valued according to the Black-Scholes model. Finally, the Greeks are plotted for range of -/+20% of stock prices from the current strike.

Website: https://options-price-calculator-jbj0yj8wq-lasource18.vercel.app/

### Next Steps (subject to change)

* [x] Refactor the code to convert the console app to a Flask web app 
* [x] Add HTML to improve user experience
* [x] Deploy the app 

*Inspired from: https://github.com/hashABCD/opstrat*

