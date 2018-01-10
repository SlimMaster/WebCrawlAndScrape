from django.contrib import admin
from .models import Comment
# Register your models here.

# class CommentModelAdmin(admin.ModelAdmin):
# 	list_display = ["title","update","timestamp"]
# 	class Meta:
# 		model = Post



admin.site.register(Comment)#,PostModelAdmin)