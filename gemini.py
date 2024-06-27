from datetime import datetime
import json
import argparse
import requests
import numpy as np


class Gemini:

    def __init__(self, currency: str, deviation: float, log_level: str = "INFO"):
        self.currency = currency
        self.deviation = deviation

        if log_level.upper() in ["DEBUG", "INFO", "ERROR"]:
            self.log_level = log_level.upper()
        else:
            self.log_level = "INFO"

    def gather_symbols(self) -> list[str]:
        response = requests.get("https://api.gemini.com/v1/symbols", timeout="5")
        response.raise_for_status()
        return response.json()

    def ticker_data(self, currency: str) -> dict:
        response = requests.get(f"https://api.gemini.com/v2/ticker/{currency}", timeout="5")
        response.raise_for_status()
        return response.json()

    def analyze_data(self, data: dict) -> dict:

        prices = np.asarray(data["changes"], dtype=np.float64)

        std_deviation = np.std(prices)

        # Calculate mean
        mean_price = np.mean(prices)

        self.log_debug(f"mean price: {mean_price}")

        # Calculate deviation from mean
        deviations = prices - mean_price

        self.log_debug(f"deviations: {deviations}")

        # Calculate absolute value of deviation as notional value 
        price_change_value = np.sum(np.abs(deviations))

        self.log_debug(f"price change value: {price_change_value}")

        return {
            "std_deviation": std_deviation,
            "price_change_value": price_change_value,
        }

    def report_24hr_deviation(self):
        if self.currency == "ALL":
            try:
                currency_list = self.gather_symbols()
            except requests.HTTPError as e:
                self.log_error(e)
        else:
            currency_list = [self.currency]

        for currency in currency_list:
            try:
                data = self.ticker_data(currency)
                deviation_data = self.analyze_data(data)

                self.log_currency(data, deviation_data)
            except requests.HTTPError as e:
                self.log_error(e)

    def log_debug(self, data):
        if self.log_level != "DEBUG":
            return
        output = {
            "timestamp": datetime.now().isoformat(),
            "level": "DEBUG",
            "data": data,
        }
        print(json.dumps(output))

    def log_error(self, e):
        if self.log_level not in ["DEBUG", "INFO", "ERROR"]:
            return
        output = {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "data": {"error": str(e)},
        }
        print(json.dumps(output))

    def log_currency(self, data, deviation_data):

        if self.log_level not in ["DEBUG", "INFO"]:
            return
        output = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "traiding_currency": data["symbol"],
        }

        if self.log_level == "DEBUG":
            pass

        if deviation_data["std_deviation"] >= self.deviation:
            output["deviation"] = True
            data_block = {
                "last_price": data["close"],
                "average": "",
                "sdev": deviation_data["std_deviation"],
                "change": deviation_data["price_change_value"],
            }
            output["data"] = data_block
        else:
            output["deviation"] = False

        print(json.dumps(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--currency",
        default="ALL",
        help="Currency trading currency or ALL (default: ALL)",
    )
    parser.add_argument(
        "-d",
        "--deviation",
        type=float,
        default="1",
        help="Standard deviation threshold (default: 1.0)",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        help="Log level of DEBUG, INFO, or ERROR (default: INFO)",
    )

    args = parser.parse_args()

    gemini_currency_report = Gemini(
        currency=args.currency, deviation=args.deviation, log_level=args.log_level
    )
    gemini_currency_report.report_24hr_deviation()
