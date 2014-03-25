from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template import RequestContext
from models import *
from forms import *
import hashlib

HOMEPAGE_URL = '/'
LOGIN_URL = '/login_form/'
REGISTER_URL = '/login_form/'

def landing(request):
	if request.user.is_authenticated():
		# get user info
		userInfo = UserInfo.objects.get(user=request.user)
		# set loggined
		loggined = True
	else:
		# set not loggined
		loggined = False
			
	# get all tags
	category_top_list = Category_top.objects.all().order_by('name')
	category_list = []
	for category_top in category_top_list:
		category = {}
		category['category_top'] = category_top
		category['category_sub_list'] = Category_sub.objects.filter(category_top=category_top)
		category_list.append(category)
	
	# get list of projects
	projects = Project.objects.filter(status='OP').order_by('-date_posted')
	
	# apply filters
	#if request.method == 'POST':
	#	if filter0: # corresponds to checkbox being checked
	#		f0 = Category_sub.objects.get(name='filter0')
	#		projects.filter(Category_subs=f0)
	#	if filter1:
	#		f1 = Category_sub.objects.get(name='filter1')
	#		projects.filter(Category_subs=f1
	
	return render(request, 'landing.html', {'projects': projects, 'category_list': category_list}, context_instance=RequestContext(request))

def user_register(request):
	if request.method == 'POST':
		uniqname = request.POST['uniqname']
		password = request.POST['password']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		if not (password and uniqname and firstname and lastname):
			return redirect(REGISTER_URL)
		if User.objects.filter(username=uniqname).exists():
			return redirect(REGISTER_URL)
		# TODO: Check legitimate username, password, uniqname, etc.
		email = uniqname + '@umich.edu'
		user = User.objects.create_user(username=uniqname, password=password, email=email, first_name=firstname, last_name=lastname)
		user.is_active = False
		send_verify_email(request, uniqname, email)
		user.save()
		return redirect('/thankyou/')
	else:
		raise Http404

def send_verify_email(request, username, email):
	activation_code = generate_actication_code(username)
	verify_url = request.build_absolute_uri('/activate/' + username + '/' + activation_code)
	user = User.objects.get(username=username)
	send_mail('Michigan Mobile Manufactory User Verification', render(request, 'email_verification.txt', {'user': user, 'verify_url': verify_url}).content, 'mmm.umich@gmail.com', [email], fail_silently=False)

def user_activate(request, username, activation_code):
	if activation_code == generate_actication_code(username):
		user = User.objects.get(username=username)
		user.is_active = True
		user.save()
		userInfo = UserInfo(user=user, setting_0=False, setting_1=False, setting_2=False)
		userInfo.save()
		return redirect(LOGIN_URL)
	else:
		return redirect(REGISTER_URL)

def generate_actication_code(username):
	return hashlib.sha256(username[0] + username[-1] + username).hexdigest()

def user_login_form(request):
	if request.method == 'GET':
		if request.GET.get('next'):
			next = request.GET['next']
		else:
			next = HOMEPAGE_URL
		if request.user.is_authenticated():
			return redirect(next)
		else:
			return render(request, 'login.html', {'next': next}, context_instance=RequestContext(request))


def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if request.POST['next']:
			next = request.POST['next']
		else:
			next = HOMEPAGE_URL
		if not (username and password):
			return render(request, 'login.html', {'next': next, 'username': username, 'error': 'Fields cannot be empty'}, context_instance=RequestContext(request))
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(next);
			else:
				# Return a 'disabled account' error message
				return render(request, 'login.html', {'next': next, 'username': username, 'error': 'Account Disabled!'}, context_instance=RequestContext(request))
		else:
			# Return an 'invalid login' error message.
			return render(request, 'login.html', {'next': next, 'username': username, 'error': 'Login Invalid'}, context_instance=RequestContext(request))
	else:
		raise Http404

def user_logout(request):
	logout(request)
	# redirect to homepage
	return redirect(HOMEPAGE_URL)

