from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum

from cash_flow.api.transaction_manager import TransactionManager
from cash_flow.api import AccountManager
from cash_flow.models import Category, Tag, Transaction

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

def stock(request):
    # search = request.GET.get('q', '')

    # products = Product.objects.all().order_by('-stock_quantity')

    # if search:
    #     products = products.filter(name__icontains=search)

    # paginator = Paginator(products, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'stock.html', {
        'stock': []
    })

def add_transaction(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    accounts = AccountManager(request.user.id).queryset

    if request.method == 'POST':
        tm = TransactionManager(request.user)
        try:
            if request.POST.get('recurring'):
                # Recurring transaction
                data = {
                    'bank_account': accounts.get(id=request.POST.get('account')),
                    'category': Category.objects.get(id=request.POST.get('rec_category')),
                    'description': request.POST.get('rec_description'),
                    'type': request.POST.get('rec_type'),
                    'amount': float(request.POST.get('rec_amount')),
                    'date': request.POST.get('start_date'),
                    'status': 'PLANNED',
                    # Add other recurring fields as needed
                }
                tm.create_transactions([data])
                messages.success(request, "Recorrente adicionada com sucesso!")
            else:
                # Normal transaction
                data = {
                    'bank_account': accounts.get(id=request.POST.get('account')),
                    'category': categories.get(id=request.POST.get('category')),
                    'description': request.POST.get('description'),
                    'type': request.POST.get('type'),
                    'amount': float(request.POST.get('amount')),
                    'date': request.POST.get('date'),
                    'status': request.POST.get('status'),
                    # Add tags if needed
                }
                tm.create_transactions([data])
                messages.success(request, "Transação adicionada com sucesso!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro ao adicionar: {e}")

    return render(request, 'transaction_form.html', {
        'accounts': accounts,
        'categories': categories,
        'tags': tags,
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