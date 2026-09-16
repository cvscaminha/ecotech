from apps.form_helpers import mark_required_fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from .validators import normalize_document, format_phone, normalize_email

BRAZIL_STATES = [
    ('', 'Selecione o estado'),
    ('AC','Acre'), ('AL','Alagoas'), ('AP','Amapá'), ('AM','Amazonas'),
    ('BA','Bahia'), ('CE','Ceará'), ('DF','Distrito Federal'), ('ES','Espírito Santo'),
    ('GO','Goiás'), ('MA','Maranhão'), ('MT','Mato Grosso'), ('MS','Mato Grosso do Sul'),
    ('MG','Minas Gerais'), ('PA','Pará'), ('PB','Paraíba'), ('PR','Paraná'),
    ('PE','Pernambuco'), ('PI','Piauí'), ('RJ','Rio de Janeiro'), ('RN','Rio Grande do Norte'),
    ('RS','Rio Grande do Sul'), ('RO','Rondônia'), ('RR','Roraima'), ('SC','Santa Catarina'),
    ('SP','São Paulo'), ('SE','Sergipe'), ('TO','Tocantins'),
]

class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                continue
            field.widget.attrs.setdefault('class', 'form-control')

class ContactValidationMixin:
    def clean_email(self):
        try:
            email = normalize_email(self.cleaned_data.get('email'))
        except forms.ValidationError:
            raise forms.ValidationError('Informe um endereço de e-mail válido.')
        qs = User.objects.filter(email__iexact=email)
        if getattr(self, 'instance', None) and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Já existe uma conta com este e-mail.')
        return email

    def clean_cpf_cnpj(self):
        raw = self.cleaned_data.get('cpf_cnpj')
        if not raw:
            raise forms.ValidationError('Este campo é obrigatório.')
        try:
            document = normalize_document(raw)
        except forms.ValidationError:
            raise forms.ValidationError('Informe um CPF ou CNPJ válido.')
        # compara normalizado para também capturar registros antigos com máscara
        for user in User.objects.exclude(pk=getattr(self.instance, 'pk', None)).exclude(cpf_cnpj__isnull=True).only('cpf_cnpj'):
            if ''.join(filter(str.isdigit, user.cpf_cnpj or '')) == document:
                raise forms.ValidationError('Já existe um cadastro com este CPF/CNPJ.')
        return document

    def clean_phone(self):
        try:
            return format_phone(self.cleaned_data.get('phone'))
        except forms.ValidationError as exc:
            raise forms.ValidationError(exc.messages[0])

    def clean_city(self):
        # A cidade é carregada dinamicamente pelo Select via IBGE.
        # Aceita o município enviado pelo navegador após validação básica,
        # evitando conflito entre choices dinâmicas e validação do Django.
        city = (self.cleaned_data.get('city') or '').strip()
        if not city:
            raise forms.ValidationError('Selecione a cidade.')
        return city

