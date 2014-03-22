# INSTRUCTIONS: Run the following commands from the directory MMM/mmm
#				python manage.py shell < deleteSampleData.py

from mmm.mmm_app.models import UserInfo, Project, Comment, Category_top, Category_sub
from django.contrib.auth.models import User
from django.utils import timezone

UserInfo.objects.all().delete()
Project.objects.all().delete()
Comment.objects.all().delete()
Category_top.objects.all().delete()
Category_sub.objects.all().delete()
for x in User.objects.all():
	if (not (x.username == 'admin')):
		x.delete()

