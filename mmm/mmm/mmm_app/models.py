from django.db import models
from django.contrib.auth.models import User
import os

def path_and_rename(path):
	def wrapper(instance, filename):
		ext = filename.split('.')[-1]
		filename = '{}.{}'.format(instance.pk, ext)
		# return the whole path to the file
		return os.path.join(path, filename)
	return wrapper

# Create your models here

# user info table
# associated with each django user object
class UserInfo(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = False)

	# any settings that we decdie to add
	setting_0 = models.BooleanField()
	setting_1 = models.BooleanField()
	setting_2 = models.BooleanField()

	# bookmarked projects
	bookmarks = models.ManyToManyField('Project', blank = True)

	# developer information
	major = models.CharField(max_length=100, blank=True) # major/department
	bio = models.TextField()

	# sponsor information
	org_name = models.CharField(max_length=100)
	org_bio = models.TextField()
		
	# optional picture/logo
	image = models.FileField("User Image", upload_to=path_and_rename("images/users/"), blank=True)	
	
	class Meta:
		ordering = ['user']

	def __unicode__(self):
		return u'%s: (%s %s)' %(self.user.username, self.user.first_name, self.user.last_name)


# projects table
class Project(models.Model):
	# choices for status
	STATUS_CHOICES = (
	    ('OP', 'Open'),
	    ('CL', 'Closed'),
	    ('CO', 'Completed'),
	)

	# project information
	title = models.CharField(max_length=100)
	date_posted = models.DateTimeField('date posted', auto_now_add=True)
	sponsor = models.ForeignKey(User, max_length = 100, blank = False)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='IN')
	show_in_gallery = models.BooleanField() # show in gallery after competion
	description = models.TextField()
	flags = models.IntegerField()

	image = models.FileField("Project Image", upload_to=path_and_rename("images/projects/"), blank=True)
		
	# sub-categorization of project
	category_subs = models.ManyToManyField('Category_sub', blank=True) 
	
	class Meta:
		ordering = ['date_posted']

	def __unicode__(self):
		return u'%s' %(self.title)

# comments table
class Comment(models.Model):
	# django user object id
	user = models.ForeignKey(User, max_length = 100, blank = False)

	# comment information
	project = models.ForeignKey(Project, max_length = 100, blank = False)
	date_posted = models.DateTimeField('date posted', auto_now_add=True)
	text = models.TextField()
	flags = models.IntegerField()

	class Meta:
		ordering = ['date_posted']

	def __unicode__(self):
		return u'%s -> %s' %(self.project, self.title)

# category_top table
class Category_top(models.Model):
	# the category name
	name = models.CharField(max_length=100)

	# sub-categorization of project
	# category_subs = models.ManyToManyField('Category_sub', blank=True) 

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return u'%s' %(self.name)

# category_sub table
class Category_sub(models.Model):
	# the category name
	name = models.CharField(max_length=100)

	# the category_top this category_sub belongs to
	category_top = models.ForeignKey(Category_top, max_length = 100, blank = False)	
	
	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return u'%s -> %s' %(self.category_top.name, self.name)
