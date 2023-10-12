import django.forms as forms
from .models import users, mobiles, ipads, cart, orders

class deviceForm(forms.ModelForm):
    class Meta:
        model = mobiles
        fields = ['name', 'image', 'price', 'description', 'category']