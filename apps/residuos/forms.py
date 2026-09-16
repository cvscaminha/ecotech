from apps.form_helpers import mark_required_fields
from django import forms
from .models import ElectronicWaste, Category

class WasteForm(forms.ModelForm):
    class Meta:
        model = ElectronicWaste
        fields = ['category','equipment','manufacturer','model','serial_number','description','quantity','weight','condition','image','status']
        widgets = {'description': forms.Textarea(attrs={'rows':3, 'maxlength':'500', 'placeholder':'Ex.: Notebook Dell Inspiron com tela quebrada e sem carregador.'}), 'weight': forms.NumberInput(attrs={'step':'0.01','min':'0.01'})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values(): field.widget.attrs.setdefault('class','form-control')
        if 'active' in self.fields:
            self.fields['active'].widget.attrs['class']='form-check-input'
        self.fields['category'].widget.attrs['class']='form-select'
        active_categories = Category.objects.filter(active=True)
        if self.instance and self.instance.pk and self.instance.category_id:
            active_categories = Category.objects.filter(pk=self.instance.category_id) | active_categories
        self.fields['category'].queryset = active_categories.distinct().order_by('name')
        self.fields['category'].label = 'Categoria'
        self.fields['condition'].label = 'Situação'
        self.fields['condition'].widget.attrs['class']='form-select'
        self.fields['status'].label = 'Status'
        self.fields['status'].widget.attrs['class']='form-select'
        mark_required_fields(self)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('A imagem deve ter no máximo 5 MB.')
        return image


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description','active']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            if name == 'active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs.setdefault('class','form-control')
