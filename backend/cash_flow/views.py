from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum

from cash_flow.api.transaction_manager import TransactionManager
from cash_flow.api import AccountManager
from cash_flow.models import Category, Transaction

from datetime import datetime, date
import calendar

# from .models import Customer, Order, OrderItem, Product

def home(request):
    search = request.GET.get('q', '')

    accounts = AccountManager(request.user.id).list_accounts()  # Prevent linter error, should be imported if used
    transactions = Transaction.objects.all().order_by('-date')

    if search:
        transactions = transactions.filter(category__name__icontains=search) | transactions.filter(bank_account__name__icontains=search)

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    amount = 0
    for account in accounts.values():
        amount += account['balance'] or 0

    return render(request, 'home.html', {
        'transactions': page_obj,
        'accounts': accounts,
        'total_accounts': amount,
        'user': request.user,
    })

def invoices(request):
    month_param = request.GET.get('month')
    year_param = request.GET.get('year')
    credit_card_param = request.GET.get('credit_card')

    transactions = Transaction.objects.all()

    # Filter by month (accepts "YYYY-MM", "MM-YYYY", or "MM" with optional "year" param)
    if month_param:
        try:
            if '-' in month_param:
                a, b = month_param.split('-', 1)
                if len(a) == 4:
                    year = int(a); month = int(b)
                else:
                    year = int(b); month = int(a)
            else:
                month = int(month_param)
                year = int(year_param) if year_param else datetime.now().year

            start_date = date(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)

            date_field = Transaction._meta.get_field('date')
            if date_field.get_internal_type() == 'DateTimeField':
                start_dt = datetime(year, month, 1)
                if month == 12:
                    next_month_start = datetime(year + 1, 1, 1)
                else:
                    next_month_start = datetime(year, month + 1, 1)
                transactions = transactions.filter(date__gte=start_dt, date__lt=next_month_start)
            else:
                transactions = transactions.filter(date__range=(start_date, end_date))
        except Exception as e:
            messages.error(request, f"Invalid month/year parameters: {e}")

    # If credit_card param is truthy, filter to only credit-card accounts (tries common field names)
    if credit_card_param and credit_card_param.lower() in ('1', 'true', 'yes', 'y'):
        try:
            bank_rel_model = Transaction._meta.get_field('bank_account').related_model
            bank_field_names = {f.name for f in bank_rel_model._meta.fields}
            if 'is_credit_card' in bank_field_names:
                transactions = transactions.filter(bank_account__is_credit_card=True)
            elif 'credit_card' in bank_field_names:
                transactions = transactions.filter(bank_account__credit_card=True)
            elif 'type' in bank_field_names:
                transactions = transactions.filter(bank_account__type='credit_card')
            # else: no known credit-card marker on account model, skip filtering
        except Exception:
            # If anything goes wrong inspecting related model, skip the credit-card filter silently
            pass

    transactions = transactions.order_by('-date')

    return render(request, 'invoices.html', {
        'invoices': []
    })

def add_transaction(request):
    categories = Category.objects.all()
    accounts = AccountManager(request.user.id).queryset

    if request.method == 'POST':
        tm = TransactionManager(request.user)
        try:
            data = {
                    'bank_account': accounts.get(id=request.POST.get('account')),
                    'category': categories.get(id=request.POST.get('category')),
                    'description': request.POST.get('description'),
                    'type': request.POST.get('type'),
                    'amount': float(request.POST.get('amount')),
                    'date': request.POST.get('date'),
                    'status': request.POST.get('status'),
            }
            if request.POST.get('recurring'):
                data['frequence'] = request.POST.get('frequence')
                data['end_date'] = request.POST.get('end_date')
                tm.create_recurrent_transactions([data])
            else:                
                tm.create_transactions([data])
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro ao adicionar: {e}")

    return render(request, 'transaction_form.html', {
        'accounts': accounts,
        'categories': categories,
    })

def add_product(request):
    # if request.method == "POST":
    #     name = request.POST.get("name")
    #     description = request.POST.get("description", "")
    #     sale_price = request.POST.get("sale_price")
    #     cost_price = request.POST.get("cost_price")
    #     stock_quantity = request.POST.get("stock_quantity")
    #     category_id = request.POST.get("category")  # pode ser "" se vazio
    #     supplier_id = request.POST.get("supplier")  # pode ser "" se vazio

    #     # Criar e salvar o produto
    #     Product.objects.create(
    #         name=name,
    #         description=description,
    #         sale_price=sale_price,
    #         cost_price=cost_price,
    #         stock_quantity=stock_quantity,
    #     )
    #     return redirect("stock")
    return render(request, "product_form.html")

def update_transaction(request, transaction_id):
    return home(request)

def delete_transaction(request, transaction_id):
    return home(request)

def update_stock(request, product_id):
    return stock(request)