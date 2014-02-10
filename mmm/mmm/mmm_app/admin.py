from django.contrib import admin
from django.contrib.auth.models import User

from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Category_top, Category_sub

# Register your models here.

# UserInfo
class UserInfoAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)
	fieldsets = (
		('Username', {
			'fields': ('user',)
		}),
		('User Type', {
			'fields': ('is_sponsor', 'is_developer',)
		}),
		('User Settings', {
			'fields': ('setting_0', 'setting_1', 'setting_2',)
		}),
	)
admin.site.register(UserInfo, UserInfoAdmin)

# Developer
class DeveloperAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)
	fieldsets = (
		('User', {
			'fields': ('user', 'image',)
		}),
		('Developer Information', {
			'fields': ('major', 'bio',)
		}),
		('Developer Works', {
			'fields': ('projects',)
		}),
	)
admin.site.register(Developer, DeveloperAdmin)

# Sponsor
class SponsorAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)
	fieldsets = (
		('User', {
			'fields': ('user',)
		}),
		('Sponsor Information', {
			'fields': ('org_name', 'image', 'org_bio',)
		}),
	)
admin.site.register(Sponsor, SponsorAdmin)

# Project
class ProjectAdmin(admin.ModelAdmin):
	fieldsets = (
		('Project Information', {
			'fields': ('title', 'image', 'sponsor', 'description', 'developers',)
		}),
		('Meta Information', {
			'fields': ('date_posted', 'status', 'show_in_gallery', 'likes', 'category_subs',)
		}),
	)	
admin.site.register(Project, ProjectAdmin)

# Comment
class CommentAdmin(admin.ModelAdmin):
	readonly_fields = ('user', 'project', 'date_posted',)
	fieldsets = (
		('User', {
			'fields': ('user',)
		}),
		('Comment Information', {
			'fields': ('title', 'text',)
		}),
		('Meta Information', {
			'fields': ('project', 'date_posted',)
		}),
	)
admin.site.register(Comment, CommentAdmin)

# Category_top
class Category_topAdmin(admin.ModelAdmin):
	readonly_fields = ('name',)
	fieldsets = (
		('Top Level Category', {
			'fields': ('name',)
		}),
	)
admin.site.register(Category_top, Category_topAdmin)

# Category_sub
class Category_subAdmin(admin.ModelAdmin):
	fieldsets = (
		('Top Level Category(s)', {
			'fields': ('top',)
		}),
		('Sub-Category', {
			'fields': ('name',)
		}),
	)
admin.site.register(Category_sub, Category_subAdmin)

