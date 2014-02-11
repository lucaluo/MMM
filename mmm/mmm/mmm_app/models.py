from django.db import models
from django.contrib.auth.models import User

# Create your models here

# user info table
# associated with each django user object
class UserInfo(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = False)

	# is the user a sponsor or developer?
	is_sponsor = models.BooleanField()
	is_developer = models.BooleanField()

	# any settings that we decdie to add
	setting_0 = models.BooleanField()
	setting_1 = models.BooleanField()
	setting_2 = models.BooleanField()

	class Meta:
		ordering = ['user']

	def __unicode__(self):
		return u'%s' %(self.user.username)

# developers table
class Developer(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = False)

	# developer information
	major = models.CharField(max_length=100, blank=True)
	bio = models.TextField()

	# optional picture of developer
	image = models.FileField("Developer Image", upload_to="images/developers/", blank=True)

	# projects that the developer is a part of
	projects = models.ManyToManyField('Project', related_name = 'dev_proj_assoc', blank=True)
		
	class Meta:
		ordering = ['user']

	def __unicode__(self):
		return u'%s' %(self.user.username)

# sponsors table
class Sponsor(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = False)

	# sponsor information
	org_name = models.CharField(max_length=100)
	org_bio = models.TextField()
		
	# optional sponsor picture/logo
	image = models.FileField("Sponsor Image", upload_to="images/sponsors/", blank=True)

	class Meta:
		ordering = ['user']

	def __unicode__(self):
		return u'%s' %(self.org_name)

# projects table
class Project(models.Model):
	# choices for status
	STATUS_CHOICES = (
    ('IN', 'Inactive'),
    ('AC', 'Active'),
    ('CO', 'Completed'),
	)

	# project information
	title = models.CharField(max_length=100)
	date_posted = models.DateTimeField('date posted')
	sponsor = models.ForeignKey(User, unique = True, max_length = 100, blank = False)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='IN')
	show_in_gallery = models.BooleanField() # show in gallery after competion
	description = models.TextField()
	requirements = models.TextField()
	likes = models.IntegerField()

	image = models.FileField("Project Image", upload_to="images/projects/", blank=True)

	# developers that are a part of the project
	developers = models.ManyToManyField(User, related_name = 'proj_dev_assoc', blank=True)
		
	# sub-categorization of project
	category_subs = models.ManyToManyField('Category_sub', blank=True) 
	
	# top level categorization of project
	category_tops = models.ManyToManyField('Category_top', blank=True) 
	
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
	date_posted = models.DateTimeField('date posted')
	title = models.CharField(max_length=100)
	text = models.TextField()

	class Meta:
		ordering = ['date_posted']

	def __unicode__(self):
		return u'%s' %(self.title)

# category_top table
class Category_top(models.Model):
	# the category name
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return u'%s' %(self.name)

# category_sub table
class Category_sub(models.Model):
	# the category name
	name = models.CharField(max_length=100)

	# the category_top this category_sub belongs to
	top = models.ForeignKey(Category_top, max_length = 100, blank = False)	
	
	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return u'%s -> %s' %(self.top.name, self.name)

