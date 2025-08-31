from django.shortcuts import render
from .models import Instrument, Record, Portfolio, IntrumentPrice
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    instrument_count = Instrument.objects.count()
    portfolio_count = Portfolio.objects.count()
    record_count = Record.objects.count()
    return render(request, "investment_hub/home.html", {
        "instrument_count": instrument_count,
        "portfolio_count": portfolio_count,
        "record_count": record_count,
    })

# def instrument_list(request):
#     instruments = Instrument.objects.all()
#     return render(request, "investment_hub/instrument_list.html", {
#         "instruments": instruments,
#     })

def portfolio_list(request):
    portfolios = Portfolio.objects.all()
    return render(request, "investment_hub/portfolio_list.html", {
        "portfolios": portfolios,
    })

def record_list(request):
    records = Record.objects.all()
    return render(request, "investment_hub/record_list.html", {
        "records": records,
    })

def instrument_list(request, instrument_id=1):
    instrument = Instrument.objects.get(pk=instrument_id)
    prices = IntrumentPrice.objects.filter(instrument=instrument).order_by('date')
    chart_data = {
        "labels": [price.date.strftime("%Y-%m-%d") for price in prices],
        "prices": [price.price for price in prices],
        "instrument_name": instrument.name,
    }
    return render(request, "investment_hub/instrument_list.html", {
        "chart_data": chart_data,
        "instrument": instrument,
    })