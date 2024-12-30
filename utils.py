import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Union, Dict

class StockDataAnalyzer:
    """
    A class to analyze stock market data using the yfinance API.
    
    Attributes:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL' for Apple)
        _ticker (yf.Ticker): yfinance Ticker object
    """
    
    def __init__(self, ticker_symbol: str):
        """
        Initialize the StockDataAnalyzer with a ticker symbol.
        
        Args:
            ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL' for Apple)
        """
        self.ticker_symbol = ticker_symbol
        self._ticker = yf.Ticker(ticker_symbol)
    
    @staticmethod
    def _get_default_dates() -> Dict[str, str]:
        """
        Get default start and end dates (1 year period ending today).
        
        Returns:
            Dict[str, str]: Dictionary containing start_date and end_date
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        return {'start_date': start_date, 'end_date': end_date}
    
    def get_stock_data(self, 
                      start_date: Optional[str] = None, 
                      end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch daily stock price data for the ticker symbol.
        
        Args:
            start_date (str, optional): Start date in 'YYYY-MM-DD' format
            end_date (str, optional): End date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: DataFrame containing the stock price data
        """
        dates = self._get_default_dates()
        start_date = start_date or dates['start_date']
        end_date = end_date or dates['end_date']
        
        df = self._ticker.history(start=start_date, end=end_date)
        return df[['Open', 'High', 'Low', 'Close']]
    
    def get_daily_volume(self, 
                        start_date: Optional[str] = None, 
                        end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Retrieve daily trading volume data.
        
        Args:
            start_date (str, optional): Start date in 'YYYY-MM-DD' format
            end_date (str, optional): End date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: DataFrame containing date and volume data
        """
        dates = self._get_default_dates()
        start_date = start_date or dates['start_date']
        end_date = end_date or dates['end_date']
        
        hist = self._ticker.history(start=start_date, end=end_date)
        volume_data = hist[['Volume']].reset_index()
        volume_data.columns = ['Date', 'Volume']
        
        return volume_data
    
    def get_combined_data(self, 
                         start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get combined price and volume data.
        
        Args:
            start_date (str, optional): Start date in 'YYYY-MM-DD' format
            end_date (str, optional): End date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: DataFrame containing combined price and volume data
        """
        price_data = self.get_stock_data(start_date, end_date).reset_index()
        volume_data = self.get_daily_volume(start_date, end_date)
        
        merged_data = pd.merge(price_data, volume_data, on='Date', how='outer')
        return merged_data.sort_values('Date').set_index('Date')

# Example usage:
if __name__ == "__main__":
    analyzer = StockDataAnalyzer('TSLA')
    data = analyzer.get_combined_data('2024-05-01', '2024-12-29')
    print(data.sample(3))