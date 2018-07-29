from decimal import Decimal
from forex_python.converter import CurrencyRates, RatesNotAvailableError


def convertecurrencyrates(base, to, amount=1):
    currencyRates = CurrencyRates(force_decimal=True)
    try:
        base = base.upper()
        to = to.upper()
        rates = currencyRates.convert(base, to, Decimal(amount))
        return str(amount) + " " + base + " = " + str(rates) + " " + to
    except RatesNotAvailableError:
        return "Error! the rates data are not available."
    except AttributeError:
        return "Please use the right format."


if __name__ == "__main__":
    print(convertecurrencyrates(10, 20, 20))
