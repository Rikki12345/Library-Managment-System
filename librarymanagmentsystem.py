import json 

class Book:
    def __init__(self, title, author, ISBN, copies):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.copies = copies

    #Returns a human-readable string representation of the book
    def __str__(self):
        return f"Book: {self.title} by {self.author}, ISBN: {self.ISBN}, Copies: {self.copies}"
    #Returns a developer-friendly string representation of the book.
    def __repr__(self):
        return f"Book({self.title}, {self.author}, {self.ISBN}, {self.copies})"
    #Converts the book's attributes to a dictionary.
    def to_dict(self):
        return {"title": self.title, "author": self.author, "ISBN": self.ISBN, "copies": self.copies}
    #Class method to create a Book instance from a dictionary.
    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['author'], data['ISBN'], data['copies'])

class Member:
    # Constructor to initialize the member's attributes.
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    #Returns a human-readable string representation of the member.
    def __str__(self):
        return f"Member: {self.name}, ID: {self.member_id}, Borrowed Books: {len(self.borrowed_books)}"
    #Returns a developer-friendly string representation of the member.
    def __repr__(self):
        return f"Member({self.name}, {self.member_id } Borrowed Books,{len(self.borrowed_books)}"
    #Adds a book to the member's borrowed books if available
    def borrow_book(self, book):
        if book.copies > 0:
            self.borrowed_books.append(book.ISBN)
            book.copies -= 1
            print(f"{self.name} borrowed {book.title}")
        else:
            print(f"Sorry, {book.title} is not available.")
    #Removes a book from the member's borrowed books.
    def return_book(self, book):
        if book.ISBN in self.borrowed_books:
            self.borrowed_books.remove(book.ISBN)
            book.copies += 1
            print(f"{self.name} returned {book.title}")
        else:
            print(f"{self.name} did not borrow {book.title}")
    #Returns the number of borrowed books.
    def __len__(self):
        return len(self.borrowed_books)
    #Converts the member's attributes to a dictionary.
    def to_dict(self):
        return {"name": self.name, "member_id": self.member_id, "borrowed_books": self.borrowed_books}
    #Class method to create a Member instance from a dictionary.
    @classmethod
    def from_dict(cls, data):
        member = cls(data['name'], data['member_id'])
        member.borrowed_books = data['borrowed_books']
        return member

class Library:
    #Constructor to initialize the library's attributes.
    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = []
    #Returns a human-readable string representation of the library.
    def __str__(self):
        return f"Library: {self.name}, Books: {len(self.books)}, Members: {len(self.members)}"
    #Returns a developer-friendly string representation of the library.
    def __repr__(self):
        return f"Library({self.name})"
        #Adds a book to the library.
    def add_book(self, book):
        if book.ISBN in self.books:
            self.books[book.ISBN].copies += book.copies
        else:
            self.books[book.ISBN] = book
        print(f"Added {book.title} to the library.")
    #Removes a book from the library.
    def remove_book(self, book):
        if book.ISBN in self.books:
            del self.books[book.ISBN]
            print(f"Removed {book.title} from the library.")
        else:
            print(f"{book.title} not found in the library.")
    #Adds a member to the library.
    def add_member(self, member):
        self.members.append(member)
        print(f"Added member {member.name} to the library.")
    #Removes a member from the library
    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
            print(f"Removed member {member.name} from the library.")
        else:
            print(f"Member {member.name} not found in the library.")
    #Lends a book to a member.
    def lend_book(self, member, book):
        if book.ISBN in self.books:
            member.borrow_book(self.books[book.ISBN])
        else:
            print(f"{book.title} not available in the library.")
    #Returns a book from a member.
    def return_book(self, member, book):
        if book.ISBN in self.books:
            member.return_book(self.books[book.ISBN])
        else:
            print(f"{book.title} not recognized by the library.")
    #Returns the number of books in the library.
    def __len__(self):
        return len(self.books)
    #Converts the library's attributes to a dictionary.
    def to_dict(self):
        return {
            "name": self.name,
            "books": {ISBN: book.to_dict() for ISBN, book in self.books.items()},
            "members": [member.to_dict() for member in self.members]
        }
    #aves the library's state to a JSON file.
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)
    #Loads the library's state from a JSON file.
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    #Class method to create a Library instance from a dictionary.
    @classmethod
    def from_dict(cls, data):
        library = cls(data['name'])
        library.books = {ISBN: Book.from_dict(book_data) for ISBN, book_data in data['books'].items()}
        library.members = [Member.from_dict(member_data) for member_data in data['members']]
        return library

class EBook(Book):
    #Constructor to initialize the eBook's attributes.
    def __init__(self, title, author, ISBN, copies, file_format):
        super().__init__(title, author, ISBN, copies)
        self.file_format = file_format
    #Returns a human-readable string representation of the eBook, including the file format.
    def __str__(self):
        return f"EBook: {self.title} by {self.author}, ISBN: {self.ISBN}, Copies: {self.copies}, Format: {self.file_format}"
    #Returns a developer-friendly string representation of the eBook, including the file format.
    def __repr__(self):
        return f"EBook({self.title}, {self.author}, {self.ISBN}, {self.copies}, {self.file_format})"
    #Converts the eBook's attributes to a dictionary, including the file format.
    def to_dict(self):
        book_dict = super().to_dict()
        book_dict['file_format'] = self.file_format
        return book_dict
    #Class method to create an EBook instance from a dictionary.
    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['author'], data['ISBN'], data['copies'], data['file_format'])

# Load library data from JSON file
library = Library.load_from_file('library.json')

print(library)
for member in library.members:
    print(member)
