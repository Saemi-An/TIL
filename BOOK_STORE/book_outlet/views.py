from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from .models import Book
# Create your views here.

def index(request):
    books = Book.objects.all().order_by("-rating")
    total_books = books.count()
    avg_rating = books.aggregate(Avg("rating"))

    return render(request, "book_outlet/index.html", {
        "books" : books,
        "total_books" : total_books,
        "avg_rating" : avg_rating,
    })

def book_detail(request, slug):
    # 숏컷
    book = get_object_or_404(Book, slug=slug)
    
    # 전통적인 방식
    # try:
    #     book = Book.objects.get(pk=id)
    # except:
    #     raise Http404()

    return render(request, "book_outlet/book_detail.html", {
        "title" : book.title,
        "author" : book.author,
        "rating" : book.rating,
        "is_bestseller" : book.is_bestselling,
    })
