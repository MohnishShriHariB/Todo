from django.forms import ModelForm
from .models import todo

class todoforms(ModelForm):
    class Meta:
        model=todo
        fields=['Title','List','Important']
        
