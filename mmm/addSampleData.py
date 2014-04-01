# INSTRUCTIONS: Run the following commands from the directory MMM/mmm
#				python manage.py shell < deleteSampleData.py
#				python manage.py shell < addSampleData.py
# IMPORTANT:	You MUST delete data from the database before adding the sample data


from mmm.mmm_app.models import *
from django.contrib.auth.models import User
from django.utils import timezone

#--------------------------------------
# Category_top

cat_t0 = Category_top(
	name = 'Platform',
)
cat_t0.save()

cat_t1 = Category_top(
	name = 'Language',
)
cat_t1.save()

cat_t2 = Category_top(
	name = 'Category',
)
cat_t2.save()

cat_t3 = Category_top(
	name = 'Pay',
)
cat_t3.save()



#--------------------------------------
# Category_sub

cat_s0 = Category_sub(
	name = 'Android',
	category_top = cat_t0,
)
cat_s0.save()

cat_s1 = Category_sub(
	name = 'iOS',
	category_top = cat_t0,
)
cat_s1.save()

cat_s2 = Category_sub(
	name = 'Windows Phone',
	category_top = cat_t0,
)
cat_s2.save()

cat_s3 = Category_sub(
	name = 'Web App',
	category_top = cat_t0,
)
cat_s3.save()

cat_s4 = Category_sub(
	name = 'C',
	category_top = cat_t1,
)
cat_s4.save()

cat_s5 = Category_sub(
	name = 'C++',
	category_top = cat_t1,
)
cat_s5.save()

cat_s6 = Category_sub(
	name = 'Java',
	category_top = cat_t1,
)
cat_s6.save()

cat_s7 = Category_sub(
	name = 'Objective C',
	category_top = cat_t1,
)
cat_s7.save()

cat_s8 = Category_sub(
	name = 'Education',
	category_top = cat_t2,
)
cat_s8.save()

cat_s9 = Category_sub(
	name = 'Research',
	category_top = cat_t2,
)
cat_s9.save()

cat_s10 = Category_sub(
	name = 'Medical',
	category_top = cat_t2,
)
cat_s10.save()

cat_s11 = Category_sub(
	name = 'Entertainment',
	category_top = cat_t2,
)
cat_s11.save()

cat_s12 = Category_sub(
	name = 'Media',
	category_top = cat_t2,
)
cat_s12.save()

cat_s13 = Category_sub(
	name = 'Productivity',
	category_top = cat_t2,
)
cat_s13.save()

cat_s14 = Category_sub(
	name = 'Transportation',
	category_top = cat_t2,
)
cat_s14.save()

cat_s15 = Category_sub(
	name = 'Paid',
	category_top = cat_t3,
)
cat_s15.save()

cat_s16 = Category_sub(
	name = 'Unpaid',
	category_top = cat_t3,
)
cat_s16.save()



#--------------------------------------
# Users

u0 = User.objects.create_user(
	'user0', 
	'user0@fakemail.com', 
	'user0_pswd',
)
u0.save()

u1 = User.objects.create_user(
	'user1', 
	'user1@fakemail.com', 
	'user1_pswd',
)
u1.save()

u2 = User.objects.create_user(
	'user2', 
	'user2@fakemail.com', 
	'user2_pswd',
)
u2.save()

u3 = User.objects.create_user(
	'user3', 
	'user3@fakemail.com', 
	'user3_pswd',
)
u3.save()

#--------------------------------------
# UserInfo

ui0 = UserInfo(
	user = u0,
	setting_0=True,
	setting_1=True,
	setting_2=True,
	major = 'Computer Engineering',
	bio = 'I am a cool person.',
	full_name = 'User Zero',
)
ui0.save()

ui1 = UserInfo(
	user = u1,
	setting_0=False,
	setting_1=True,
	setting_2=False,
	major = 'Computer Science',
	bio = 'I love computers!!!!',
	full_name = 'User One',
)
ui1.save()

ui2 = UserInfo(
	user = u2,
	setting_0=False,
	setting_1=False,
	setting_2=False,
	full_name = 'The coolest Startup Ever',
	bio = 'Ann Arbor based startup.',
)
ui2.save()

ui3 = UserInfo(
	user = u3,
	setting_0=False,
	setting_1=False,
	setting_2=False,
	major = 'Computer Science',
	bio = 'Im a cool person',
	full_name = 'User Three',
)
ui3.save()

#--------------------------------------
# Project

p0 = Project(
	title = 'The New Angry Birds',
	date_posted = timezone.now(),
	sponsor = u2,
	status = 'OP',
	show_in_gallery = True,
	description = 'A talented team of Java developers are making the next Angry Bird game for Android!',
	flags = 0,
)
p0.save()
p0.category_subs.add(cat_s0)
p0.category_subs.add(cat_s3)
p0.category_subs.add(cat_s7)
p0.save()

p1 = Project(
	title = 'Bitcoin Mining Operation',
	date_posted = timezone.now(),
	sponsor = u3,
	status = 'OP',
	show_in_gallery = False,
	description = 'We are going to get rich by stealing bitcoins.',
	flags = 1,
)
p1.save()
p1.category_subs.add(cat_s5)
p1.category_subs.add(cat_s6)
p1.save()

# add bookmaked projects to userInfos
ui0.bookmarks.add(p0)
ui1.bookmarks.add(p1)
ui2.bookmarks.add(p0)
ui2.bookmarks.add(p1)

#--------------------------------------
# Comment

c0 = Comment(
	user = u0,
	project = p0,
	date_posted = timezone.now(),
	text = 'Wow this is such a cool project!',
	flags = 0,
)
c0.save()

c1 = Comment(
	user = u3,
	project = p1,
	date_posted = timezone.now(),
	text = 'You all are bad people.',
	flags = 4,
)
c1.save()

c2 = Comment(
	user = u1,
	project = p1,
	date_posted = timezone.now(),
	text = 'Hi folks. The FBI would like to speak with you...',
	flags = 0,
)
c2.save()
