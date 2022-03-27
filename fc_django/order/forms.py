from webbrowser import get
from django import forms
from .models import Order


class RegisterForm(forms.Form):
    def __init__(self,request, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.request = request


    quantity = forms.IntegerField(
        error_messages={'required':'상품수량을 입력해주세요.'},
        label='상품수량'
    )
    product = forms.IntegerField(
        error_messages={'required':'상품ID을 입력해주세요.'},
        label='상품ID', widget=forms.HiddenInput
    )
    

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        
        if not( quantity and product ) :
            self.add_error('quantity','값이 없습니다.')
            self.add_error('product', '값이 없습니다.')


    