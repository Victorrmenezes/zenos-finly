from django.contrib import admin
from .models import (
    Instrument,
    IntrumentPrice,
    Record,
    Portfolio,
)

admin.site.register(Instrument)
admin.site.register(IntrumentPrice)
admin.site.register(Record)
admin.site.register(Portfolio)