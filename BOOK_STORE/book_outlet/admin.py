from django.contrib import admin
from .models import Book, Author, Address, Country

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # readonly_fields = ("slug",)   # 읽기 전용으로 만들 클래스 속성들을 튜플로 작성 (must be tuple)
    prepopulated_fields = {"slug" : ("title",)}
    list_filter = ("author", "rating", "is_bestselling",)
    list_display = ("title", "author", "rating",)

admin.site.register(Book, BookAdmin)   # Book 모델을 어드민에서 보여줘라
admin.site.register(Author)
admin.site.register(Address)
admin.site.register(Country)
