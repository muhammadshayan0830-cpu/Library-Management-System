"""Library operations and librarian actions."""
import csv
from pathlib import Path

from models import Book, Member


class Librarian:
    """Provide staff actions for managing the library."""

    def __init__(self, name):
        self.name = name

    def add_book(self, library, book):
        """Ask the library to store a new book."""
        library.add_book(book)

    def remove_book(self, library, book_id):
        """Ask the library to remove a book."""
        library.remove_book(book_id)

    def register_member(self, library, member):
        """Ask the library to register a member."""
        library.register_member(member)

    def show_catalogue(self, library):
        """Return the current catalogue."""
        return library.list_books()


class Library:
    """Store books and members and coordinate borrowing."""

    def __init__(self, data_folder="data"):
        self.books = {}
        self.members = {}
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(exist_ok=True)

    def add_book(self, book):
        """Add a book, preventing duplicate IDs."""
        if book.book_id in self.books:
            raise ValueError("A book with this ID already exists.")
        self.books[book.book_id] = book

    def remove_book(self, book_id):
        """Remove a book only when it is not borrowed."""
        book = self._get_book(book_id)
        if not book.is_available():
            raise ValueError("Return the book before removing it.")
        del self.books[book_id]

    def register_member(self, member):
        """Register a member, preventing duplicate IDs."""
        if member.member_id in self.members:
            raise ValueError("A member with this ID already exists.")
        self.members[member.member_id] = member

    def list_books(self):
        """Return books as a list."""
        return list(self.books.values())

    def search_books(self, search_term):
        """Find books whose title or author contains the search term."""
        term = search_term.casefold()
        return [
            book for book in self.books.values()
            if term in book.title.casefold() or term in book.author.casefold()
        ]

    def borrow_book(self, book_id, member_id):
        """Lend a book to a registered member."""
        book = self._get_book(book_id)
        member = self._get_member(member_id)
        book.borrow()
        try:
            member.borrow_book(book_id)
        except ValueError:
            book.return_book()
            raise

    def return_book(self, book_id, member_id):
        """Record a book return for the correct member."""
        book = self._get_book(book_id)
        member = self._get_member(member_id)
        member.return_book(book_id)
        book.return_book()

    def save_data(self):
        """Save books and members to separate CSV files."""
        books_path = self.data_folder / "books.csv"
        members_path = self.data_folder / "members.csv"

        with books_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["book_id", "title", "author", "available"]
            )
            writer.writeheader()
            writer.writerows(book.to_dict() for book in self.books.values())

        with members_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["member_id", "name", "email", "borrowed_books"],
            )
            writer.writeheader()
            writer.writerows(member.to_dict() for member in self.members.values())

    def load_data(self):
        """Load saved books and members when their CSV files exist."""
        books_path = self.data_folder / "books.csv"
        members_path = self.data_folder / "members.csv"

        if books_path.exists():
            with books_path.open("r", newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    book = Book(
                        row["book_id"], row["title"], row["author"],
                        row["available"].lower() == "true",
                    )
                    self.books[book.book_id] = book

        if members_path.exists():
            with members_path.open("r", newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    member = Member.from_dict(row)
                    self.members[member.member_id] = member

    def _get_book(self, book_id):
        """Return a book or raise a clear error."""
        if book_id not in self.books:
            raise ValueError("Book ID was not found.")
        return self.books[book_id]

    def _get_member(self, member_id):
        """Return a member or raise a clear error."""
        if member_id not in self.members:
            raise ValueError("Member ID was not found.")
        return self.members[member_id]
