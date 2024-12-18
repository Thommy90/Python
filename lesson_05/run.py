from typing import Any
from functools import wraps

users = [
    {"username": "thommy", "password": "qwerty"}
]

user_cache = None


def auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        global user_cache

        if user_cache:
            print(f"Glad to see you again {user_cache}")
            return func(*args, **kwargs)

        print("Please log in:")
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            for user in users:
                if user["username"] == username and user["password"] == password:
                    user_cache = username
                    print(f"You are logged by {username}")
                    return func(*args, **kwargs)

            print("Incorrect login or password :(. Please try again")

    return inner


class Price:
    conversion_chf_to_currency = {
        "USD": 1.13,
        "UAH": 47.25,
        "GBP": 0.89,
        "EUR": 1.08,
    }

    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def convert(self, to: str) -> "Price":
        if self.currency == to:
            return self
        if self.currency == "CHF":
            if to not in self.conversion_chf_to_currency:
                raise ValueError(f"Currency {self.currency} or {to} not supported :(")
            conversion_rate = self.conversion_chf_to_currency[to]
        elif to == "CHF":
            if self.currency not in self.conversion_chf_to_currency:
                raise ValueError(f"Currency {self.currency} or {to} not supported :(")
            conversion_rate = 1 / self.conversion_chf_to_currency[self.currency]
        else:
            if self.currency not in self.conversion_chf_to_currency or to not in self.conversion_chf_to_currency:
                raise ValueError(f"Currency {self.currency} or {to} not supported :(")
            conversion_rate = self.conversion_chf_to_currency[to] / self.conversion_chf_to_currency[self.currency]

        converted_value = round(self.value * conversion_rate, 2)
        return Price(value=converted_value, currency=to)

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        else:
            if self.currency != other.currency:
                converted_self = self.convert(to="CHF")
                converted_other = other.convert(to="CHF")
                result_in_chf = converted_self.value + converted_other.value
                result_in_self_currency = Price(result_in_chf, "CHF").convert(to=self.currency)

                return result_in_self_currency

        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            return Price(value=self.value + other.value, currency=self.currency)
        else:
            raise ValueError("Currency must be number")

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        else:
            if self.currency != other.currency:
                converted_self = self.convert(to="CHF")
                converted_other = other.convert(to="CHF")
                result_in_chf = converted_self.value - converted_other.value
                result_in_self_currency = Price(result_in_chf, "CHF").convert(to=self.currency)

                return result_in_self_currency

        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            return Price(value=self.value - other.value, currency=self.currency)
        else:
            raise ValueError("Currency must be number")


if __name__ == "__main__":
    #@auth
    def command():
        phone = Price(value=200, currency="EUR")
        tablet = Price(value=400, currency="USD")
        keyboard = Price(value=30, currency="USD")
        total: Price = keyboard + tablet
        print(total)

        total: Price = tablet - keyboard
        print(total)

        print(keyboard + phone)

        print(phone - keyboard)


    command()
    command()
