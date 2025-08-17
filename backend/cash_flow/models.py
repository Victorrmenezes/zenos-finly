from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)
    symbol = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} ({self.symbol})"


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_accounts")
    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    balance_initial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credit_cards")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name="credit_cards")
    name = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=12, decimal_places=2)
    closing_day = models.PositiveSmallIntegerField()  # dia de fechamento da fatura
    due_day = models.PositiveSmallIntegerField()      # dia de vencimento da fatura

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class CreditCardInvoice(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('PAID', 'Paid'),
    ]

    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="invoices")
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("credit_card", "month", "year")

    def __str__(self):
        return f"Invoice {self.month}/{self.year} - {self.credit_card.name}"


class Category(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('TRANSFER', 'Transfer'),
    ]
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)
    invoice = models.ForeignKey(CreditCardInvoice, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="transactions")

    description = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLANNED")

    tags = models.ManyToManyField(Tag, blank=True)

    # Para transferências: vincular duas transações (saida/entrada)
    transfer_id = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.type})"


class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
        ('CUSTOM', 'Custom'),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="recurring_transactions")

    description = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Transaction.TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    next_occurrence = models.DateField()

    def __str__(self):
        return f"{self.description} ({self.frequency})"
