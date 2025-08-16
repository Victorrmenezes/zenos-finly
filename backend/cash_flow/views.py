from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

# from .models import Customer, Order, OrderItem, Product

def home(request):
    # search = request.GET.get('q', '')

    # orders = Order.objects.all().order_by('-created_at')

    # if search:
    #     orders = orders.filter(cliente__icontains=search) | orders.filter(produto__icontains=search)

    # paginator = Paginator(orders, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'orders': []
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

def add_order(request):
    # customers = Customer.objects.all()
    # products = Product.objects.all()

    # if request.method == 'POST':
    #     customer_id = request.POST.get('customer')  # pode ser vazio
    #     customer = Customer.objects.filter(id=customer_id).first() if customer_id else None

    #     # Os dados dos itens virão como listas
    #     produtos_ids = request.POST.getlist('product')
    #     quantidades = request.POST.getlist('quantity')
    #     unit_prices = request.POST.getlist('unit_price')
    #     descontos = request.POST.getlist('discount')

    #     if not produtos_ids or len(produtos_ids) == 0:
    #         messages.error(request, "Adicione ao menos um item no pedido.")
    #         return render(request, 'adicionar_pedido.html', {'customers': customers, 'products': products})

    #     # Validar itens
    #     itens = []
    #     total_value = 0
    #     for i in range(len(produtos_ids)):
    #         try:
    #             product = Product.objects.get(id=produtos_ids[i])
    #             quantity = int(quantidades[i])
    #             unit_price = float(unit_prices[i])
    #             discount = float(descontos[i])
    #         except (Product.DoesNotExist, ValueError):
    #             messages.error(request, "Dados inválidos no item do pedido.")
    #             return render(request, 'adicionar_pedido.html', {'customers': customers, 'products': products})

    #         if quantity <= 0 or unit_price < 0 or discount < 0:
    #             messages.error(request, "Quantidade, preço e desconto devem ser valores positivos.")
    #             return render(request, 'adicionar_pedido.html', {'customers': customers, 'products': products})

    #         line_total = quantity * unit_price - discount
    #         if line_total < 0:
    #             messages.error(request, "Desconto não pode ser maior que o total do item.")
    #             return render(request, 'adicionar_pedido.html', {'customers': customers, 'products': products})

    #         total_value += line_total
    #         itens.append({
    #             'product': product,
    #             'quantity': quantity,
    #             'unit_price': unit_price,
    #             'discount': discount,
    #         })

    #     # Tudo validado: salvar pedido e itens atomicalmente
    #     try:
    #         with transaction.atomic():
    #             order = Order.objects.create(
    #                 customer=customer,
    #                 status='OPEN',
    #                 total_value=total_value,
    #             )
    #             for item in itens:
    #                 OrderItem.objects.create(
    #                     order=order,
    #                     product=item['product'],
    #                     quantity=item['quantity'],
    #                     unit_price=item['unit_price'],
    #                     discount=item['discount'],
    #                 )
    #         messages.success(request, f"Pedido #{order.id} criado com sucesso!")
    #         return redirect('listar_pedidos')  # ajuste essa URL conforme seu projeto
    #     except Exception as e:
    #         messages.error(request, f"Erro ao salvar o pedido: {e}")

    return render(request, 'order_form.html', {
        'customers': [],
        'products': [],
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

def update_order(request, order_id):
    return home(request)

def delete_order(request, order_id):
    return home(request)

def update_stock(request, product_id):
    return stock(request)