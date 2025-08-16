from django.contrib import admin
from .models import (
    User,
    Currency,
    BankAccount,
    CreditCard,
    CreditCardInvoice,
    Category,
    Tag,
    Transaction,
    RecurringTransaction,
)

admin.site.register(User)
admin.site.register(Currency)
admin.site.register(BankAccount)
admin.site.register(CreditCard)
admin.site.register(CreditCardInvoice)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(RecurringTransaction)