from django import forms
from models import *

class ProjectForm(forms.Form):
	title = forms.CharField(max_length=100)
	description = forms.CharField(required=False)
	requirements = forms.CharField(required=False)
	image = forms.FileField(required=False)
	category_subs = forms.ModelMultipleChoiceField(
			queryset = Category_sub.objects.all(),
			required = False,
		)