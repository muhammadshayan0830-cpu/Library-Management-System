# Library Management System

## Purpose
A beginner-friendly, menu-driven Python application for managing a small library catalogue and member borrowing.

## Features
- Add and remove books
- Register members
- View and search the catalogue
- Borrow and return books
- Save and load records using CSV files
- Handle invalid IDs and unavailable books with clear error messages

## Requirements
- Python 3.9 or newer
- No third-party packages are required

## Run
1. Download or clone this repository.
2. Open a terminal in the `library_management_system` folder.
3. Run: `python main.py` (Windows may use `py main.py`).

## First use
Choose option 1 to add a book and option 2 to register a member. Use the IDs you created to borrow or return books. Choose option 8 to save and exit.

## Files
- `main.py`: menu and user interaction
- `models.py`: Book and Member classes
- `library.py`: Library and Librarian classes
- `data/`: CSV files created automatically when the program saves data

## Data
The program creates `data/books.csv` and `data/members.csv` when option 8 is selected. Keep these files with the project to retain saved records.
