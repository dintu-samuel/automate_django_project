from django.db import models

# Create your models here.

class stock(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=50)
    sector = models.CharField(max_length=100, null=True, blank=True )
    exchange = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class StockData(models.Model):
    stock = models.ForeignKey(stock, on_delete=models.CASCADE)
    current_price = models.CharField(max_length=25, null=True, blank=True)
    price_changed = models.CharField(max_length=25, null=True, blank=True)
    percentage_changed = models.CharField(max_length=25, null=True, blank=True)
    previous_close = models.CharField(max_length=25, null=True, blank=True)
    week_52_high = models.CharField(max_length=25, null=True, blank=True)
    week_52_low = models.CharField(max_length=25, null=True, blank=True)
    market_cap = models.CharField(max_length=25, null=True, blank=True)
    pe_ratio = models.CharField(max_length=25, null=True, blank=True)
    dividend_yeild = models.CharField(max_length=25, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.stock} - {self.current_price}"
    