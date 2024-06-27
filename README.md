# Overview
This script uses Gemini.com's public Rest API to look for deviation in currency pair prices

## Docker (PREFERRED)
### Build Docker Image

docker build . -t gemini:local

### Running Docker Image

docker run -rm gemini:local [flags]

#### Flags
-h, --help          show this help message and exit \
-c CURRENCY, --currency CURRENCY \
                    Currency trading currency or ALL (default: ALL) \
-d DEVIATION, --deviation DEVIATION \
                    Standard deviation threshold (default: 1.0) \
 -l LOG_LEVEL, --log_level LOG_LEVEL \
                    Log level of DEBUG, INFO, or ERROR (default: INFO) 

```docker run --rm gemini:local -h``` for help info

By default this will run against all currency pairs with standard deviation set to 1.0 and INFO logging.
```docker run --rm gemini:local```

Adjust flags as needed to specify single currency pairs, change deviation, or log levels.

eg: ```docker run --rm gemini:local --currency BTCUSD --deviation 2.0```

## Local Build
The script can be run locally with an appropriate version of python and the requirements.txt file. \
It is recommended to use pyenv, andaconda, or miniconda to avoid muddying other project environments.

### Requirements
Python 3.11.x \
numpy==2.0.0 \
requests==2.32.3 \

The additional package can be installed via ```pip install -r requirements.txt```

### Running 
```python gemini.py``` or ```python3 gemini.py``` according to your how python is set up in your environment.

Assuming ```python``` is correct for your environment:
```python gemini.py -h``` will generate help info to express the flags available.

#### Flags
-h, --help          show this help message and exit \
-c CURRENCY, --currency CURRENCY \
                    Currency trading currency or ALL (default: ALL) \
-d DEVIATION, --deviation DEVIATION \
                    Standard deviation threshold (default: 1.0) \
 -l LOG_LEVEL, --log_level LOG_LEVEL \
                    Log level of DEBUG, INFO, or ERROR (default: INFO) 

By default this will run against all currency pairs with standard deviation set to 1.0 and INFO logging.
```python gemini.py```

Adjust flags as needed to specify single currency pairs, change deviation, or log levels.

eg: ```python gemini.py --currency BTCUSD --deviation 2.0```


## Further Improvements
#### Logging
Either using the built in logger module and arranging the formatting or at least normalizing the functions into one function. \
It would be good to get most of the details for logging out of the gemini class if possible. \

Also handling the full list of log levels to match standards. Right now it only takes DEBUG, INFO, and ERROR specifically. 

#### Timestamps
Timestamps having microseconds may or may not be valuable. \
I would think in most cases they wouldn't be important and could be truncated for readability. \
However transaction histories may be quite fast in high frequency trading so it may be best to leave them. 


#### Error Handling
Error handling is currently basic. \
It would be good to put futher effort in to figure out when: 
* errors should stop all operation vs continue 
* errors should be handled within a function vs bubble up 
* any other sections that could use some checked such as the analysis function in case data is missing 

#### Typing / Parameterization
Most of the functions have types specified with the parameters and returns but a few got left out such as the logging functions 

#### Value normalization
There are some cases when I am using the built in float and some where I let NumPy handle floats. \
These aren't going to be at the same decimal value. They should be examined and decided on what float value is needed and normalize everything to use it to avoid risk of data loss / truncation. 

#### Class data vs passed data
There is a mix of data that is stored as part of the initalized class and some that is passed around between the class. \
There are some approaches to look over, either making more variables held by the instance or passing more around. \
For instance, removing the currency pair from the class and making it something passed in could lead to removing most class variables and handling everything with whatever is passed in during the moment. It could be a single call to handle everything that way. \
Inversely, cleaning up and normalinzing what's in the class would leave an object that could be examined as it does work or after it does work without redoing API calls to gather data. \
Either way, some normalization of the self. variables and the passed around variables would be good. 


## Future Features / Ideas
With price changes available, watching for peaks or valleys along with the deviation change data could suggest sell/buy times. \
If a known buy price is available, this data could suggest sell times based upon the current price. \
Watching multiple pairs could show price deviation between a shared currency that could give an buy/sell option if they move in different directions. \
Such as watching BTCUSD and ETHUSD when one moves up and the other moves down, it could be a good time to sell one and buy the other off of the premise of holding one or more of them, wanting additional investment, and low concern of continuing drops. \
There are likely high frequency trading type alerts and could be quite noisy, though. 

## Approach
I started the script with making some of the argparse parameters. \
With some optional ones I didn't know if I would make, I opted to start examing the API to start making small functions. 

I started looking at the public gemini API for a currency pair list. \
I hoped to avoid having to generate keys and pass them around to keep initial development time shorter. \
I found the the available currency pairs via the gemini api. \
Then I looked at what I could do to get the right data to be able to calculate standard deviation info by looking for some kind of history or price change data. \
I settled on the Ticker v2 endpoint. \
Once I could generate deviation, I looked at the additional data for the output to see what needed to be calculated vs what was already there available. \
Luckily, everything I needed was available through the ticker data so I didn't need to chain any further requests. 

I already had these somewhat split into functions so wrapped them in a class and started adding details to parameterize the functions. \
Having the option to handle multiple currencies helped define the main function with most of the others being smaller task functions. 

I tied the arguments from argparse into the class and polished them up a little. 

Finally, I created a basic logging function to get the output format and duplicated it for different outputs due to differening input parameters. 
 
After a bit of clean up, I focused on getting some documentation written. 


## Issues
#### Standard deviation and notional value

I had some issues here as I haven't had to deal with things like currency exchanges and such so am unfamiliar with things like standard deviation and notional value outside of college classes some time ago. I'm still uncertain if these are all correct as it's quite a bit to try to grok at once. \
Looking at python and standard deviation with numpy defined most of what I came up with. 

#### Logging 
I had intially wanted to use the logger and do some kind of format override so it would be easy to call. \
Though there is some availability to override formatting, I kept having it print it outside of JSON format so moved to a quick and dirty method. \
This could use some attention as I'm sure there's a right way to do this. \
## Time Taken
3:57 including code and documentation 
