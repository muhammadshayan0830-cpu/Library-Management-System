"""Run the menu-driven Library Management System."""
from library import Library, Librarian
from models import Book, Member


def show_menu():
    """Display available actions."""
    print("\n--- LIBRARY MANAGEMENT SYSTEM ---")
    print("1. Add a book")
    print("2. Register a member")
    print("3. View all books")
    print("4. Search books")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. Remove a book")
    print("8. Save and exit")


def main():
    """Start the application and process menu choices."""
    library = Library()
    library.load_data()
    librarian = Librarian("Library Administrator")

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        try:
            if choice == "1":
                book = Book(
                    input("Book ID: ").strip(),
                    input("Title: ").strip(),
                    input("Author: ").strip(),
                )
                librarian.add_book(library, book)
                print("Book added successfully.")

            elif choice == "2":
                member = Member(
                    input("Member ID: ").strip(),
                    input("Full name: ").strip(),
                    input("Email: ").strip(),
                )
                librarian.register_member(library, member)
                print("Member registered successfully.")

            elif choice == "3":
                for book in librarian.show_catalogue(library):
                    status = "Available" if book.is_available() else "Borrowed"
                    print(f"{book.book_id}: {book.title} by {book.author} - {status}")
                if not library.books:
                    print("The catalogue is empty.")

            elif choice == "4":
                term = input("Enter title or author to search: ").strip()
                results = library.search_books(term)
                for book in results:
                    print(f"{book.book_id}: {book.title} by {book.author}")
                if not results:
                    print("No matching books were found.")

            elif choice == "5":
                book_id = input("Book ID: ").strip()
                member_id = input("Member ID: ").strip()
                library.borrow_book(book_id, member_id)
                print("Book borrowed successfully.")

            elif choice == "6":
                book_id = input("Book ID: ").strip()
                member_id = input("Member ID: ").strip()
                library.return_book(book_id, member_id)
                print("Book returned successfully.")

            elif choice == "7":
                book_id = input("Book ID to remove: ").strip()
                librarian.remove_book(library, book_id)
                print("Book removed successfully.")

            elif choice == "8":
                library.save_data()
                print("Data saved. Goodbye.")
                break

            else:
                print("Please enter a number from 1 to 8.")

        except (ValueError, OSError, KeyError) as error:
            print(f"Could not complete the action: {error}")


if __name__ == "__main__":
    main()
