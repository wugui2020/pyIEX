import json
import re
import requests

from func_utils import ensure_params_under_instance_context

VARIABLE_CHECK = re.compile('{([A-Z0-9a-z])+}')
API_URL = 'https://api.iextrading.com'

class API(object):

    def __init__(self, api_name, *args):
        """
        route path is the route for the desired API endpoint
        for variables in path, simply wrap that string with '{}'

        Examples:
        ['1.0', 'stock', 'aapl', 'company'] => https://api.iextrading.com/1.0/stock/aapl/company
        ['1.0', 'stock', '<symbol>', 'company'] => https://api.iextrading.com/1.0/stock/{symbol}/company

        The variables will be required parameters for the call function.
        """
        self._route_path = [API_URL] + list(args)
        self._variables = [arg[1:-1] for arg in args if VARIABLE_CHECK.match(arg)]
        self._api_name = api_name

    def call(self, *args, **kwargs):
        params_dict = {self._variables[i]: arg for (i, arg) in enumerate(args)}
        remaining_args = self._variables[len(args):]
        for arg in remaining_args:
            if arg not in kwargs:
                raise ValueError('Missing argument {} for API {}'.format(arg, self._api_name))
            params_dict[arg] = kwargs[arg]

        url = "/".join(self._route_path)
        url = url.format(**params_dict)

        response = requests.get(url)

        if response.status_code != 200:
            message = [response.text, 'API Call Error for url:', url]
            raise ValueError("\n".join(message))
        return response.json()

if __name__ == '__main__':
    stock_api = API('Stock', '1.0', 'stock', '{symbol}', 'company')
    result = stock_api.call(symbol='aapl')
    print(result)
    result = stock_api.call(symbol='aaapl')
    print(result)
