from django.shortcuts import get_object_or_404

from backend.cash_flow.api import AccountManager
from ..models import Transaction, BankAccount

class TransactionManager:
    queryset = Transaction.objects.all()

    def __init__(self, user):
        self.user = user
        self.queryset = self.queryset.filter(bank_account__user=user)
        self.account_manager = AccountManager(self.user)

    def create_transactions(self, transactions_data):
        """
        Create multiple transactions from a list of dictionaries.
        Each dictionary should contain the fields required to create a Transaction instance.
        Example:
        transactions_data = [
            {
                'bank_account': bank_account_instance,
                'invoice': invoice_instance or None,
                'category': category_instance or None,
                'description': 'Transaction 1' or None,
                'type': 'INCOME',
                'amount': 100.00,
                'date': '2023-10-01',
                'status': 'PLANNED',
            },
            {
                'bank_account': bank_account_instance,
                'invoice': invoice_instance or None,
                'category': category_instance or None,
                'description': 'Transaction 2' or None,
                'type': 'EXPENSE',
                'amount': 50.00,
                'date': '2023-10-02',
                'status': 'CONFIRMED',
            }
        ]
        """
        transactions = []
        for data in transactions_data:
            self.pre_create_validation(data)
            # Ensure all required fields are present
            transaction = Transaction(**data)
            transactions.append(transaction)
        with transaction.atomic():
            Transaction.objects.bulk_create(transactions)
        return transactions
    
    def update_transactions(self, transaction_data):
        """
        Update a transaction with the given ID using the provided data.
        The data should be a dictionary containing the fields to update.
        Example:
        transaction_data = [{
            'transaction_id': 1,
            'description': 'Updated Transaction',
            'amount': 120.00,
            'status': 'CONFIRMED',
        }]
        """
        transactions = []
        transaction_ids = [transaction.pop('transaction_id') for transaction in transaction_data]
        transactions_qs = self.queryset.filter(id__in=transaction_ids).first()
        for transaction in transactions_qs:
            for key, value in transaction_data.items():
                if key in Transaction._meta.fields and value is not None:
                    setattr(transaction, key, value)
                else:
                    raise ValueError(f"Invalid field: {key}")
            transactions.append(transaction)

        with transaction.atomic():
            Transaction.objects.bulk_update(transactions, fields=transaction_data.keys())
        return transactions
    
    def delete_transactions(self, transaction_ids):
        """
        Delete multiple transactions by their IDs.
        Example:
        transaction_ids = [1, 2, 3]
        """
        transactions = Transaction.objects.filter(id__in=transaction_ids)
        deleted_count, _ = transactions.delete()
        return deleted_count
    def pre_create_validation(self, data):
        """
        Validate the data before creating a transaction.
        This method can be overridden to add custom validation logic.
        """
        required_fields = ['bank_account', 'amount', 'date', 'type']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Missing required field: {field}")
        if data['amount'] <= 0:
            raise ValueError("Amount must be greater than zero")
        if data['date'] is None:
            raise ValueError("Date cannot be null")
        if data['type'] not in dict(Transaction.TYPE_CHOICES):
            raise ValueError(f"Invalid transaction type: {data['type']}")
        if not isinstance(data['bank_account'],BankAccount):
            if isinstance(data['bank_account'], int):
                # If bank_account is an ID, fetch the BankAccount instance
                data['bank_account'] = get_object_or_404(BankAccount, id=data['bank_account'])
            elif isinstance(data['bank_account'], str):
                # If bank_account is a string, assume it is the name and create a new account
                data['bank_account'] = self.account_manager.create_account(
                    name=data['bank_account']
                )
            elif isinstance(data['bank_account'], dict):
                # If bank_account is a dict, assume it contains the ID
                if 'id' in data['bank_account']:
                    data['bank_account'] = get_object_or_404(BankAccount, id=data['bank_account']['id'])
                else:
                    self.account_manager.create_account(
                        name=data['bank_account']['name'],
                        bank_name=data['bank_account'].get('bank_name'),
                        initial_balance=data['bank_account'].get('initial_balance', 0),
                        currency=data['bank_account'].get('currency')
                    )
            data['bank_account'] = data['bank_account'].id