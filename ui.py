import tkinter
import customtkinter
import time
from library import Library

class LibraryInterface(customtkinter.CTk):
    def __init__(self, library:Library):
        super().__init__()
        #window sections 
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.library = library

        self.table_cells = None

        self.geometry("800x1000")
        self.title("Library Interface")

        self.add_button = customtkinter.CTkButton(self, text="Add Book", font=("Inter",24), 
                                                  border_color="white",corner_radius=5,
                                                  border_width=3, width=760,
                                                  bg_color="white", height=40, command=self.open_book_add_window
                                                  )
        self.add_button.grid(column=0, row=0, padx=20,columnspan=8)

        self.remove_button = customtkinter.CTkButton(self, text="Remove Book", font=("Inter",24), border_color="white"
                                                     ,corner_radius=5, border_width=3, 
                                                     width=760,bg_color="white", height=40, command=self.open_book_remove_window
                                                     )
        self.remove_button.grid(column=0, row=1, padx=20, columnspan=8)

        self.list_button = customtkinter.CTkButton(self, text="List Books", font=("Inter",24), 
                                                   border_color="white",corner_radius=5,
                                                   border_width=3, width=760,bg_color="white", height=40,
                                                   command=self.table_list_books)
        self.list_button.grid(column=0, row=2, padx=20,columnspan=8)

        self.delete_button = customtkinter.CTkButton(self, text="Delete", 
                                                     font=("Roboto",24), border_color="white",corner_radius=5, 
                                                     border_width=3, width=100,bg_color="white", height=40,command=self.delete_library
                                                     )
        self.delete_button.grid(row=3,column=5,columnspan=2, padx=50, pady=20)

        self.log_label = customtkinter.CTkLabel(self, text=None, text_color="black",font=("Roboto",25,"bold"),justify="center")
        self.log_label.grid(row=4,column=0,columnspan=8,padx=50,pady=20)

        self.book_add_window = None
        self.book_remove_window = None
        self.library_remove_window = None

    def open_book_add_window(self):
        if self.book_add_window is None or not self.book_add_window.winfo_exists():
            self.book_add_window = book_add_window(self)
            
    def open_book_remove_window(self):
        if self.book_remove_window is None or not self.book_remove_window.winfo_exists():
            self.book_remove_window = book_remove_window(self)

    def pass_book_data(self):
        if self.book_add_window is not None:
            name = self.book_add_window.name_input.get()
            author = self.book_add_window.author_input.get()
            publish_date = self.book_add_window.publish_input.get()
            pages = self.book_add_window.page_input.get()

            if name == "" or author == "" or publish_date == "" or pages == "":
                self.book_add_window.error_text = "None of the input fields can be left empty!!!"
                self.book_add_window.raise_error()

            else:
                self.log_label.configure(text="", text_color="black")
                self.clear_table()

                self.book_add_window.clear_error()
                self.library.add_book(name, author, publish_date, pages)

                self.book_add_window.confirm_addition()
                self.book_add_window.name_input.delete(0,customtkinter.END)
                self.book_add_window.author_input.delete(0,customtkinter.END)
                self.book_add_window.publish_input.delete(0,customtkinter.END)
                self.book_add_window.page_input.delete(0,customtkinter.END)

                self.book_add_window
                self.book_add_window.name_input.focus()

    def pass_remove_book_data(self):
        if self.book_remove_window is not None:
            name = self.book_remove_window.name_input.get()
            if name == "":
                self.book_remove_window.error_text = "Please enter the book name!!!"
                self.book_remove_window.raise_error()
            
            else:
                self.book_remove_window.clear_log()
                is_removed = self.library.remove_book(name)
                if is_removed:
                    self.clear_table()
                    self.book_remove_window.confirm_submission()
                else:
                    self.book_remove_window.raise_not_found_error()
    
    def table_list_books(self):
        self.label_params = {"master":self, "width":300, "height":50, "text_color":"red", "font":("Roboto",20),}

        self.name_header = customtkinter.CTkButton(text="Book Name",master=self,width=300,
                                                  height=50,border_width=3,
                                                  text_color="white",
                                                  font=("Roboto",24,"bold"),
                                                  hover="False",border_color="white",bg_color="white")
        self.author_header = customtkinter.CTkButton(text="Author Name",master=self,width=300,
                                                  height=50,border_width=3,
                                                  text_color="white",
                                                  font=("Roboto",24,"bold"),
                                                  hover="False",border_color="white",bg_color="white")

        self.table_cells = [(self.name_header, self.author_header)]

        output = self.library.list_books()
        if output == False:
            self.clear_table()
            self.log_label.configure(text="There is no book in the database add some!!!", text_color="red")
        else:
            self.table_cells = [(self.name_header, self.author_header)]
            self.name_header.grid(row=5, column=1,columnspan=3)
            self.author_header.grid(row=5, column=4, columnspan=3)

            self.log_label.configure(text=f"{len(output)} books will be listed", text_color="white")
            row_count = 6
            for book in output:
                meta_data = book.split(",")
                name_cell = customtkinter.CTkButton(text=meta_data[0],master=self,width=300,
                                                        height=30,border_width=3,
                                                        text_color="white",
                                                        font=("Roboto",20),
                                                        hover="False",border_color="white",bg_color="white")
            
                author_cell = customtkinter.CTkButton(text=meta_data[1],master=self,width=300,
                                                        height=30,border_width=3,
                                                        text_color="white",
                                                        font=("Roboto",20),
                                                        hover="False",border_color="white",bg_color="white")
                name_cell.grid(row=row_count, column=1,columnspan=3)
                author_cell.grid(row=row_count, column=4,columnspan=3)
                self.table_cells.append((name_cell, author_cell))

                row_count+=1
                
    def delete_library(self):
        self.clear_table()
        self.library.remove_object()
        self.log_label.configure(text=f"Library was deleted, all buttons are disabled")

        #disable buttons:
        self.add_button.configure(state="disabled")
        self.remove_button.configure(state="disabled")
        self.list_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")

            
    def clear_table(self):
        self.log_label.configure(text="", text_color="black")
        if self.table_cells is not None:
            for name_cell, author_cell in self.table_cells:
                name_cell.destroy()
                author_cell.destroy()
