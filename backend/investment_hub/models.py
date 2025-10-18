from django.db import models

# Create your models here.
import datetime 
from time import time
from enum import Enum

class Instrument(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class IntrumentPrice(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField()
    price = models.FloatField()

    class Meta:
        unique_together = ("instrument", "date")

    def __str__(self):
        return f"{self.instrument.name} - {self.date}: {self.price}"


class Record(models.Model):
    date = models.DateField()
    unit_price = models.FloatField()
    quantity = models.FloatField()
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.instrument.name} - {self.date}: {self.quantity} units at {self.unit_price} each"

    def value(self) -> float:
        return self.unit_price * self.quantity


class Portfolio(models.Model):
    date = models.DateField()
    # def __init__(self, portfolios = []):
    #     self.fill_portfolios(portfolios)
    #     self.value = self.total_value()
    #     self.incomings = self.total_incomings()
    #     self.expenses = self.total_expenses()

    def fill_portfolios(self, portfolios):
        for portfolio in portfolios:
            if not isinstance(portfolio, (Record, Portfolio)):
                raise ValueError("Portfolio must be InvestmentRecord or InvestmentPortfolio instances")
            if isinstance(portfolio, Record):
                self.records.update(portfolio)
            elif isinstance(portfolio, Portfolio):
                self.records.update(portfolio.records)

    def total_value(self) -> float:
        return sum(record.value() for record in self.records.values())

    def total_incomings(self) -> float:
        return sum(0 for record in self.records.values())

    def total_expenses(self) -> float:
        return sum(0 for record in self.records.values())
    
    def summary(self) -> str:
        msgs = [f"{inst.value}: {rec.quantity} units at ${rec.unit_price} each" for inst, rec in self.records.items()]
        return f"Portfolio as of {self.date}: Total Value = {self.value} and Rentability = {self.rentability}%" + "\n\t" + "\n\t".join(msgs)

    def calculate_rentability(self, start_date: datetime.date = None) -> float:
        """This method calculates the profit and loss (PnL) for the portfolio, considering assets held."""
        start_date_records = self.get_records_by_start_date(start_date=start_date)
        start_portfolio = Portfolio(start_date_records, date=start_date) if start_date_records else None
        if not start_portfolio:
            return 0.0
        for i, record in self.records.items():
            # if isinstance(record, InvestmentPortfolio) and i in start_portfolio.records:
            start_record = start_portfolio.records.get(i)
        self.rentability = self.value - start_portfolio.value
        return self.rentability, (self.rentability / start_portfolio.value) if start_portfolio and start_portfolio.value != 0 else 0
    
    def get_records_by_start_date(self, start_date: datetime.date = datetime.date(2023, 1, 1)) -> dict:
        # mocked data - replace with actual data retrieval logic
        records = [Record(start_date, 100.0, 2, instrument=Instrument.STOCK), Record(start_date, 100.0, 3, instrument=Instrument.BOND),Record(date(2023, 2, 15), 500.0, 5, instrument=Instrument.STOCK)]

        filtered_records = [r for r in records if r.instrument in self.records]
        return filtered_records

class PortfolioRecord(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="records")
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="portfolios")
    class Meta:
        unique_together = ("portfolio", "record")