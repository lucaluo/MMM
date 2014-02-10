# INSTRUCTIONS: Run the following commands from the directory MMM/mmm
#				python manage.py shell < deleteSampleData.py


from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Category_top, Category_sub
from django.contrib.auth.models import User
from django.utils import timezone

# Delete User
for x in User.objects.all():
	if x.username == 'admin':
		pass
	else:
		x.delete()

# Delete UserInfo
for x in UserInfo.objects.all():
	x.delete()
	
# Delete Developer
for x in Developer.objects.all():
	x.delete()

# Delete Sponsor
for x in Sponsor.objects.all():
	x.delete()

# Delete Project
for x in Project.objects.all():
	x.delete()

# Delete Comment
for x in Comment.objects.all():
	x.delete()

# Delete Category_top
for x in Category_top.objects.all():
	x.delete()

# Delete Category_sub
for x in Category_sub.objects.all():
	x.delete()

