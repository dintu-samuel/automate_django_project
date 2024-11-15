from django.contrib import admin
from .models import stock, StockData

# Register your models here.


class StockAdmin(admin.ModelAdmin):
    
    search_fields =('id','name','symbol')

admin.site.register(stock, StockAdmin)
admin.site.register(StockData)
