from decimal import Decimal
from enum import Enum


class NotEnoughFundsError(Exception):
    ...


class InsufficientStocksError(Exception):
    ...


class AssetPrice(Enum):
    LKOH = Decimal(5896)
    SBER = Decimal(250)


class Portfolio:
    def __init__(self, cash: Decimal):
        self.assets = {asset: 0 for asset in AssetPrice}
        self.cash = cash

    @property
    def balance(self) -> Decimal:
        return self.cash + sum(
            asset.value * quantity for asset, quantity in self.assets.items()
        )


class Trader:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def buy(self, asset: AssetPrice, quantity: int):
        cost = asset.value * quantity
        if cost > self.portfolio.cash:
            raise NotEnoughFundsError(
                f"Not enough funds to buy {quantity} shares of {asset.name}"
            )

        self.portfolio.cash -= cost
        self.portfolio.assets[asset] += quantity

    def sell(self, asset: AssetPrice, quantity: int):
        if (
            asset not in self.portfolio.assets
            or self.portfolio.assets[asset] < quantity
        ):
            raise InsufficientStocksError(
                f"Insufficient shares of {asset.name} to sell or incorrect quantity specified"
            )

        self.portfolio.cash += asset.value * quantity
        self.portfolio.assets[asset] -= quantity
