from django.http import HttpResponse
from nutri.forms import NutriForm
from django.shortcuts import render
from ingred_table.models import Ingredient

def nutriForm(request):
	ingredients = ('hello', 'barnacles')
	if request.method == 'POST':
		form = NutriForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			print cd['ingredient']
			print cd['amount']
			print cd['unit']

			return render(request, 'nutri_form.html', {'form': form, 'ingred_list':ingredients})
	else:
		form = NutriForm(initial={'ingredient': 'pasta'})
	return render(request, 'nutri_form.html', {'form': form, 'ingred_list':ingredients})