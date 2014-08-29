from django.http import HttpResponse
from django import forms
from nutri.forms import NutriForm
from django.shortcuts import render
from ingred_table.models import Ingredient

def nutriForm(request):
	ingred_list = []
	error = ""
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

		if 'amount' in request.POST:
			if 'ingred_to_add' not in request.POST:
				error = 'Please search for and select an ingredient'
			else:
				ingred_to_add = request.POST['ingred_to_add']
			amount = request.POST['amount']
			unit = request.POST['unit']

			if not error and not amount:
				error = 'Please input an amount'
			if error:
				print 'major error'
				return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error})


		return render(request, 'select_temp.html', {'ingred_list':ingred_list, 'error':error})
	else:
		return render(request, 'nutri_form.html', {'ingred_list':ingred_list, 'error':error})



'''		form = NutriForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			print cd['ingredient']
			print cd['amount']
			print cd['unit']

			ingred_list.append(cd['ingredient'])

			return render(request, 'nutri_form.html', {'form': form, 'ingred_list':ingred_list})
	'''
	