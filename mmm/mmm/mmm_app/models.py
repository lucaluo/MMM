from django.db import models

# Create your models here

# user info table 
# associated with each django user object
class UserInfo(models.Model):
	# django user object id
	user_id = models.ForeignKey(max_length = 100, blank = false)
	
	is_sponsor = models.BooleanField()
	is_developer = models.BooleanField()
	
	# any settings that we decdie to add
	setting_0 = models.BooleanField()
	setting_1 = models.BooleanField()
	setting_2 = models.BooleanField()
	
	class Meta:
		ordering = ['user_id']

	def __unicode__(self):
		return u'%s' %(user_id)

# developers table
class Developer(models.Model):
	# django user object id
	user_id = models.ForeignKey(max_length = 100, blank = false)
	
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	bio = models.TextField()
	major = models.CharField(max_length=100, blank=True)
	project0 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
	project1 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
	project2 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
	project3 = models.ForeignKey('Project', blank=True, null=True, related_name='+')
	
	image = models.FileField("Developer Image", upload_to="images/developers/", blank=True)
	
	class Meta:
		ordering = ['last_name']
	
	def __unicode__(self):
		return u'%s, %s' %(self.last_name, self.first_name)
		
# sponsors table
class Sponsor(models.Model):
	# django user object id
	user_id = models.ForeignKey(max_length = 100, blank = false)
	
	org_name = models.CharField(max_length=100)
	org_bio = models.TextField()
	
	image = models.FileField("Sponsor Image", upload_to="images/sponsors/", blank=True)
	
	class Meta:
		ordering = ['org_name']
	
	def __unicode__(self):
		return u'%s' %(self.org_name)
		

class Project(models.Model):
	# django user object id
	user_id = models.ForeignKey(max_length = 100, blank = false)

	title = models.CharField(max_length=100)
	
	date_posted = models.DateTimeField('date posted')
	
	status = models.CharField(max_length=100)
	
	image = models.FileField("Project Image", upload_to="images/projects/", blank=True)
	
	likes = models.IntegerField()
	
	developer0 = models.ForeignKey('Developer', blank=True, null=True, related_name='+')
	developer1 = models.ForeignKey('Developer', blank=True, null=True, related_name='+')
	developer2 = models.ForeignKey('Developer', blank=True, null=True, related_name='+')
	
	description = models.TextField()
	
	tag_0 = models.ForeignKey(max_length = 100, blank = false)
	tag_1 = models.ForeignKey(max_length = 100, blank = false)
	tag_2 = models.ForeignKey(max_length = 100, blank = false)
	
	class Meta:
		ordering = ['date_posted']
	
	def __unicode__(self):
		return u'%s' %(self.title)
		
class Comment(models.Model):
	# django user object id
	user_id = models.ForeignKey(max_length = 100, blank = false)

	text = models.TextField()
	
	date_posted = models.DateTimeField('date posted')
	
	project_id = models.ForeignKey(max_length = 100, blank = false)

	title = models.CharField(max_length=100)
	
	class Meta:
		ordering = ['date_posted']
	
	def __unicode__(self):
		return u'%s' %(self.title)
		
class Tag(models.Model):
	term = models.CharField(max_length=100)
	
	class Meta:
		ordering = ['term']
	
	def __unicode__(self):
		return u'%s' %(self.term)

