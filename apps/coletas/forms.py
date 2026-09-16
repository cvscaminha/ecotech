from apps.form_helpers import mark_required_fields
from django import forms
from django.db.models import Q
from .models import CollectionRequest, DestinationRecord
from apps.residuos.models import ElectronicWaste
from apps.accounts.models import User

class CollectionRequestForm(forms.ModelForm):
    wastes=forms.ModelMultipleChoiceField(queryset=ElectronicWaste.objects.none(),widget=forms.SelectMultiple(attrs={'class':'form-select'}),label='Resíduos para coleta')
    class Meta:
        model=CollectionRequest
        fields=['wastes','cep','address','number','neighborhood','city','latitude','longitude','preferred_date','period','notes']
        widgets={'preferred_date':forms.DateInput(attrs={'type':'date'}),'notes':forms.Textarea(attrs={'rows':3}),'cep':forms.TextInput(attrs={'placeholder':'00000-000'}),'latitude':forms.HiddenInput(),'longitude':forms.HiddenInput()}
    def __init__(self,*args,user=None,**kwargs):
        super().__init__(*args,**kwargs)
        active=[CollectionRequest.Status.REQUESTED,CollectionRequest.Status.ANALYSIS,CollectionRequest.Status.APPROVED,CollectionRequest.Status.SCHEDULED,CollectionRequest.Status.IN_PROGRESS]
        if user:
            self.fields['wastes'].queryset=ElectronicWaste.objects.filter(user=user,collected=False).exclude(collection_requests__status__in=active).distinct()
            self.fields['address'].initial=user.address
            self.fields['city'].initial=user.city
        for name,field in self.fields.items():
            if name!='wastes': field.widget.attrs.setdefault('class','form-control')
        self.fields['period'].widget.attrs['class']='form-select'
        mark_required_fields(self)

    def clean_wastes(self):
        wastes=self.cleaned_data.get('wastes')
        if not wastes:
            raise forms.ValidationError('Selecione pelo menos um resíduo.')
        return wastes

class StatusUpdateForm(forms.ModelForm):
    class Meta: model=CollectionRequest; fields=['status','responsible','notes']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['status'].widget.attrs['class']='form-select'; self.fields['responsible'].queryset=User.objects.filter(user_type=User.UserType.COLLECTION_TEAM, approved=True, is_active=True)
        self.fields['responsible'].label='Responsável pela coleta'
        self.fields['responsible'].widget.attrs['class']='form-select'; self.fields['notes'].widget.attrs['class']='form-control'; mark_required_fields(self)

class DestinationForm(forms.ModelForm):
    class Meta:
        model=DestinationRecord
        fields=['destination','destination_date','notes']
        widgets={'destination_date':forms.DateInput(attrs={'type':'date'}),'notes':forms.Textarea(attrs={'rows':3})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['notes'].label = 'Anotações'
        for f in self.fields.values(): f.widget.attrs.setdefault('class','form-control')
        mark_required_fields(self)
