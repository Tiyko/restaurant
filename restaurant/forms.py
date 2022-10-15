from django import forms


class ReservationForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    time = forms.TimeField()
    date = forms.DateField()
    number_of_people = forms.FloatField()
