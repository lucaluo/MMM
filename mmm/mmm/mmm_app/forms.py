from django import forms
from models import *

#def getAllCategories():
#	category_top_list = Category_top.objects.all().order_by('name')
#	category_list = []
#	for category_top in category_top_list:
#		category = {}
#		category['category_top'] = category_top
#		category['category_sub_list'] = Category_sub.objects.filter(category_top=category_top)
#		category_list.append(category)
#	return category_list

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
	
class FilterForm(forms.Form):
	additional_filter = forms.CharField(max_length=50, required=False)
	f_category_subs = forms.ModelMultipleChoiceField(
			queryset = Category_sub.objects.all(),
			required = False,
			widget=forms.CheckboxSelectMultiple
		)
	
	
	# cd is a dictionary containing two entries:
	#	category_top: category_top_name
	#	category_sub_list: category_sub_list
	#def __init__(self, *args, **kwargs):
		#super(FilterForm, self).__init__(args, kwargs)
		
		#i = 0
		#for cd in getAllCategories():
			#for cs in cd['category_sub_list']:
				#self.fields[i] = forms.BooleanField()
				#++i

