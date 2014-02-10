from django.contrib import admin

from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Category_top, Category_sub

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

# Category_top
class Category_topAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Category_top, Category_topAdmin)

# Category_sub
class Category_subAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Category_sub, Category_subAdmin)

