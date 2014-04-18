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
LOGIN_URL = '/login/'
REGISTER_URL = '/login/'
PASSWORD_MINLENGTH = 8

# landing page
def landing(request):
	if request.user.is_authenticated():
		# get user info
		userInfo = UserInfo.objects.get(user=request.user)
		# set loggined
		loggined = True
	else:
		# set not loggined
		userInfo = None
		loggined = False
			
	# get all tags
	category_list = getAllCategories()
	
	# message color and contents
	mtype = 'none'
	mcontents = ''
	
	# get list of projects
	projects = Project.objects.filter(status='OP', approved=True).order_by('-date_posted')
	# get filters of projects and sponsor
	project_filters = []
	project_sponsors = []
	for project in projects:
		project_filters.append((project.id, project.category_subs.all()))
		project_sponsors.append((project.id, UserInfo.objects.get(user=project.sponsor)))

	bookmarked = False
	bookmarkedProjects = None
	f_cat_subs_dict = {}
	for x in category_list:
		for cs in x['category_sub_list']:
			f_cat_subs_dict[cs] = False
	af = ''
	
	# filtering on get method
	form = FilterForm(data=request.GET)

	# filter open flag
	filter_open = None

	if loggined and form.is_valid():
		# bookmarked projects
		b = form.cleaned_data['bookmarked']
		bookmarkedProjects = UserInfo.objects.get(user=request.user).bookmarks.all()
		if b:
			projects = bookmarkedProjects
			bookmarked = True
	
		# checkbox filters
		f_cat_subs = form.cleaned_data['f_category_subs']
			
		for cat_sub in f_cat_subs:
			# corresponds to checkbox being checked
			projects = projects.filter(category_subs=cat_sub)
			f_cat_subs_dict[cat_sub] = True
		
		# search box
		af = form.cleaned_data['additional_filter']
		match = False
		if af:
			for cd in category_list:
				for cs in cd['category_sub_list']:
					if cs.name == af:
						projects = projects.filter(category_subs=cs)
						match = True
			if not match:
				newprojects = projects.filter(title__icontains=form.cleaned_data['additional_filter'])
				if not newprojects:
					projects = projects.filter(description__icontains=form.cleaned_data['additional_filter'])
				else:
					projects = newprojects
					
		if not projects:
			mtype = 'alert-danger'
			mcontents = 'No projects matched'
		if request.GET.get('from') and request.GET['from'] == 'form':
			filter_open = True
			
	elif loggined:
		mtype = 'alert-danger'
		mcontents = 'Invalid filters'
		projects = []
	
	args = {
			'filterForm': form, 
			'projects': projects, 
			'category_list': category_list, 
			'message_type': mtype, 
			'message_contents': mcontents, 
			'cat_sub_checked_dict': f_cat_subs_dict, 
			'bookmarked': bookmarked, 
			'additional_filter': af, 
			'bookmarkedProjects': bookmarkedProjects,
			'project_filters': project_filters,
			'project_sponsors': project_sponsors,
			'filter_open': filter_open,
			'userInfo': userInfo,
		}		

	return render(request, 'landing.html', args, context_instance=RequestContext(request))

# returns list of dicts containing the categories
def getAllCategories():
	category_top_list = Category_top.objects.all().order_by('pk')
	category_list = []
	for category_top in category_top_list:
		category = {}
		category['category_top'] = category_top
		category['category_sub_list'] = Category_sub.objects.filter(category_top=category_top)
		category_list.append(category)
	return category_list


