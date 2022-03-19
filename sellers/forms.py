from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm

user_choices= [
    ('none', 'none'),
    ('Admin', 'Admin'),
    ('Seller', 'Seller'),
    ('Buyer', 'Buyer'),
    ]


class SignUpForm(UserCreationForm):
    class Meta:
        model=Users
        fields = {'choices', 'username', 'email','password1','password2'}

    # email = forms.CharField(max_length=255,required=True,widget=forms.EmailInput())
    username = forms.CharField(label='username')
    choices= forms.CharField(label='User Type', widget=forms.Select(choices=user_choices))
    field_order = ['choices', 'username', 'email', 'password1']
    # favorite_fruit= forms.ModelChoiceField(queryset=user_choices.all())

# class ProjectForm(ModelForm):
#     class Meta:
#         model = Sellers
#         fields = '__all__'

#     start_date = DateTimeField(widget=SelectDateWidget)
#     end_date = DateTimeField(widget=SelectDateWidget)

#     field_order = ['start_date', 'end_date']