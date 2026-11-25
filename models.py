"""Data models for the Library Management System."""
from dataclasses import dataclass


@dataclass
class Book:
    """Represent one book in the library."""
    book_id: str
    title: str
    author: str
    available: bool = True

    def is_available(self):
        """Return True if the book can be borrowed."""
        return self.available

    def borrow(self):
        """Mark this book as borrowed."""
        if not self.available:
            raise ValueError("This book is already borrowed.")
        self.available = False

    def return_book(self):
        """Mark this book as available again."""
        if self.available:
            raise ValueError("This book is not currently borrowed.")
        self.available = True

    def to_dict(self):
        """Convert the book into a dictionary for CSV storage."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "available": str(self.available),
        }


@dataclass
class Member:
    """Represent a registered library member."""
    member_id: str
    name: str
    email: str

    def borrow_book(self, book_id):
        """Record a borrowed book in this member's list."""
        if book_id in self.borrowed_books:
            raise ValueError("This member has already borrowed this book.")
        self.borrowed_books.append(book_id)

    def return_book(self, book_id):
        """Remove a returned book from this member's list."""
        if book_id not in self.borrowed_books:
            raise ValueError("This member has not borrowed this book.")
        self.borrowed_books.remove(book_id)

    def to_dict(self):
        """Convert the member into a dictionary for CSV storage."""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": ";".join(self.borrowed_books),
        }

    @classmethod
    def from_dict(cls, row):
        """Create a member from a CSV dictionary."""
        member = cls(row["member_id"], row["name"], row["email"])
        member.borrowed_books = [
            item for item in row.get("borrowed_books", "").split(";") if item
        ]
        return member

    def __post_init__(self):
        """Create the list used to track this member's borrowed books."""
        self.borrowed_books = []