# register page
def user_register(request):
	if request.method == 'POST':
		uniqname = request.POST['uniqname']
		password = request.POST['password']
		full_name = request.POST['full_name']
		if not (password and uniqname and full_name):
			mtype = 'alert-danger'
			mcontents = 'Please fill all register fields!'
			return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		if User.objects.filter(username=uniqname).exists():
			mtype = 'alert-danger'
			mcontents = 'Uniqname has been registered!'
			return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		passwordStrength = check_password_strength(request.POST['password'])
		if passwordStrength:
			mtype = 'alert-danger'
			mcontents = passwordStrength
			return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		email = uniqname + '@umich.edu'
		user = User.objects.create_user(username=uniqname, password=password, email=email)
		user.is_active = False
		user.save()
		userInfo = UserInfo(user=user, full_name=full_name, weekly_email=True,)
		userInfo.save()
		send_verify_email(request, uniqname, email)
		mtype = 'alert-success'
		mcontents = 'Please check your email for an activation link!'
		return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
	else:
		return redirect(REGISTER_URL)


# send the account verification email
def send_verify_email(request, username, email):
	activation_code = generate_actication_code(username)
	verify_url = request.build_absolute_uri('/activate/' + username + '/' + activation_code)
	user = User.objects.get(username=username)
	userInfo = UserInfo.objects.get(user=user)
	send_mail('Michigan Mobile Manufactory User Verification', render(request, 'email_verification.txt', {'user': user, 'userInfo': userInfo, 'verify_url': verify_url}).content, 'mmm.umich@gmail.com', [email], fail_silently=False)



# activate user function
def user_activate(request, username, activation_code):
	if activation_code == generate_actication_code(username):
		user = User.objects.get(username=username)
		user.is_active = True
		user.save()
		return redirect(LOGIN_URL)
	else:
		return redirect(REGISTER_URL)



# getnerate activation code function
def generate_actication_code(username):
	return hashlib.sha256(username[0] + username[-1] + username).hexdigest()



