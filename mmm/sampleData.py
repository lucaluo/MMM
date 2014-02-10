from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Category_top, Category_sub
from django.contrib.auth.models import User
from django.utils import timezone

#--------------------------------------

cat_t = Category_top(
	name = 'Platform',
)
cat_t.save()

cat_s = Category_sub(
	name = 'Android',
	top = cat_t,
)
cat_s.save()

#--------------------------------------

# User0
u = User.objects.create_user(
	'user0', 
	'user0@fakemail.com', 
	'user0_pswd',
	first_name='User', 
	last_name='Zero', 
)
u.save()

ui = UserInfo(
	user = u,
	is_sponsor=False, 
	is_developer=True,
	setting_0=True,
	setting_1=True,
	setting_2=True,
)
ui.save()

# Developer0
d = Developer(
	user = u,
	major = 'Computer Engineering',
	bio = 'I am a cool person.',
)
d.save()

#--------------------------------------

# User1
u = User.objects.create_user(
	'user1', 
	'user1@fakemail.com', 
	'user1_pswd',
	first_name='User', 
	last_name='One', 
)
u.save()

ui = UserInfo(
	user = u,
	is_sponsor=False, 
	is_developer=True,
	setting_0=False,
	setting_1=True,
	setting_2=False,
)
ui.save()

# Developer1
d = Developer(
	user = u,
	major = 'Computer Science',
	bio = 'I love computers!!!!',
)
d.save()

#--------------------------------------

# User2
u = User.objects.create_user(
	'user2', 
	'user2@fakemail.com', 
	'user2_pswd',
	first_name='User', 
	last_name='Two', 
)
u.save()

ui = UserInfo(
	user = u,
	is_sponsor=True, 
	is_developer=False,
	setting_0=False,
	setting_1=False,
	setting_2=False,
)
ui.save()

# Sponsor0
s = Sponsor(
	user = u,
	org_name = 'Really Cool Startup',
	org_bio = 'We are the most cool and awesome startup in the entire city of Ann Arbor!',
)
s.save()

#--------------------------------------

# User3
u = User.objects.create_user(
	'user3', 
	'user3@fakemail.com', 
	'user3_pswd',
	first_name='User', 
	last_name='Three', 
)
u.save()

ui = UserInfo(
	user = u,
	is_sponsor=True, 
	is_developer=False,
	setting_0=False,
	setting_1=False,
	setting_2=False,
)
ui.save()

# Developer2
d = Developer(
	user = u,
	major = 'Computer Science',
	bio = 'Im a cool person',
)
d.save()

# Sponsor1
s = Sponsor(
	user = u,
	org_name = 'The Even More Cooler Startup',
	org_bio = 'We build Android apps for everything.',
)
s.save()

#--------------------------------------

p = Project(
	title = 'The New Angry Birds',
	date_posted = timezone.now(),
	sponsor = u,
	status = 'active',
	description = 'A talented team of Java developers are making the next Angry Bird Game for Android!',
	likes = 0,
	developers = (Developer.objects.get(pk=1), Developers.objects.get(pk=2)),
)
p.save()

#--------------------------------------

c = Comment(
	user = u,
	project = p,
	date_posted = timezone.now(),
	title = 'AWESOME!!',
	text = 'Wow this is such a cool project!',
)
c.save()

