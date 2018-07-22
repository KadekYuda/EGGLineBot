from decimal import Decimal
from forex_python.converter import CurrencyRates, RatesNotAvailableError


def convertecurrencyrates(base, to, amount=1):
    currencyRates = CurrencyRates(force_decimal=True)
    try:
        rates = currencyRates.convert(base, to, Decimal(amount))
        print(str(amount) + " " + base + " = " + str(rates) + " " + to)
    except RatesNotAvailableError as e:
        print("Error! the rates data are not available.")

#
# if __name__ == "__main__":
#    convertecurrencyrates("USD", "ZWD", 20)