# login the user
def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if request.POST.get('next'):
			next = request.POST['next']
		else:
			next = HOMEPAGE_URL
		if not (username and password):
			mtype = 'alert-danger'
			mcontents = 'Please fill your uniqname and password!'
			return render(request, 'login.html', {'next': next, 'username': username, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(next);
			else:
				mtype = 'alert-danger'
				mcontents = 'Account is not activated!'
				return render(request, 'login.html', {'next': next, 'username': username, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		else:
			mtype = 'alert-danger'
			mcontents = 'The user does not exists!'
			return render(request, 'login.html', {'next': next, 'username': username, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
	else:
		if request.GET.get('next'):
			next = request.GET['next']
		else:
			next = HOMEPAGE_URL
		if request.user.is_authenticated():
			return redirect(next)
		else:
			return render(request, 'login.html', {'next': next}, context_instance=RequestContext(request))



#logout the user
def user_logout(request):
	logout(request)
	# redirect to homepage
	return redirect(HOMEPAGE_URL)



# profile page
@login_required
def profile(request, prof_id):
	mtype = 'none'
	mcontents = ''
	if request.method == 'POST':
		if prof_id == str(request.user.id):
			# bound form
			form = ProfileForm(request.POST, request.FILES)
			if form.is_valid():
				try:
					# get user and userInfo to edit
					userInfo = UserInfo.objects.get(user=request.user)
				except UserInfo.DoesNotExist:
					raise Http404
					
				# this is the cleaned data
				full_name = form.cleaned_data['full_name']
				major = form.cleaned_data['major']
				bio = form.cleaned_data['bio']
				# weekly_email = form.cleaned_data['weekly_email']
				# update models in db
				userInfo.full_name = full_name
				userInfo.major = major
				userInfo.bio = bio
				# userInfo.weekly_email = weekly_email
				if request.FILES.get('image'):
					userInfo.image = request.FILES['image']
				try:
					userInfo.save()
					# message color and contents
					mtype = 'alert-success'
					mcontents = 'Profile successfully updated'
				except userInfo.DoesNotExist: # what other errors could occur?
					# message color and contents
					mtype = 'alert-danger'
					mcontents = 'Profile could not be updated'
				# get sponsored projects
				projects = Project.objects.filter(sponsor=prof_id)
				#return redirect('/profile/' + prof_id + '/')
				return render(request, 'profile.html', {'userInfoObj': userInfo, 'profileEditForm':form, 'projects': projects, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
			else:
				mtype = 'alert-danger'
				mcontents = 'Edit is not valid!'
				print form.errors
		else:
			mtype = 'alert-danger'
			mcontents = 'User does not have permission to edit!'
			print request.user.id
	# GET request
	try:
		# get user and userInfo to edit
		userInfo = UserInfo.objects.get(user=request.user)
	except UserInfo.DoesNotExist:
		raise Http404
	# unbound form
	form = ProfileForm()
	# get info
	userInfo = UserInfo.objects.get(user=prof_id)
	# get sponsored projects
	projects = Project.objects.filter(sponsor=prof_id)
	# render
	return render(request, 'profile.html', {'userInfoObj': userInfo, 'profileEditForm':form, 'projects': projects, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))



# new project page
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
							approved=False,
							description=form.cleaned_data['description'], 
							flags=0,
						)
			project.save()
			if request.FILES.get('image'):
				project.image = request.FILES['image']
			if request.POST.get('in_gallery'):
				project.show_in_gallery = True
			else:
				project.show_in_gallery = False
			for category_sub in form.cleaned_data['category_subs']:
				project.category_subs.add(category_sub)
			project.save()
			return redirect(HOMEPAGE_URL)
		else:
			print 'not valid'
			return redirect(HOMEPAGE_URL)
	else:
		return redirect(HOMEPAGE_URL)



# project details page
@login_required
def project(request, proj_id):
	if request.method == 'POST':
		form = ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			if project.sponsor == request.user:
				project.title = form.cleaned_data['title']
				project.description = form.cleaned_data['description']
				if request.POST.get('status'):
					project.status = request.POST['status']
				if request.POST.get('in_gallery'):
					project.show_in_gallery = True
				else:
					project.show_in_gallery = False
				if request.FILES.get('image'):
					project.image = request.FILES['image']
				project.category_subs.through.objects.all().delete()
				for category_sub in form.cleaned_data['category_subs']:
					project.category_subs.add(category_sub)
				project.save()
				return redirect('/project/' + proj_id + "/")
			else:
				print 'no permission'
		else:
			print 'not valid'
	else: # GET
		try:
			project = Project.objects.get(id=proj_id)
		except Project.DoesNotExist:
			raise Http404
		sponsor = UserInfo.objects.get(user=project.sponsor)
		category_subs = project.category_subs.all()
		category_sub_ids = [category_sub.id for category_sub in category_subs]
		comments = Comment.objects.filter(project=project)
		commentsObj = []
		for comment in comments:
			commentObj = {'comment': comment, 'commenter': UserInfo.objects.get(user=comment.user)}
			commentsObj.append(commentObj)
		category_list = getAllCategories()
		if project in UserInfo.objects.get(user=request.user).bookmarks.all():
			is_bookmarked = True
		else:
			is_bookmarked = False
		return render(request, 'projDetails.html', {'project': project, 'sponsor': sponsor, 'category_subs': category_subs, 'commentsObj': commentsObj, 'category_list': category_list, 'category_sub_ids': category_sub_ids, 'is_bookmarked': is_bookmarked}, context_instance=RequestContext(request))



# apply to project function
@login_required
def apply_project(request):
	if request.method == 'POST':
		if request.POST['message'] and request.POST['proj_id']:
			message = request.POST['message']
			proj_id = request.POST['proj_id']
			applier = request.user
			applierInfo = UserInfo.objects.get(user=applier)
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			sponsorInfo = UserInfo.objects.get(user=project.sponsor)
			profile_url = request.build_absolute_uri('/profile/' + str(applier.id) + '/')
			project_url = request.build_absolute_uri('/project/' + str(proj_id) + '/')
			sponsor_email = EmailMessage('Project Application on Michigan Mobile Manufactory', render(request, 'email_sponsor.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url, 'applierInfo': applierInfo, 'sponsorInfo': sponsorInfo}).content, 'mmm.umich@gmail.com', [project.sponsor.email], [], headers = {'Reply-To': applier.email})
			sponsor_email.send(fail_silently=False)
			applier = EmailMessage('Confirmation of Project Application on Michigan Mobile Manufactory', render(request, 'email_applier.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url, 'applierInfo': applierInfo, 'sponsorInfo': sponsorInfo}).content, 'mmm.umich@gmail.com', [applier.email], [])
			applier.send(fail_silently=False)
			return redirect(HOMEPAGE_URL)
		else:
			return redirect(HOMEPAGE_URL)
	else:
		raise Http404



# post new comment function
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



# delete existing comment function
@login_required
def delete_comment(request, proj_id, comm_id):
	try:
		comment = Comment.objects.get(id=comm_id)
		if str(comment.project.id) != proj_id:
			# TODO error message comment and proejct id not correspond
			print "comment and proejct id not correspond"
		elif comment.user != request.user:
			# TODO no permission to delete this comment
			print "no permission to delete this comment"
		else:
			comment.delete()
			return redirect('/project/' + proj_id + '/')
	except Comment.DoesNotExist:
		# TODO error message comment to delete not exists
		print "error message comment to delete not exists"



# bookmark project function
@login_required
def bookmark(request, proj_id):
	try:
		project = Project.objects.get(id=proj_id)
	except Project.DoesNotExist:
		raise Http404
	userInfo = UserInfo.objects.get(user=request.user)
	if project not in userInfo.bookmarks.all():
		userInfo.bookmarks.add(project)
	redirectUrl = '/project/' + proj_id + '/'
	if request.META.get('HTTP_REFERER'):
		redirectUrl = request.META['HTTP_REFERER']
	return redirect(redirectUrl)



# unbookmark project function
@login_required
def unbookmark(request, proj_id):
	try:
		project = Project.objects.get(id=proj_id)
	except Project.DoesNotExist:
		raise Http404
	userInfo = UserInfo.objects.get(user=request.user)
	if project in userInfo.bookmarks.all():
		userInfo.bookmarks.remove(project)
	redirectUrl = '/project/' + proj_id + '/'
	if request.META.get('HTTP_REFERER'):
		redirectUrl = request.META['HTTP_REFERER']
	return redirect(redirectUrl)


# settings page
@login_required
def editSettings(request):
	try:
		userInfo = UserInfo.objects.get(user=request.user)
	except UserInfo.DoesNotExist:
		raise Http404
		
	if request.method == 'POST':
		form = SettingsForm(request.POST)
		if form.is_valid():
			userInfo.weekly_email = form.cleaned_data['weekly_email']
			userInfo.save()
		else:
			print 'invlaid settings form'
	return redirect(HOMEPAGE_URL)

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordForm(request.POST)
		if form.is_valid():
			user = authenticate(username=request.user.username, password=form.cleaned_data['old_password'])
			if user is not None and user.is_active:
				strenghMessage = check_password_strength(form.cleaned_data['new_password'])
				if form.cleaned_data['new_password'] != form.cleaned_data['confirm_password']:
					print 'password not match'
				elif strenghMessage:
					print strenghMessage
				else:
					user.set_password(form.cleaned_data['new_password'])
					user.save()
			else:
				print 'wrong password'
		else:
			print 'invlaid password form'
	return redirect(HOMEPAGE_URL)

def check_password_strength(password):
	if len(password) < PASSWORD_MINLENGTH:
		return 'Password too short.'
	hasNumeric = False
	hasAlphabet = False
	for c in password:
		if c >= '0' and c <= '9':
			hasNumeric = True
		if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
			hasAlphabet = True

	if not hasNumeric:
		return 'Password must contain at least one numeric value.'
	if not hasAlphabet:
		return 'Password must contain at least one alphabet.'
	return None


# gallery page (unimplemented)
@login_required
def gallery(request):
	pass

