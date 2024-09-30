import requests
from langchain.tools import BaseTool
from pydantic import Field
from typing import Literal

class FinancialIndicatorsTool(BaseTool):
    name: Literal["Financial Indicators Tool"] = Field("Financial Indicators Tool")
    description: Literal["Get key financial indicators for a given ticker symbol"] = Field("Get key financial indicators for a given ticker symbol")
    api_key: str
    base_url: str = Field("https://www.alphavantage.co/query")

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _run(self, ticker: str) -> str:
        indicators = {}

        # Fetching different financial indicators
        functions = {
            "OVERVIEW": "Company Overview",
            "TIME_SERIES_DAILY": "Daily Time Series",
            "EARNINGS": "Earnings",
            "BALANCE_SHEET": "Balance Sheet",
            "INCOME_STATEMENT": "Income Statement",
            "CASH_FLOW": "Cash Flow"
        }

        for function, description in functions.items():
            params = {
                "function": function,
                "symbol": ticker,
                "apikey": self.api_key
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()

            # Debugging information
            print(f"API Response for {description}:", data)

            if function == "OVERVIEW":
                indicators.update({
                    "P/E Ratio": data.get("PERatio"),
                    "EPS": data.get("EPS"),
                    "Debt-to-Equity": data.get("DebtEquityRatio"),
                    "Current Ratio": data.get("CurrentRatio"),
                    "ROE": data.get("ReturnOnEquityTTM"),
                    "Profit Margin": data.get("ProfitMargin")
                })
            elif function == "TIME_SERIES_DAILY":
                time_series = data.get("Time Series (Daily)", {})
                if time_series:
                    latest_date = sorted(time_series.keys())[0]
                    latest_data = time_series[latest_date]
                    indicators.update({
                        "Short-term MA": latest_data.get("4. close"),  # Placeholder for actual calculation
                        "Long-term MA": latest_data.get("4. close"),  # Placeholder for actual calculation
                        "Average Volume": latest_data.get("5. volume"),  # Placeholder for actual calculation
                        "Current Volume": latest_data.get("5. volume")
                    })
            elif function == "EARNINGS":
                earnings = data.get("quarterlyEarnings", [])
                if earnings:
                    indicators["EPS"] = earnings[0].get("reportedEPS")
            elif function == "BALANCE_SHEET":
                balance_sheet = data.get("quarterlyReports", [])
                if balance_sheet:
                    total_liabilities = balance_sheet[0].get("totalLiabilities")
                    total_shareholder_equity = balance_sheet[0].get("totalShareholderEquity")
                    if total_liabilities and total_shareholder_equity:
                        indicators["Debt-to-Equity"] = int(total_liabilities) / int(total_shareholder_equity)
            elif function == "INCOME_STATEMENT":
                income_statement = data.get("quarterlyReports", [])
                if income_statement:
                    gross_profit = income_statement[0].get("grossProfit")
                    total_revenue = income_statement[0].get("totalRevenue")
                    if gross_profit and total_revenue:
                        indicators["Profit Margin"] = int(gross_profit) / int(total_revenue)
            elif function == "CASH_FLOW":
                cash_flow = data.get("quarterlyReports", [])
                if cash_flow:
                    total_current_assets = cash_flow[0].get("totalCurrentAssets")
                    total_current_liabilities = cash_flow[0].get("totalCurrentLiabilities")
                    if total_current_assets and total_current_liabilities:
                        indicators["Current Ratio"] = int(total_current_assets) / int(total_current_liabilities)

        return indicators
        
        # return f"""
        # Financial indicators for {ticker}:
        # P/E Ratio: {indicators.get("P/E Ratio")}
        # EPS: {indicators.get("EPS")}
        # Debt-to-Equity: {indicators.get("Debt-to-Equity")}
        # Current Ratio: {indicators.get("Current Ratio")}
        # ROE: {indicators.get("ROE")}
        # Short-term MA: {indicators.get("Short-term MA")}
        # Long-term MA: {indicators.get("Long-term MA")}
        # Average Volume: {indicators.get("Average Volume")}
        # Current Volume: {indicators.get("Current Volume")}
        # RSI: {indicators.get("RSI", "N/A")}  # Placeholder for actual calculation
        # Profit Margin: {indicators.get("Profit Margin")}
        # """

# Example usage
if __name__ == "__main__":
    api_key = "IKPRCH1Z25YCA2SP"
    tool = FinancialIndicatorsTool(api_key=api_key)
    print(tool._run("IBM"))  # Example ticker for Reliance Industries on BSE