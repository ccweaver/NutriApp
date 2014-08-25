from django.http import HttpResponse
from nutri.forms import NutriForm
from django.shortcuts import render

def nutriForm(request):
	if request.method == 'POST':
		form = NutriForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = NutriForm(initial={'ingredient': 'pasta'})
	return render(request, 'nutri_form.html', {'form': form})