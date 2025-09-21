from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, CallRecord
class SignUpForm(UserCreationForm):
    email= forms.EmailField(label="", widget=forms.TextInput(attrs={"class":"form-control form-control-user", "placeholder":"Email Address"}))
    first_name= forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class":"form-control form-control-user", "placeholder":"First Name"}))
    last_name= forms.CharField(label="",  max_length=100, widget=forms.TextInput(attrs={"class":"form-control form-control-user", "placeholder":"Last Name"}))
    username= forms.CharField(label="",  max_length=100, widget=forms.TextInput(attrs={"class": "form-control form-control-user", "placeholder":"User Name"}))
    password1= forms.CharField(label="",  max_length=100, widget=forms.PasswordInput(attrs={"class":"form-control form-control-user", "placeholder":"Password"}))
    password2= forms.CharField(label="",  max_length=100, widget=forms.PasswordInput(attrs={"class":"form-control form-control-user", "placeholder":"Confirm Password"}))

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'password1', 'password2'}

#create Add Customer form
class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name","class":"form-control"}),label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name","class":"form-control"}),label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email","class":"form-control"}),label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone","class":"form-control"}),label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address","class":"form-control"}),label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City","class":"form-control"}),label="")
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"state","class":"form-control"}),label="")
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode","class":"form-control"}),label="")

    class Meta:
        model = Customer
        exclude = ("user",)


#create upload audio form
class AudioUploadForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"file name","class":"form-control"}),label="")

    class Meta:
        model = CallRecord        
        fields = ('audio_file','title')  
