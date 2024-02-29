from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from catalog.models import Book, Genre, Language

api = NinjaAPI()


class BookIn(Schema):
    title: str
    author_id: int  # Assuming author_id is used to reference the author
    summary: str
    isbn: str
    genre_ids: List[int] = None  # Assuming genre_ids is used to reference multiple genres
    language_id: int = None


class BookOut(Schema):
    id: int
    title: str
    author_id: int
    summary: str
    isbn: str
    genre_ids: List[int] = None
    language_id: int = None


@api.post("/books")
def create_book(request, payload: BookIn):
    book = Book.objects.create(**payload.dict())
    return {"id": book.id}


@api.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    return book


@api.get("/books", response=List[BookOut])
def list_books(request):
    qs = Book.objects.all()
    return qs


@api.put("/books/{book_id}")
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return {"success": True}


@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}
