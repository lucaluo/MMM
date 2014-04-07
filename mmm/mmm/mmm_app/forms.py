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
	# user information
	full_name = forms.CharField(max_length=50)
	user_image = forms.FileField(required=False)
	major = forms.CharField(max_length=50, required=False)
	bio = forms.CharField(max_length=500, required=False)
	weekly_email = forms.BooleanField(required=False)
	
class FilterForm(forms.Form):
	bookmarked = forms.BooleanField(required=False)
	additional_filter = forms.CharField(max_length=50, required=False)
	f_category_subs = forms.ModelMultipleChoiceField(
			queryset = Category_sub.objects.all(),
			required = False,
		)
	
