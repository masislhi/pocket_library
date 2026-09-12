import requests
import inflect
from tabulate import tabulate

def main():
    while True:
        print("\n==============================")
        print("      Pocket Library")
        print("==============================")
        print("1. Search books")
        print("2. My books")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_menu()

        elif choice == "2":
            my_books_menu()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

def search_menu():
    while True:
        print("\n==============================")
        print("          SEARCH BOOKS")
        print("==============================")
        print("1. Search by title")
        print("2. Search by author")
        print("0. Back")

        choice = input("Choose: ")

        if choice == "0":
            return

        elif choice == "1":
            search_results("title")

        elif choice == "2":
            search_results("author")

        else:
            print("Invalid choice.")

def search_results(parameter):
    query = input("Search: ")
    page = 1

    while True:
        data = search_books(parameter, query, 10, page)
        if data is None:
            return
        books = create_books(extract_book_data(data))

        if not books:
            if page == 1:
                print("No book found")
                continue
            else:
                print("No more books found.")
                page -= 1
                continue

        show_books(books, (page - 1) * 10 + 1)

        print("\nA. Add to list")
        
        if page > 1:
            print("B. Previous page")

        print("N. Next page")
        print("E. Exit")

        choice = input("Choose: ").lower()

        if choice == "a":
            add_book(books)
            continue

        if choice == "n":
            page += 1

        elif choice == "b" and page > 1:
            page -= 1

        elif choice == "e":
            return

        else:
            print("Invalid choice.")

def show_books(books, start):
    table = []

    for i, book in enumerate(books, start):
        authors = book.p.join(book.authors)
        year = book.year if book.year else "Unknown"
        title = book.title
        if len(title) > 60:
            title = title[:57] + "..."

        if len(authors) > 40:
            authors = authors[:37] + "..."
        information = f"{title}\n{authors} ({year})"

        table.append([i, information])

    print(tabulate(
        table,
        headers=["#", "Book"],
        tablefmt="simple"
    ))


def add_book(books):
    choice = input("Which book would you like to add? (1-10): ")

    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a number.")
        return

    if choice < 1 or choice > len(books):
        print("Invalid book number.")
        return

    book = books[choice - 1]

    if book.add_list():
        print(f"{book.title} was added to your reading list.")
    else:
        print(f"{book.title} already exists in your reading list.")

def my_books_menu():
    while True:
        books = get_my_books()

        print("\n==============================")
        print("          MY BOOKS")
        print("==============================")

        if not books:
            print("Your reading list is empty.")
        else:
            table = []

            for i, (book, completion) in enumerate(books, 1):
                authors = book.p.join(book.authors)
                information = f"{book.title}\n{authors} ({book.year})\nCompletion: {completion}%"
                table.append([i, information])

            print(tabulate(
                table,
                headers=["#", "Book"],
                tablefmt="simple"
            ))

        print("\nR. Read")
        print("D. Delete")
        print("B. Back")

        choice = input("Choose: ").lower()

        if choice == "r":
            if books:
                read_book(books)
            else:
                print("Your reading list is empty.")

        elif choice == "d":
            if books:
                delete_book(books)
            else:
                print("Your reading list is empty.")

        elif choice == "b":
            return

        else:
            print("Invalid choice.")

