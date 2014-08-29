from django.http import HttpResponse
from django import forms
from nutri.forms import NutriForm
from django.shortcuts import render
from ingred_table.models import Ingredient

def nutriForm(request):
	ingred_list = []
	#['jelly beans,RAW(of course)', 'barnacles']
	if request.method == 'POST':
		print request.POST
		if 'term' in request.POST:
			print request.POST['term']
			ingred_list = Ingredient.objects.filter(ingredient__icontains=request.POST['term'])
			if not ingred_list:
				ingred_list = ['Sorry, no ingredient found']
			if not request.POST['term']:
				ingred_list = []
			
			#count = 10
			#for x in range(0,count):
			#	print ingred_list[x]

		return render(request, 'select_temp.html', {'ingred_list':ingred_list})
	else:
		return render(request, 'nutri_form.html', {'ingred_list':ingred_list})



'''		form = NutriForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			print cd['ingredient']
			print cd['amount']
			print cd['unit']

			ingred_list.append(cd['ingredient'])

			return render(request, 'nutri_form.html', {'form': form, 'ingred_list':ingred_list})
	'''
	