import requests
import json
import numpy as np
import pandas as pd

class Connection:
    def __init__(self, api_key):
        """
        A class to handle connections to the alphavantage api

        Attributes
        ----------
        api_endpoint : str
            endpoint for api
        api_key : str
            api key 


        Methods
        -------
        get_response(ticker)

        get_series(ticker)

        """
        self.api_endpoint = "https://www.alphavantage.co/query"
        self.api_key = api_key

        return

    # get request response from api for ticker
    def get_response(self, ticker):
        """
        Returns a response from a request for time series data

            Parameters
            ----------
            ticker : str
                A ticker symbol

            Returns
            -------
            response : requests.models.Response
                A request response
        """
        api_params = {'function':'TIME_SERIES_DAILY_ADJUSTED', 'symbol':ticker, 
                   'outputsize':'full', 'apikey':self.api_key}
        response = requests.get(self.api_endpoint, params=api_params)

        return response

    # print request response
    def print_response(self, response):
        json_data = response.json()
        json_text = json.dumps(json_data, indent = 4)
        print(json_text)

    # get series of closing price data for ticker
    def get_series(self, ticker, length):
        """
        Returns the series of price data for a ticker

            Paramters
            ---------
            ticker : str 
                A ticker symbol

            length : int
                The length of the price data from the most 
                recent trading day

            Returns
            -------
            series : (pandas.core.series.Series) 
                A series consisting of the price data 
                for a ticker for the last 20 years if available.
        """

        # get response and json data 
        response = self.get_response(ticker)
        json_data = response.json()

        # get dates and closing prices from json data
        dates = [date for date in json_data['Time Series (Daily)'].keys()]
        prices = [json_data['Time Series (Daily)'][date]['4. close'] for date in dates]

        # assert length is not more than available history
        assert(length <= len(dates))

        # convert date and closing prices to date-index and float types respectively
        date = pd.DatetimeIndex(dates)
        price = np.array(prices, dtype='float64')

        # create pd.Series
        series = pd.Series(data=price, index=date) 

        # cut series to length
        series = series[0:length]

        return series
        
        
    

