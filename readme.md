Project Title: Pocket Library

Project Url: https://drive.google.com/file/d/1rbDoLNKYzEa33zpYHo6w4pTqjg2wFXJr/view?usp=sharing

Project Description:

Pocket Library is a command-line personal library application written in Python. It allows users to search for books using the Open Library API, add books to a personal reading list, track reading progress, and remove books from their library.

I created this project because I wanted a simple way to keep track of books I want to read without having to manually enter all of the information about each book. Instead, the program retrieves book information from the Open Library API and lets the user save the books they are interested in.

Pocket Library provides three main options from the main menu:
Search books
My books
Exit

#Search books:

Users can search for books either by title or by author.
The program sends the search request to the Open Library Search API and retrieves up to 10 results at a time. The results are displayed in a table containing the book number, title, author(s), and publication year.
The search results are paginated, so users can move to the next or previous page when there are more results.
A user can select a book from the results and add it to their personal reading list.

#My books:

The My Books section displays all books that have been saved to the user's reading list.

For each book, the program displays:
Title
Author(s)
Publication year
Series information, when available
Reading completion percentage

From this menu, users can:
Update their reading progress
Delete a book from their reading list
Return to the main menu

##Reading progress:

Each book starts with a completion percentage of 0%.
When the user reads more of a book, they can enter the additional percentage they have read. The program updates the stored completion percentage and prevents it from exceeding 100%.

##Duplicate prevention:

Before adding a book, the program checks whether the same book is already in the reading list.
If it already exists, the user is informed that the book is already in their library instead of creating a duplicate entry.

#Open Library API:

Pocket Library uses the Open Library Search API to obtain book information.
The program sends a request to: https://openlibrary.org/search.json

The API provides information such as:
Book title
Author(s)
First publication year
Series name
Series position

The requests library is used to communicate with the API.
The API response is returned as JSON, which is then processed by the program to extract only the information needed by Pocket Library.
If the API cannot be reached, the program catches the request error and displays an appropriate message instead of crashing.

#Data Storage:

The user's reading list is stored locally in a CSV file called to_read.csv.
The file contains the following information:

title,author(s),year,series,position,completion

The CSV file allows the user's library and reading progress to persist after the program is closed.
When Pocket Library starts, it reads the saved books from the CSV file and converts them back into Book objects.
If the CSV file does not exist yet, the program treats the reading list as empty and creates the file when the first book is added.

#Design:

One of the main design decisions in this project was using a Book class rather than storing every book as separate variables. This allows all of the information belonging to a book to be grouped together and makes it easier to perform operations such as adding, deleting, and updating books.

I also separated the API-related functionality into different functions. search_books() handles communication with Open Library, extract_book_data() extracts the required information, and create_books() converts that information into Book objects. This keeps the different parts of the application organized.

For persistent storage, I chose a CSV file instead of a database because the application only needs to store a relatively small amount of information. This keeps the project simple while still allowing the user's reading list and progress to persist between program executions.