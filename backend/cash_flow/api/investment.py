from datetime import date
from time import time
from typing import List
from enum import Enum

class Instrument(Enum):
    STOCK = "Stock"
    BOND = "Bond"
    REAL_ESTATE = "Real Estate"
    MUTUAL_FUND = "Mutual Fund"
    ETF = "ETF"
    OTHER = "Other"

class InvestmentRecord:
    def __init__(self, date: date, value: float, quantity: float, instrument: Instrument = Instrument.OTHER):
        self.date = date
        self.value = value
        self.instrument = instrument
        self.quantity = quantity


class InvestmentPortfolio(InvestmentRecord):
    rentability: float = 0.0
    incomings: float = 0.0
    expenses: float = 0.0 
    def __init__(self, records: List[InvestmentRecord], date: date = date.today()):
        self.date = date
        self.records = {r.instrument: r for r in records}
        self.value = self.total_value()
        self.incomings = self.total_incomings()
        self.expenses = self.total_expenses()

    def total_value(self) -> float:
        return sum(record.value * record.quantity for record in self.records.values())

    def total_incomings(self) -> float:
        return sum(0 for record in self.records.values())

    def total_expenses(self) -> float:
        return sum(0 for record in self.records.values())
    
    def summary(self) -> str:
        msgs = [f"{inst.value}: {rec.quantity} units at ${rec.value} each" for inst, rec in self.records.items()]
        return f"Portfolio as of {self.date}: Total Value = {self.value} and Rentability = {self.rentability}%" + "\n\t" + "\n\t".join(msgs)

    def calculate_rentability(self, start_date: date = None) -> float:
        """This method calculates the profit and loss (PnL) for the portfolio, considering assets held."""
        start_date_records = self.get_records_by_start_date(start_date=start_date)
        start_portfolio = InvestmentPortfolio(start_date_records, date=start_date) if start_date_records else None
        if not start_portfolio:
            return 0.0
        for i, record in self.records.items():
            # if isinstance(record, InvestmentPortfolio) and i in start_portfolio.records:
            start_record = start_portfolio.records.get(i)
        self.rentability = self.value - start_portfolio.value
        return self.rentability, (self.rentability / start_portfolio.value) if start_portfolio and start_portfolio.value != 0 else 0
    
    def get_records_by_start_date(self, start_date: date = date(2023, 1, 1)) -> dict:
        # mocked data - replace with actual data retrieval logic
        records = [InvestmentRecord(start_date, 100.0, 2, instrument=Instrument.STOCK), InvestmentRecord(start_date, 100.0, 3, instrument=Instrument.BOND),InvestmentRecord(date(2023, 2, 15), 500.0, 5, instrument=Instrument.STOCK)]

        filtered_records = [r for r in records if r.instrument in self.records]
        return filtered_records

def test():
    # Example usage
    a = InvestmentRecord(date(2023, 6, 1), 1000.0, 7, instrument=Instrument.STOCK)
    b = InvestmentRecord(date(2023, 6, 1), 1500.0, 3, instrument=Instrument.BOND)

    portfolios = [InvestmentPortfolio([a]), InvestmentPortfolio([b]) ,InvestmentPortfolio([a,b])]
    for p in portfolios:
        p.calculate_rentability(start_date=date(2023, 1, 1))
        print(p.summary())
    print(InvestmentPortfolio(portfolios).summary())


if __name__ == "__main__":
    test()