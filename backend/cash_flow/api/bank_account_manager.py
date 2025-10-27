from collections import defaultdict
from django.shortcuts import get_object_or_404

from ..helpers import norm_str
from ..models import CreditCard, Transaction, BankAccount

class AccountManager:
    queryset = BankAccount.objects.all()

    def __init__(self, user=None):
        self.user = user
        self.queryset = self.queryset.filter(user=user) if user else self.queryset
        self.get_credit_cards()

    @classmethod
    def get_account_balance(cls, account_id):
        """
        Retrieve the balance of a specific bank account by its ID.
        """
        account = get_object_or_404(BankAccount, id=account_id)
        transactions = Transaction.objects.filter(bank_account=account)
        balance = account.balance_initial
        for transaction in transactions:
            balance += transaction.amount
        # transactions.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return {
                'balance': balance, 
                'name': account.name, 
                'currency': account.currency.symbol if account.currency else None, 
                'bank_name': account.bank_name
                }

    def list_accounts(self):
        """
        List all bank accounts with their balances.
        returns account_balances: dict {account_id: balance}        
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
    
    def create_credit_card(self, name, bank_account):
        """
        Create a new credit card for a user.
        Parameters:
        - name: Name of the credit card.
        - bank_account: BankAccount instance to which the credit card is linked.
        """
        credit_card = self.credit_cards_by_name.get(norm_str(name))
        if credit_card:
            return credit_card
        credit_card = CreditCard.objects.create(
            bank_account=bank_account,
            name=name,
        )
        return credit_card
    
    def get_credit_cards(self):
        """
        Retrieve all credit cards associated with the user's bank accounts.
        """
        self.credit_cards = defaultdict(CreditCard)
        accounts = self.queryset.prefetch_related('credit_cards')
        for account in accounts:
            self.credit_cards.update({cc.id: cc for cc in account.credit_cards.all()})
        self.credit_cards_by_name = {norm_str(cc.name): cc for cc in self.credit_cards.values()}
        return self.credit_cards
    
    def resolve_account_and_card(self, bank_account=None, credit_card=None):
        """
        Resolve and return the BankAccount and CreditCard instances based on the provided inputs.
        Parameters:
        - bank_account: Can be a BankAccount instance, an ID, a name, or a dict with details.
        - credit_card: Can be a CreditCard instance, an ID, a name, or a dict with details.
        Returns:
        - (BankAccount instance, CreditCard instance or None)
        """
        if not isinstance(credit_card, CreditCard):
            if isinstance(credit_card, int):
                # If credit_card is an ID, fetch the BankAccount instance
                credit_card = get_object_or_404(CreditCard, id=credit_card)
            elif isinstance(credit_card, str):
                # If credit_card is a string, assume it is the name and get or create a new account
                credit_card = self.create_credit_card(
                    name=credit_card,
                    bank_account=bank_account
                )
            elif isinstance(credit_card, dict):
                # If credit_card is a dict, assume it contains the ID
                if 'id' in credit_card:
                    credit_card = get_object_or_404(CreditCard, id=credit_card['id'])
                else:
                    self.create_credit_card(
                        name=credit_card['name'],
                        bank_account=credit_card.get('bank_account', bank_account)
                    )
        if credit_card:
            # If credit_card is provided, get its associated bank account
            bank_account = credit_card.bank_account
            return bank_account, credit_card
        
        if not isinstance(bank_account, BankAccount):
            if isinstance(bank_account, int):
                # If bank_account is an ID, fetch the BankAccount instance
                bank_account = get_object_or_404(BankAccount, id=bank_account)
            elif isinstance(bank_account, str):
                # If bank_account is a string, assume it is the name and get or create a new account
                bank_account = self.create_account(
                    name=bank_account
                )
            elif isinstance(bank_account, dict):
                # If bank_account is a dict, assume it contains the ID
                if 'id' in bank_account:
                    bank_account = get_object_or_404(BankAccount, id=bank_account['id'])
                else:
                    self.create_account(
                        name=bank_account['name'],
                        bank_name=bank_account.get('bank_name'),
                        initial_balance=bank_account.get('initial_balance', 0),
                        currency=bank_account.get('currency')
                    )
            bank_account = bank_account
        return bank_account, None