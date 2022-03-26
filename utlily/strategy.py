from finta import TA

class indicators:
    
    def __init__(self, data) -> None:
        self.close = data.get('Close')
        self.open = data.get('Open')
        self.high = data.get('High')

    def ema(self):
        return TA.EMA(self.close, period=15)
