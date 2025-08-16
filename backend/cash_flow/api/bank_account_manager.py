from django.shortcuts import get_object_or_404
from ..models import Transaction, BankAccount
from django.db.models import Sum

class AccountManager:
    queryset = BankAccount.objects.all()

    def __init__(self, user=None):
        self.user = user
        self.queryset = self.queryset.filter(user=user) if user else self.queryset

    @classmethod
    def get_account_balance(cls, account_id):
        """
        Retrieve the balance of a specific bank account by its ID.
        """
        account = get_object_or_404(BankAccount, id=account_id)
        transactions = Transaction.objects.filter(bank_account=account)
        balance = transactions.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return balance

    def list_accounts(self):
        """
        List all bank accounts with their balances.
        """
        accounts = self.queryset.prefetch_related('transactions')
        account_balances = {account.id: self.get_account_balance(account.id) for account in accounts}
        return account_balances
    
    def create_account(self, name, bank_name=None, initial_balance=0, currency=None):
        """
        Create a new bank account for a user.
        Parameters:
        - user: User instance to whom the account belongs.
        - name: Name of the bank account.
        - bank_name: Optional name of the bank.
        - initial_balance: Initial balance of the account, default is 0.
        - currency: Currency instance for the account, can be null.
        """
        account = self.queryset.filter(name=name).first()
        if account:
            return account
        account = BankAccount.objects.create(
            user=self.user,
            name=name,
            bank_name=bank_name,
            balance_initial=initial_balance,
            currency=currency
        )
        return account