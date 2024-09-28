from django.contrib import admin
from .models import Tag, Author, Post

# Register your models here.

class YourBlogAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, YourBlogAdmin)
admin.site.register(Author)
admin.site.register(Tag)
