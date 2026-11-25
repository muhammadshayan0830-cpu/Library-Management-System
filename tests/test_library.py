"""Basic tests for core library operations."""
import tempfile
import unittest

from library import Library
from models import Book, Member


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.library = Library(self.temp_dir.name)
        self.library.add_book(Book("B1", "Python Basics", "A. Writer"))
        self.library.register_member(Member("M1", "Sam Reader", "sam@example.com"))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_borrow_and_return(self):
        self.library.borrow_book("B1", "M1")
        self.assertFalse(self.library.books["B1"].is_available())
        self.library.return_book("B1", "M1")
        self.assertTrue(self.library.books["B1"].is_available())

    def test_duplicate_book_is_rejected(self):
        with self.assertRaises(ValueError):
            self.library.add_book(Book("B1", "Another title", "Another author"))

    def test_unknown_member_is_rejected(self):
        with self.assertRaises(ValueError):
            self.library.borrow_book("B1", "MISSING")

    def test_save_and_load(self):
        self.library.save_data()
        other = Library(self.temp_dir.name)
        other.load_data()
        self.assertIn("B1", other.books)
        self.assertIn("M1", other.members)


if __name__ == "__main__":
    unittest.main()
