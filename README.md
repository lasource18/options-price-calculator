# Option Price Calculator

The is a simple console application allowing the user to quickly obtain the price of a European option contract (call/put) along with the option's Greeks.

## Project details

The source code is contained in the options.py file. It contains the class definition used to model European option contracts.

This class contains a single function used to determine the theoritical price of the option, its intrinsic value and its time_value using the Black-Scholes formula.

It also returns the calculated option's Greek (delta, gamma, theta, vega and rho).

The main script collect and validates (using input validation functions of the PyInputPlus class) user's input and returns the above function's output in a nice format. It also indicate whether or not the option is over/under-valued.

**Sample output**
![Sample Output] (sample_output.png)

### How to install the required modules

Run this command on your terminal/command prompt.
```
pip install -r requirements.txt
```
### Next Steps (subject to change)

* Refactor the code to convert the console app to a web app using Flask 
* Add HTML to improve user experience
* Deploy the app using Google App Engine

*Inspired from: https://github.com/hashABCD/opstrat*

