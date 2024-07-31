import requests

class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stocks = {}

    def add_stock(self, symbol, shares):
        self.stocks[symbol] = self.stocks.get(symbol, 0) + shares
        print(f"Added {shares} shares of {symbol} to the portfolio.")

    def remove_stock(self, symbol, shares):
        if symbol in self.stocks:
            if self.stocks[symbol] >= shares:
                self.stocks[symbol] -= shares
                print(f"Removed {shares} shares of {symbol} from the portfolio.")
                if self.stocks[symbol] == 0:
                    del self.stocks[symbol]
            else:
                print(f"Not enough shares of {symbol} to remove.")
        else:
            print(f"Stock {symbol} not found in the portfolio.")

    def fetch_stock_price(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        try:
            return float(data["Global Quote"]["05. price"])
        except (KeyError, TypeError, ValueError):
            print(f"Error fetching data for {symbol}.")
            return None

    def view_portfolio(self):
        total_value = 0.0
        print("\nCurrent portfolio:")
        for symbol, shares in self.stocks.items():
            price = self.fetch_stock_price(symbol)
            if price is not None:
                value = shares * price
                total_value += value
                print(f"{symbol}: {shares} shares @ ${price:.2f} each = ${value:.2f}")
            else:
                print(f"Could not fetch price for {symbol}.")
        print(f"Total portfolio value: ${total_value:.2f}")

def main():
    API_KEY = "201P9L0G9EQU54G3"  
    portfolio = StockPortfolio(API_KEY)

    while True:
        print("\nMenu:")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. View portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == "2":
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == "3":
            portfolio.view_portfolio()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
