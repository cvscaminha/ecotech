from apps.form_helpers import mark_required_fields
from django import forms
from .models import DropoffPoint

class DropoffPointForm(forms.ModelForm):
    class Meta:
        model=DropoffPoint
        fields=['name','cep','address','number','neighborhood','phone','latitude','longitude','opening_hours','responsible','active']
        widgets={
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'active': forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if name not in ['latitude','longitude','active']:
                field.widget.attrs.setdefault('class','form-control')
        self.fields['phone'].widget.attrs.update({'placeholder':'(XX) 9XXXX-XXXX'})
        self.fields['cep'].widget.attrs.update({'placeholder':'00000-000'})
        mark_required_fields(self)
