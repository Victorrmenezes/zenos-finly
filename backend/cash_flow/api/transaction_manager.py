from django.shortcuts import get_object_or_404

from cash_flow.api.bank_account_manager import AccountManager
from ..models import CreditCard, Transaction, BankAccount, RecurringTransaction

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
        required_fields = ['amount', 'date']
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Missing required field: {field}")
        if data['date'] is None:
            raise ValueError("Date cannot be null")
        if data['type'] not in dict(Transaction.TYPE_CHOICES):
            raise ValueError(f"Invalid transaction type: {data['type']}")
        if not data.get('bank_account') and not data.get('credit_card'):
            raise ValueError("Either bank_account or credit_card must be provided")

        data['bank_account'], data['credit_card'] = self.account_manager.resolve_account_and_card(
            bank_account=data.get('bank_account'),
            credit_card=data.get('credit_card'))

    def create_recurrent_transactions(self, recurring_data):
        """
        Create recurring transactions based on the provided data.
        This method should handle the logic for creating multiple transactions
        based on a recurring schedule.
        Example:
        recurring_data = {
            'bank_account': bank_account_instance,
            'category': category_instance,
            'description': 'Monthly Subscription',
            'type': 'EXPENSE',
            'amount': 50.00,
            'start_date': '2023-10-01',
            'frequency': 'MONTHLY',  # or 'WEEKLY', etc.
            'end_date': '2024-10-01'  # Optional
        }
        """
        rec_transactions = []
        for rec_data in recurring_data:
            self.pre_create_validation(rec_data)
            # Create a RecurringTransaction instance
            recurring_transaction = RecurringTransaction(**rec_data)
            rec_transactions.append(recurring_transaction)
        try:
            RecurringTransaction.objects.bulk_create(rec_transactions)
        except(Exception) as e:
            raise ValueError(f"Error creating recurring transactions: {e}")
        return rec_transactions

