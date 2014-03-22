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
		
class ProfileForm(forms.Form):
	# in template use {{ ProfileForm.fieldName.as_hidden }} to make invisible
	PROJ_CHOICES = Project.objects.filter(status='OP')
	# user information
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	user_image = forms.FileField(required=False)
	# developer information
	bio = forms.CharField(max_length=500)
	skills = forms.CharField(max_length=200)
	projects = forms.MultipleChoiceField(choices=PROJ_CHOICES)
	# sponsor information
	org_name = forms.CharField(max_length=50)
	org_bio = forms.CharField(max_length=500)
	org_image = forms.FileField(required=False)
	
#class FilterForm(forms.Form):
		
		
