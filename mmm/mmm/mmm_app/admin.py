from django.contrib import admin

from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Tag

# Register your models here.

# UserInfo
class UserInfoAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(UserInfo, UserInfoAdmin)

# Developer
class DeveloperAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Developer, DeveloperAdmin)

# Sponsor
class SponsorAdmin(admin.ModelAdmin):
	pass

admin.site.register(Sponsor, SponsorAdmin)

# Project
class ProjectAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Project, ProjectAdmin)

# Comment
class CommentAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Comment, CommentAdmin)

# Tag
class TagAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Tag, TagAdmin)