# doesn't work yet
@login_required
def profile(request, prof_id):
	if request.method == 'POST':
		if prof_id == str(request.user.id):
			# bound form
			form = ProfileForm(request.POST, request.FILES)
			if form.is_valid():
				# get user and userInfo to edit
				userInfo = UserInfo.objects.get(user=request.user)
				# this is the cleaned data
				full_name = form.cleaned_data['full_name']
				major = form.cleaned_data['major']
				bio = form.cleaned_data['bio']
				# update models in db
				userInfo.full_name = full_name
				userInfo.major = major
				userInfo.bio = bio
				if request.FILES.get('image'):
					userInfo.image = request.FILES['image']
				userInfo.save()
				return redirect('/profile/' + prof_id + '/')
			else:
				# TODO pass error message to template
				print form.errors
		else:
			# TODO pass error message to template
			print request.user.id
	else:
		# unbound form
		form = ProfileForm()
		# get info
		userInfo = UserInfo.objects.get(user=prof_id)
		# get sponsored projects
		projects = Project.objects.filter(sponsor=prof_id)
		# render
		return render(request, 'profile.html', {'userInfoObj': userInfo, 'profileEditForm':form, 'projects': projects}, context_instance=RequestContext(request))

# @login_required
# def update_profile(request):
#    pass # is this view necessary?

@login_required
def new_project(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			project = Project(
							title=form.cleaned_data['title'], 
							sponsor=request.user, 
							status='OP', 
							show_in_gallery=True, 
							description=form.cleaned_data['description'], 
							flags=0,
						)
			project.save()
			if request.FILES.get('image'):
				project.image = request.FILES['image']
			for category_sub in form.cleaned_data['category_subs']:
				project.category_subs.add(category_sub)
			project.save()
			return redirect(HOMEPAGE_URL)
		else:
			print 'not valid'
	else:
		raise Http404


@login_required
def project(request, proj_id):
	if request.method == 'POST':
		# TODO edit project
		pass
	else:
		try:
			project = Project.objects.get(id=proj_id)
		except Project.DoesNotExist:
			raise Http404
		sponsor = UserInfo.objects.get(id=project.sponsor.id)
		category_subs = project.category_subs.all()
		comments = Comment.objects.filter(project=project)
		commentsObj = []
		for comment in comments:
			commentObj = {'comment': comment, 'commenter': UserInfo.objects.get(id=comment.user.id)}
			commentsObj.append(commentObj)
		return render(request, 'projDetails.html', {'project': project, 'sponsor': sponsor, 'category_subs': category_subs, 'commentsObj': commentsObj}, context_instance=RequestContext(request))

@login_required
def apply_project(request):
	if request.method == 'POST':
		if request.POST['message'] and request.POST['proj_id']:
			message = request.POST['message']
			proj_id = request.POST['proj_id']
			applier = request.user
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			profile_url = request.build_absolute_uri('/profile/' + str(applier.id) + '/')
			project_url = request.build_absolute_uri('/project/' + str(proj_id) + '/')
			sponsor_email = EmailMessage('Project Application on Michigan Mobile Manufactory', render(request, 'email_sponsor.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url}).content, 'mmm.umich@gmail.com', [project.sponsor.email], [], headers = {'Reply-To': applier.email})
			sponsor_email.send(fail_silently=False)
			applier = EmailMessage('Confirmation of Project Application on Michigan Mobile Manufactory', render(request, 'email_applier.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url}).content, 'mmm.umich@gmail.com', [applier.email], [])
			applier.send(fail_silently=False)
			return redirect(HOMEPAGE_URL)
		else:
			return redirect(HOMEPAGE_URL)
	else:
		raise Http404
	
# @login_required
# def edit_project(request, proj_id):
# 	projectInfo = Project.obejcts.get(id=proj_id)
# 	#developers = proejctInfo.developers.all()
# 	tags = projectInfo.category_subs.all().order_by('top')
# 	comments = Comment.objects.filter(project=proj_id)
# 	# render()

@login_required
def new_comment(request):
	if request.method == 'POST':
		if request.POST['comment'] and request.POST['proj_id']:
			comment = request.POST['comment']
			proj_id = request.POST['proj_id']
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			comment = Comment(user=request.user, project=project, text=comment, flags=0)
			comment.save()
			return redirect('/project/' + str(proj_id))
		else:
			return redirect(HOMEPAGE_URL)
	else:
		raise Http404


@login_required
def delete_comment(request):
	if request.method == 'POST':
		if request.POST['comment'] and request.POST['proj_id']:
			comment = request.POST['comment']
			proj_id = request.POST['proj_id']
			# TODO
			return redirect('/project/' + str(proj_id))
		else:
			return redirect(HOMEPAGE_URL)
	else:
		raise Http404

def gallery(request):
	pass


