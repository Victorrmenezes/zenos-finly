from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from cash_flow.api.transaction_manager import TransactionManager
from cash_flow.api import AccountManager
from cash_flow.models import Category, Transaction

from datetime import datetime

def home(request):
    search = request.GET.get('q', '')

    accounts = AccountManager(request.user.id).list_accounts()  # Prevent linter error, should be imported if used
    transactions = Transaction.objects.filter(bank_account_id__in=accounts.keys()).order_by('-date')

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
    date = datetime.fromisoformat(request.GET.get('date')) if request.GET.get('date') else datetime.now()
    filter = {
        'date__year': date.year,
        'date__month': date.month,
    }
    if request.GET.get('credit_card'):
        filter['credit_card'] = request.GET.get('credit_card')

    transactions = Transaction.objects.filter(**filter)

    transactions = transactions.order_by('-date')

    return render(request, 'invoices.html', {
        'invoices': []
    })

def add_transaction(request):
    categories = Category.objects.all()
    account_manager = AccountManager(request.user.id)
    accounts = account_manager.queryset
    credit_cards = account_manager.get_credit_cards()

    if request.method == 'POST':
        tm = TransactionManager(request.user)
        try:
            data = {
                    'bank_account': accounts.get(id=request.POST.get('account')),
                    'category': categories.get(id=request.POST.get('category')),
                    'credit_card': credit_cards.get(id=request.POST.get('credit_card',None)),
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
        'credit_cards': credit_cards,
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