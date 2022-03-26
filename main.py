from pprint import pprint
from time import sleep
from binance.spot import Spot
import pandas as pd
import cconfig
from utlily.strategy import indicators



class Bot_binance:

    """
    Bot para binance que permite automatizar las compras y ventas en el mercado spot.

    """
    __api_key = cconfig.API_KEY
    __api_secret_key = cconfig.API_SECRET_KEY
    binance_client = Spot(key=__api_key, secret=__api_secret_key)


    def __init__(self, pair: str, temporality: str ):
        self.pair = pair.upper()
        self.temporality = temporality
        self.symbol = self.pair.removeprefix("USDT")

    def _recuest(self, endpoint: str, parameters: dict =  None):
        while True:
            try:
                response = getattr(self.binance_client, endpoint)
                return response() if parameters is None else response (**parameters)
            except:
                print(f'El endpoint{endpoint} ha fallado.\n Parametros{parameters}\n\n')
                sleep(2)

    
    def binance_account(self) ->dict:
        """
        devuelve las metricas y balance asociados a la cuenta
        """
        return self._recuest('account')

    
    def cryptocurrencies(self) -> list[dict]:
        """
        devuelve una lista de todas las criptomonedas en la cuenta 
        que tengan saldo positivo
        """
        return [crypto for crypto in self.binance_account().get('balances') if float(crypto.get('free'))> 0]


    def symbol_price(self, pair: str = None):
        """
        devuelve el precio de un par determinado.
        """
        symbol = self.pair if pair is None else pair
        return float(self._recuest('ticker_price',{'symbol':symbol.upper()}).get('price'))


    def candlestick(self, limit: int = 50) -> pd.DataFrame:
        """
        devuelve la informacion de las velas.
        """
        pararms = {
           'symbol': self.pair, 
            'interval':self.temporality, 
            'limit': limit
        }

        candlestick = pd.DataFrame(self._recuest(
            'klines',
            pararms
            ),
          
             columns = ['Open time','Open','High','Low','Close','Volume','Close time',
                        'Quote asset volume','Number of trades','Taker buy base asset volume',
                        'Taker buy quote asset volume', 'Ignore'
            ],
            dtype=float
            )

        return candlestick[['Open time','Open','High','Low','Close','Volume']]

bot = Bot_binance("SOLUSDT","4h")
pprint(indicators(bot.candlestick()).ema())