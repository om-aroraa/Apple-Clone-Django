import django.forms as forms
from .models import mobiles

class deviceForm(forms.ModelForm):
    class Meta:
        model = mobiles
        fields = ['name', 'image', 'price', 'keyfeature']