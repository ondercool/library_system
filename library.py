import time
import os
import tkinter
import customtkinter
class Library():
    def __init__(self):
        with open("library_project/books.txt","a+") as f:
            pass

    def add_book(self, name, author, release_date, pages):
        with open("library_project/books.txt", "a+") as f:
            book_data = f"{name},{author},{release_date},{pages}\n"
            f.write(book_data)
        
    def list_books(self)->bool:
        if os.path.exists("library_project/books.txt"):
            with open("library_project/books.txt","r") as f:
                books = [book for book in f.read().splitlines()]
                if len(books) == 0:
                    return False
                else:
                    return books
        else:
            return False
    
    def remove_book(self, book_title)->bool:
        removed = False
        with open("library_project/books.txt","r") as f:
            books = [book for book in f.read().splitlines()]
            for book in books:
                meta_data = book.split(",")
                if meta_data[0].lower() == book_title.lower():
                    books.remove(book)
                    removed = True

            if removed:
                with open("library_project/books.txt","w") as f:
                    for book in books:
                        meta_data = book.split(",")
                        self.add_book(meta_data[0], meta_data[1], meta_data[2], meta_data[3])

        return removed

    def remove_object(self):
        if os.path.exists("library_project/books.txt"):
            os.remove("library_project/books.txt")
        
    
            
            
            


