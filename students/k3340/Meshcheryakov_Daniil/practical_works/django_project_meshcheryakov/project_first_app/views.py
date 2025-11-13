from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book

def book_list(request):
    query = request.GET.get("q", "")
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    paginator = Paginator(books, 5)  # 5 книг на странице
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "books/book_list.html", {"page_obj": page_obj, "query": query})
