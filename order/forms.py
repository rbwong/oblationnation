from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(label='Name', max_length=80)
    email = forms.EmailField(label='Email')
    contact = forms.CharField(label='Contact No', max_length=80)
    street = forms.CharField(label='Address', max_length=80)
    city = forms.CharField(label='Town/City', max_length=30)
