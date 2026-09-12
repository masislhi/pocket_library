import pytest
import requests
import os
from project import Book, read, search_books, create_books, extract_book_data

def test_read():
    if os.path.exists("to_read.csv"):
        os.remove("to_read.csv")
    books = create_books(extract_book_data(search_books("title","dune",10,1)))
    with pytest.raises(ValueError):
        read(books[0],50)
    books[0].add_list()
    with pytest.raises(ValueError):
        read(books[0],-50)
    with pytest.raises(ValueError):
        read(books[1],50)


    read(books[0], 50)
    read(books[0], 70)

    with open("to_read.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()

    assert lines[1].strip().endswith(",100")
    if os.path.exists("to_read.csv"):
        os.remove("to_read.csv")

def test_add_list():
    
    books = create_books(extract_book_data(search_books("title","dune",10,1)))
    assert books[1].add_list() == True
    assert books[1].add_list() == False
    if os.path.exists("to_read.csv"):
        os.remove("to_read.csv")

def test_del_list():
    books = create_books(extract_book_data(search_books("title","dune",10,1)))
    with pytest.raises(ValueError):
        books[5].del_list()
    books[5].add_list()
    books[3].add_list()
    books[5].del_list()
    with pytest.raises(ValueError):
        books[5].del_list()
    if os.path.exists("to_read.csv"):
        os.remove("to_read.csv")
    

def test_search_books_error(monkeypatch):

    def fake_get(*args, **kwargs):
        raise requests.RequestException

    monkeypatch.setattr(requests, "get", fake_get)

    assert search_books("title", "dune", 10, 1) is None
    


    