class book_add_window(customtkinter.CTkToplevel):
        def __init__(self, parent_window:LibraryInterface):
            #self.configure(title="Add Book")
            super().__init__()
            self.geometry("600x300")
            self.parent = parent_window
            self.error_text = None
            #name label
            self.name_label = customtkinter.CTkLabel(self, text="Book Name: ", font=("Roboto",20,"bold"), justify="left")
            self.name_input = customtkinter.CTkEntry(self, placeholder_text="Name of the book", 
                                                     placeholder_text_color="gray",width=380,
                                                     font=("Roboto",15,"italic"),
                                                     )
            self.name_label.grid(column=0, row=0)
            self.name_input.grid(column=1, row=0)


            #author label
            self.author_label = customtkinter.CTkLabel(self, text="Author: ", font=("Roboto",20,"bold"), justify="left")
            self.author_input = customtkinter.CTkEntry(self, placeholder_text="Author of the book", 
                                                     placeholder_text_color="gray",width=380,
                                                     font=("Roboto",15,"italic"),
                                                     )
            self.author_label.grid(column=0, row=1)
            self.author_input.grid(column=1, row=1)

            #Publish year
            self.publish_label = customtkinter.CTkLabel(self, text="Publish Year: ", font=("Roboto",20,"bold"), justify="left")
            self.publish_input = customtkinter.CTkEntry(self, placeholder_text="Publish year of the book", 
                                                     placeholder_text_color="gray",width=380,
                                                     font=("Roboto",15,"italic"),
                                                     )
            self.publish_label.grid(column=0, row=2)
            self.publish_input.grid(column=1, row=2)

            #Number of Pages
            self.page_label = customtkinter.CTkLabel(self, text="Pages: ", font=("Roboto",20,"bold"), justify="left")
            self.page_input = customtkinter.CTkEntry(self, placeholder_text="Number of pages", 
                                                     placeholder_text_color="gray",width=380,
                                                     font=("Roboto",15,"italic"),
                                                     )
            self.page_label.grid(column=0, row=3)
            self.page_input.grid(column=1, row=3)

            self.error_label = customtkinter.CTkLabel(self, text="", text_color="black",font=("Roboto",20,"italic"))
            self.error_label.grid(column=0,row=4,columnspan=2,pady=20)

            #submit button
            
            self.submit_button = customtkinter.CTkButton(self,text="Add Book", font=("Inter",24), 
                                                  border_color="white",corner_radius=5,
                                                  border_width=3, width=90,
                                                  bg_color="white", height=30,command=self.parent.pass_book_data)
            self.submit_button.grid(row=5, column=0,columnspan=2,padx=255, pady=60)
            
        def raise_error(self):
            self.error_label.configure(text=self.error_text,text_color="red")

        def clear_error(self):
            self.error_label.configure(text="",text_color="black")

        def confirm_addition(self):
            self.error_label.configure(text=f'"{self.name_input.get()}" successfully added', text_color="green")
class book_remove_window(customtkinter.CTkToplevel):
    def __init__(self, parent_window:LibraryInterface):
        super().__init__()
        self.error_text = None
        self.minsize(width=600, height=300)
        self.geometry("600X300")
        self.parent = parent_window
        self.name_label = customtkinter.CTkLabel(self, text="Enter Book Title:", font=("Roboto",20,"bold"),justify="center",width=600)
        self.name_input = customtkinter.CTkEntry(self, placeholder_text="Name of the book", 
                                                    placeholder_text_color="gray", height=40, width=500,justify="center",
                                                    font=("Roboto",15,"italic"),
                                                     )
        self.name_label.grid(row=0,column=0,pady=10)
        self.name_input.grid(row=1,column=0)

        self.submit_button = customtkinter.CTkButton(self,text="Remove", font=("Inter",24), 
                                                border_color="white",corner_radius=5,
                                                border_width=3, width=90,
                                                bg_color="white", height=30, command=self.parent.pass_remove_book_data)
        self.submit_button.grid(row=2, column=0, padx=255, pady=20)

        self.error_label = customtkinter.CTkLabel(self, text="", text_color="black",font=("Roboto",25,"italic"),justify="center", width=600)
        self.error_label.grid(row=3,column=0,pady=20)

    def raise_error(self):
        self.error_label.configure(text=self.error_text,text_color="red")

    def clear_log(self):
        self.error_label.configure(text=None, text_color="black")
    
    def confirm_submission(self):
        self.error_label.configure(text="Book successfully removed", text_color="green")
    
    def raise_not_found_error(self):
        self.error_text = "Book does not exist in the database"
        self.raise_error()