def get_my_books():
    FILE = "to_read.csv"
    try:
        with open(FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    books = []

    for line in lines[1:]:
        data = line.strip().split(",")

        title = data[0]
        authors = data[1].split(" and ")
        year = int(data[2])

        if data[3] == "-":
            series = []
            series_position = []
        else:
            series = [data[3]]

            if data[4] == "-":
                series_position = []
            else:
                series_position = [data[4]]

        book = Book(title, authors, year, series, series_position)
        completion = int(data[5])

        books.append((book, completion))

    return books



def read_book(books):
    choice = input("Which book did you read? ")

    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a number.")
        return

    if choice < 1 or choice > len(books):
        print("Invalid book number.")
        return

    book = books[choice - 1][0]

    percent = input("How much did you read? ")

    try:
        percent = int(percent)
    except ValueError:
        print("Please enter a number.")
        return

    if percent < 0:
        print("You cannot read a negative percentage.")
        return

    read(book, percent)

    print(f"Updated {book.title}.")

def delete_book(books):
    choice = input("Which book would you like to delete? ")

    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a number.")
        return

    if choice < 1 or choice > len(books):
        print("Invalid book number.")
        return

    book = books[choice - 1][0]

    confirm = input(f"Delete '{book.title}'? (y/n): ").lower()

    if confirm == "y":
        book.del_list()
        print(f"{book.title} was deleted.")
    else:
        print("Delete cancelled.")

def search_books(p, q, l, page):
    try:
        response = requests.get("https://openlibrary.org/search.json",params={p: q, "limit":l, "page":page})
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print("Could not connect to OpenLibrary.")
    return None

def extract_book_data(data):
    books = []

    for book in data["docs"]:
        books.append({
            "title": book.get("title"),
            "authors": book.get("author_name", []),
            "year": book.get("first_publish_year"),
            "series": book.get("series_name", []),
            "series_position": book.get("series_position", []),
        })

    return books

def create_books(data):
    books = []

    for book in data:
        books.append(
            Book(
                book["title"],
                book["authors"],
                book["year"],
                book["series"],
                book["series_position"]
            )
        )

    return books

def read(book, percent):
    FILE = "to_read.csv"
    if percent < 0:
        raise ValueError("Percent can not be negative")
    authors = book.p.join(book.authors).replace(","," ")
    book_string = f"{str(book.title).replace(",","")},{authors},{book.year}"
    if book.series :
        book_string += f",{book.series[0]}"
        if book.series_position :
            book_string += f",{book.series_position[0]}"
        else:
            book_string += ",-"
    else:
        book_string += ",-,-"

    try :
        with open(FILE, "r", encoding="utf-8") as text:
            lines = text.readlines()
    except FileNotFoundError:
        raise ValueError(f"{FILE} does not exist")

    found = False


    for i in range(1,len(lines)):
        book_data = lines[i].strip().split(",")
        book_without_completion = ",".join(book_data[:-1])
        if book_string == book_without_completion:
            completion = int(book_data[-1])
            completion += percent
            if completion >= 100:
                completion = 100

            lines[i] = f"{book_string},{completion}\n"
            found = True
            break

    if  not found:
        raise ValueError(f"This book does not exist in {FILE}")

    with open(FILE, "w", encoding="utf-8") as file:

        for line in lines:
            file.write(line)
    

    


class Book:

    p = inflect.engine()
    
    def __init__(self, title, authors, year, series, series_position):
        self.title = title
        self.authors = authors
        self.year = year
        self.series = series
        self.series_position = series_position

    def __str__(self):

        authors = self.p.join(self.authors)
        result = f"Title: {self.title}\nAuthor(s): {authors}\nYear: {self.year}"
        if self.series :
            result += f"\nSeries: {self.series[0]}"
            if self.series_position :
                result += f"\nPosition: {self.series_position[0]}"

        return result

    def add_list(self):
        FILE = "to_read.csv"
        authors = self.p.join(self.authors).replace(","," ")
        book = f"{str(self.title).replace(",","")},{authors},{self.year}"
        if self.series :
            book += f",{self.series[0]}"
            if self.series_position :
                book += f",{self.series_position[0]}"
            else:
                book += ",-"
        else:
            book += ",-,-"

        with open(FILE,"a", encoding="utf-8") as file :
            if file.tell() == 0:
                file.write("title,author(s),year,series,position,completion\n")
                file.write(f"{book},0\n")
                return True
            
        with open(FILE, "r", encoding="utf-8") as text:
            lines = text.readlines()
            for line in lines:
                book_data = line.strip().split(",")
                book_without_completion = ",".join(book_data[:-1])
                if book == book_without_completion:
                    return False

        with open(FILE,"a",encoding="utf-8") as file :
            file.write(f"{book},0\n")
            return True

    def del_list(self):
        FILE = "to_read.csv"
        authors = self.p.join(self.authors).replace(","," ")
        book = f"{str(self.title).replace(",","")},{authors},{self.year}"

        if self.series :
            book += f",{self.series[0]}"
            if self.series_position :
                book += f",{self.series_position[0]}"
            else:
                book += ",-"
        else:
            book += ",-,-"
        try :
            with open(FILE, "r", encoding="utf-8") as text:
                lines = text.readlines()
        except FileNotFoundError:
            raise ValueError(f"{FILE} does not exist")

        found = False


        for line in lines:
            book_data = line.strip().split(",")
            book_without_completion = ",".join(book_data[:-1])
            if book == book_without_completion:
                found = True
                break

        if  not found:
            raise ValueError(f"This book does not exist in {FILE}")

        with open(FILE, "w", encoding="utf-8") as file:
            
            for line in lines:
                book_data = line.strip().split(",")
                book_without_completion = ",".join(book_data[:-1])
                if book_without_completion != book:
                    file.write(line)



if __name__ == "__main__":
    main()


