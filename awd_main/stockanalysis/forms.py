from dal import autocomplete
from .models import stock
from django  import forms


class StockForm(forms.Form):
    
    stock = forms.ModelChoiceField(
        queryset=stock.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='stock-autocomplete',
            attrs ={
            
             'data-placeholder': 'Select a Stock....',
            
            } 
        )
    )