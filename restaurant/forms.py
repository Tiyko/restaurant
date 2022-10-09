from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)


class ReservationForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    time = forms.TimeField()
    date = forms.DateField()
    number_of_people = forms.FloatField()


class ItemsForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
    zipcode = forms.CharField(label='Zipcode', max_length=20)
    meal_name = forms.CharField(label='Meal Name', max_length=100)
    total_price = forms.FloatField()
    # quantity = forms.IntegerField()
