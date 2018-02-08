from django import forms;
from places.models import City

class CityForm(forms.Form):
	choices = [(x.id,x.name) for x in City.objects.all()]
	city = forms.ChoiceField(choices=choices,required=False)

class SearchForm(forms.Form):
	query = forms.CharField(required=False)