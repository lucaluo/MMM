from django.db import models

# Create your models here

# user info table
# associated with each django user object
class UserInfo(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = false)

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
		return u'%s' %(user)

# developers table
class Developer(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = false)

	# developer information
	major = models.CharField(max_length=100, blank=True)
	bio = models.TextField()

	# optional picture of developer
	image = models.FileField("Developer Image", upload_to="images/developers/", blank=True)

	# projects that the developer is a part of
	projects = models.ManyToManyField(Project, blank=True)
		#project0 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
		#project1 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
		#project2 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
		#project3 = models.ForeignKey('Project', blank=True, null=True, related_name='+')

	class Meta:
		ordering = ['user.last_name']

	def __unicode__(self):
		return u'%s, %s' %(user.last_name, user.first_name)

# sponsors table
class Sponsor(models.Model):
	# django user object id
	user = models.ForeignKey(User, unique = True, max_length = 100, blank = false)

	# sponsor information
	org_name = models.CharField(max_length=100)
	org_bio = models.TextField()
		
	# optional sponsor picture/logo
	image = models.FileField("Sponsor Image", upload_to="images/sponsors/", blank=True)

	class Meta:
		ordering = ['org_name']

	def __unicode__(self):
		return u'%s' %(self.org_name)

# projects table
class Project(models.Model):
	# project information
	title = models.CharField(max_length=100)
	date_posted = models.DateTimeField('date posted')
	sponsor = models.ForeignKey(User, unique = True, max_length = 100, blank = false)
	status = models.CharField(max_length=100)
	description = models.TextField()
	likes = models.IntegerField()

	image = models.FileField("Project Image", upload_to="images/projects/", blank=True)

	# developers that are a part of the project
	developers = models.ManyToManyField(User, blank=True)
		#developer0 = models.ForeignKey('Developer', blank=True, null=True, related_name='+')
		#developer1 = models.ForeignKey('Developer', blank=True, null=True, related_name='+')
		#developer2 = models.ForeignKey('Developer', blank=True, null=True, related_name='+')

	# tags (keywords or search terms) applicable to the project
	tags = models.ManyToManyField(Tag, blank=True)
		#tag_0 = models.ForeignKey(max_length = 100, blank = false)
		#tag_1 = models.ForeignKey(max_length = 100, blank = false)
		#tag_2 = models.ForeignKey(max_length = 100, blank = false)

	class Meta:
		ordering = ['-date_posted']

	def __unicode__(self):
		return u'%s' %(self.title)

# comments table
class Comment(models.Model):
	# django user object id
	user = models.ForeignKey(User, max_length = 100, blank = false)

	# comment information
	project = models.ForeignKey(Project, max_length = 100, blank = false)
	date_posted = models.DateTimeField('date posted')
	title = models.CharField(max_length=100)
	text = models.TextField()

	class Meta:
		ordering = ['date_posted']

	def __unicode__(self):
		return u'%s' %(self.title)

# tags table
class Tag(models.Model):
	# the tag term (keyword)
	term = models.CharField(max_length=100)

	class Meta:
		ordering = ['term']

	def __unicode__(self):
		return u'%s' %(self.term)

