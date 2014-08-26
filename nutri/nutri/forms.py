from django import forms
from ingred_table.models import Ingredient
import autocomplete_light

class NutriForm(forms.Form):
	ingreds = []
	for i in Ingredient.objects.filter(ingredient__icontains='butter'):
		print i.ingredient

	units = (('g','g'),('oz','oz'),('mL','mL'),('tsp','tsp'),('tblspn','tblspn'))


	ingredient = forms.ModelChoiceField(required=True, queryset=Ingredient.objects.all(), widget=autocomplete_light.ChoiceWidget('au'))
	amount = forms.DecimalField(max_digits=7, decimal_places=2, min_value=(0))
	unit = forms.ChoiceField(choices=units)