from django.contrib import admin
from .models import Tag, Author, Post

# Register your models here.

class YourBlogAdmin(admin.ModelAdmin):
    pass   # For the extra configurations

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date",)   # 필터
    list_display = ("title", "date", "author",)   # 테이블 컬럼
    prepopulated_fields = {"slug" : ("title",)}



admin.site.register(Post, PostAdmin)   # 두번째 인자로 추가
admin.site.register(Author)
admin.site.register(Tag)
