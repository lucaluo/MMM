from django.core.management.base import BaseCommand, CommandError
from mmm.mmm_app.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from datetime import date, timedelta

# send weekly email command
class Command(BaseCommand):
    help = 'Sends the weekly email for MMM to specified users'

    def handle(self, *args, **options):
        # determine date of 1 week ago
		cutoff_date = date.today()-timedelta(days=7)

		# get list of projects added within the last week
		new_projects = Project.objects.filter(approved=True, date_posted__gt = cutoff_date)
		
		# get list of projects that need approval
		unapproved = Project.objects.filter(approved=False)
		
		# check each normal user
		for user in User.objects.filter(is_staff=False):
		#for user in User.objects.filter(username='sloboste'):
		
			userinfo = UserInfo.objects.get(user=user)
			
			# check if user wants email
			if userinfo.weekly_email == True:
			
				# get list of bookmarked projects with comments in the last week
				bookmarked = []
				for p in userinfo.bookmarks.all():
					comments = Comment.objects.filter(project = p, date_posted__gt = cutoff_date)
					if comments:
						bookmarked.append(p)
			
				# get list of sponsored projects with comments in the last week
				sponsored = []
				for p in Project.objects.filter(sponsor=user):
					comments = Comment.objects.filter(project = p, date_posted__gt = cutoff_date)
					if comments:
						sponsored.append(p)
				
				# compile the message
				message_body = render_to_response('weekly_email.txt', {'user': user, 'userinfo': userinfo, 'new_projects': new_projects, 'cutoff_date': cutoff_date, 'bookmarked': bookmarked, 'sponsored': sponsored}).content
				email = EmailMessage('MMM Weekly Update', message_body, 'mmm.umich@gmail.com', (user.email,))
		
				# send the message to user
				email.send(fail_silently=False)
				
		# email site admins about project approval
		for user in User.objects.filter(is_staff=True):
		
			# compile message
			message_body = render_to_response('approve_projects.txt', {'user': user, 'unapproved': unapproved}).content
			email = EmailMessage('MMM Project Approval Update', message_body, 'mmm.umich@gmail.com', (user.email,))
			
			# send message to user
			email.send(fail_silently=False)
		
		return