class RegistrationForm(ContactValidationMixin, BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone','cpf_cnpj','cep','address','number','neighborhood','state','city','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields['state'] = forms.ChoiceField(choices=BRAZIL_STATES, label='UF')
        self.fields['state'].widget.attrs.update({'class':'form-select','id':'id_state'})
        # Cidade é um <select> dependente da UF. Em POST, inclua o valor enviado
        # nas choices do servidor para que a validação do Django aceite a cidade
        # carregada dinamicamente pelo JavaScript.
        posted_city = (self.data.get('city') or '').strip() if self.is_bound else ''
        city_choices = [('', 'Selecione a cidade')]
        if posted_city:
            city_choices.append((posted_city, posted_city))
        self.fields['city'] = forms.ChoiceField(choices=city_choices, label='Cidade')
        self.fields['city'].widget.attrs.update({'class':'form-select','id':'id_city'})
        for name in self.fields:
            self.fields[name].required = True
        self.fields['phone'].widget.attrs.update({'id':'id_phone','placeholder':'(XX) 9XXXX-XXXX','inputmode':'numeric'})
        self.fields['cpf_cnpj'].widget.attrs.update({'placeholder':'CPF ou CNPJ','inputmode':'numeric','id':'id_cpf_cnpj'})
        self.fields['cep'].widget.attrs.update({'placeholder':'00000-000','inputmode':'numeric','id':'id_cep'})
        self.fields['city'].widget.attrs.update({'id':'id_city'})
        self.fields['state'].widget.attrs.update({'id':'id_state'})
        self.fields['password1'].widget.attrs.update({'id':'id_password1'})
        self.fields['password2'].widget.attrs.update({'id':'id_password2'})
        self.fields['email'].widget.attrs.update({'type':'email','placeholder':'email@exemplo.com'})
        self.fields['username'].label = 'Usuário'
        self.fields['username'].help_text = None
        # O template já acrescenta um único asterisco aos campos obrigatórios.
        # Não use mark_required_fields aqui para evitar "* *" nos labels.
        for field in self.fields.values():
            if isinstance(field.label, str):
                field.label = field.label.rstrip().removesuffix('*').rstrip()

class LoginForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'E-mail ou usuário'
        self.fields['username'].widget.attrs['placeholder'] = 'seuemail@exemplo.com'
        self.fields['password'].widget.attrs['placeholder'] = 'Sua senha'
        self.apply_bootstrap()
    def clean(self):
        login_value = (self.cleaned_data.get('username') or '').strip()
        password = self.cleaned_data.get('password')

        # Resolve e-mail para o username real antes de autenticar.
        user = None
        if login_value:
            if '@' in login_value:
                user = User.objects.filter(email__iexact=login_value).first()
            else:
                user = User.objects.filter(username__iexact=login_value).first()

        if user:
            self.cleaned_data['username'] = user.username

            # O backend padrão do Django rejeita usuários inativos como se as
            # credenciais fossem inválidas. Só exibimos a mensagem específica
            # quando a senha também está correta, evitando revelar contas válidas.
            if not user.is_active and password and user.check_password(password):
                raise forms.ValidationError(
                    'Usuário Bloqueado. Entre em contato com o seu supervisor ou administrador.',
                    code='inactive',
                )

        return super().clean()

class ProfileForm(ContactValidationMixin, BootstrapFormMixin, forms.ModelForm):
    new_password = forms.CharField(
        label='Nova Senha', required=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Deixe em branco para manter a senha atual'})
    )

    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone','cpf_cnpj','cep','address','number','neighborhood','state','city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields['state'] = forms.ChoiceField(choices=BRAZIL_STATES, label='UF')
        self.fields['state'].widget.attrs.update({'class':'form-select','id':'id_state'})
        # Cidade é carregada dinamicamente pelo IBGE.
        # Mantém a cidade atual/recebida no POST entre as choices para evitar
        # validação inválida do Django antes do JavaScript popular o Select.
        current_city = ''
        if self.is_bound:
            current_city = (self.data.get('city') or '').strip()
        elif self.instance and getattr(self.instance, 'city', None):
            current_city = self.instance.city.strip()

        city_choices = [('', 'Selecione a cidade')]
        if current_city:
            city_choices.append((current_city, current_city))

        self.fields['city'] = forms.ChoiceField(choices=city_choices, label='Cidade')
        self.fields['city'].widget.attrs.update({'class':'form-select','id':'id_city'})
        for name in self.fields:
            if name != 'new_password':
                self.fields[name].required = True
        self.fields['email'].widget.attrs.update({'type':'email','placeholder':'email@exemplo.com'})
        self.fields['phone'].widget.attrs.update({'placeholder':'(XX) 9XXXX-XXXX','inputmode':'numeric'})
        self.fields['cpf_cnpj'].widget.attrs.update({'placeholder':'XXX.XXX.XXX-XX','inputmode':'numeric'})
        self.fields['cep'].widget.attrs.update({'placeholder':'XXXXX-XXX','inputmode':'numeric','maxlength':'9'})
        self.fields['number'].widget.attrs.update({'placeholder':'Número'})
        self.fields['neighborhood'].widget.attrs.update({'placeholder':'Bairro'})
        self.fields['state'].widget = forms.Select(choices=BRAZIL_STATES, attrs={'class':'form-control','id':'id_state'})
        # Mantém as opções carregadas pelo formulário. Não substituir o widget
        # após criar o ChoiceField, pois isso descartava a cidade selecionada e
        # fazia o frontend assumir a primeira opção da lista.
        self.fields['city'].widget = forms.Select(
            choices=self.fields['city'].choices,
            attrs={'class':'form-select','id':'id_city'}
        )
        if self.is_bound:
            selected_city = (self.data.get('city') or '').strip()
        else:
            selected_city = getattr(self.instance, 'city', '') or ''
        if selected_city:
            current_choices = list(self.fields['city'].choices)
            if not any(value == selected_city for value, _ in current_choices):
                current_choices.append((selected_city, selected_city))
            self.fields['city'].choices = current_choices
            self.initial['city'] = selected_city

        mark_required_fields(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('new_password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class AdminUserForm(ContactValidationMixin, BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': 'Digite ou gere uma senha',
            'id': 'id_generated_password',
        }),
    )

    class Meta:
        model = User
        fields = [
            'first_name','last_name','username','email','phone','cpf_cnpj',
            'cep','address','number','neighborhood','state','city',
            'user_type','is_active'
        ]
        widgets = {
            'state': forms.Select(choices=BRAZIL_STATES),
            'city': forms.Select(choices=[('', 'Selecione primeiro o estado')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

        required_fields = [
            'first_name','last_name','username','email','phone','cpf_cnpj',
            'cep','address','number','neighborhood','state','city','user_type'
        ]
        for name in required_fields:
            self.fields[name].required = True

        self.fields['username'].label = 'Usuário'
        self.fields['username'].help_text = None
        self.fields['user_type'].label = 'Perfil'
        self.fields['is_active'].label = 'Usuário ativo'
        self.fields['cep'].widget.attrs.update({
            'placeholder': 'XXXXX-XXX', 'maxlength': '9', 'inputmode': 'numeric', 'autocomplete':'postal-code'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': '(XX) 9XXXX-XXXX', 'maxlength': '15', 'inputmode': 'numeric', 'autocomplete':'tel'
        })
        self.fields['cpf_cnpj'].widget.attrs.update({
            'placeholder': 'XXX.XXX.XXX-XX', 'maxlength': '18', 'inputmode': 'numeric'
        })
        self.fields['address'].widget.attrs.update({'autocomplete':'street-address'})
        self.fields['number'].widget.attrs.update({'placeholder':'Nº'})
        self.fields['neighborhood'].widget.attrs.update({'placeholder':'Bairro'})
        self.fields['state'].widget.attrs.update({'id':'id_state'})
        self.fields['city'].widget.attrs.update({'id':'id_city', 'data-current-city': self.data.get('city', '') if self.is_bound else (self.instance.city if self.instance and self.instance.pk else '')})

        mark_required_fields(self)

    def clean_cep(self):
        import re
        cep = re.sub(r'\D', '', self.cleaned_data.get('cep') or '')
        if len(cep) != 8:
            raise forms.ValidationError('Informe um CEP válido no formato XXXXX-XXX.')
        return f'{cep[:5]}-{cep[5:]}'

    def clean_cpf_cnpj(self):
        # Mantém validação CPF/CNPJ já usada pelo EcoTech, mas salva formatado.
        document = super().clean_cpf_cnpj()
        if len(document) == 11:
            return f'{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}'
        return f'{document[:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[12:]}'

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('password')
        if raw_password:
            user.set_password(raw_password)
        if commit:
            user.save()
        return user
