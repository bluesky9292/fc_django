import email
from urllib import request
from django import forms
from .models import Fcuser
from django.contrib.auth.hashers import check_password

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required':'이메일을 입력해주세요.'},
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={'required':'비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput, label='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={'required':'비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password :
            if password != re_password : 
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
                self.add_error('re_password', '비밀번호가 일치하지 않습니다.')
          

class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required':'이메일을 입력해주세요.'},
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={'required':'비밀번호를 입력해주세요.'},
        widget=forms.PasswordInput, label='비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', '등록된 사용자가 없습니다.')
                return

            if not check_password(password, fcuser.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
            
