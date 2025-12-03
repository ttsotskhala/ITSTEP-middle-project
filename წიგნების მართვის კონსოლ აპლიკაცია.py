import json
from datetime import datetime

# ============================
#       VALIDATION
# ============================
def validate_author(name: str):
    name = name.strip()
    if not name:
        return False, "ავტორის ველი არ უნდა იყოს ცარიელი."

    allowed = [" ", "-", "’", "'", "."]
    invalid = next((c for c in name if not (c.isalpha() or c in allowed)), None)
    if invalid:
        return False, "ავტორის ველი არ უნდა შეიცავდეს ციფრებს ან უხარისხო სიმბოლოებს."

    return True, name


def validate_year(year_str: str):
    year_str = year_str.strip()
    if not year_str:
        return False, "წელი არ უნდა იყოს ცარიელი."
    if not year_str.isdigit():
        return False, "წელი უნდა იყოს ნატურალური რიცხვი."

    year = int(year_str)
    current_year = datetime.now().year

    if year > current_year:
        return False, "წიგნის გამოცემის წელი არ შეიძლება მომავალში იყოს."

    return True, year


# ============================
#           BOOK
# ============================
class Book:
    next_id = 1

    def __init__(self, title, author, year):
        self.__id = Book.next_id
        Book.next_id += 1

        self.title = title
        self.author = author
        self.year = year

    # ----- ID (read-only) -----
    @property
    def id(self):
        return self.__id

    # ----- TITLE -----
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        value = value.strip()
        if not value:
            raise ValueError("სათაური არ შეიძლება იყოს ცარიელი.")
        self.__title = value

    # ----- AUTHOR -----
    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        ok, result = validate_author(value)
        if not ok:
            raise ValueError(result)
        self.__author = result

    # ----- YEAR -----
    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        ok, result = validate_year(str(value))
        if not ok:
            raise ValueError(result)
        self.__year = result

    def __str__(self):
        return f"[{self.id}] '{self.title}' — {self.author}, {self.year}"


# ============================
#       BOOK MANAGER
# ============================
class BookManager:
    def __init__(self):
        self.__books = []

    # Add
    def add_book(self, book: Book):
        self.__books.append(book)

    # Show
    def show_books(self):
        if not self.__books:
            print("!!! სია ცარიელია.")
            return
        for i, book in enumerate(self.__books, start=1):
            print(f"{i}. {book}")

    # Sort
    def sort_books(self, key):
        if key == "title":
            self.__books.sort(key=lambda b: b.title.lower())
        elif key == "author":
            self.__books.sort(key=lambda b: b.author.lower())
        elif key == "year":
            self.__books.sort(key=lambda b: b.year)

    # Search
    def search_by_title(self, query):
        query = query.lower()
        return [b for b in self.__books if query in b.title.lower()]

    # Delete
    def delete_book_by_id(self, book_id):
        for b in self.__books:
            if b.id == book_id:
                self.__books.remove(b)
                return True
        return False

    # Save
    def save_to_file(self, filename="books.json"):
        data = [
            {"id": b.id, "title": b.title, "author": b.author, "year": b.year}
            for b in self.__books
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # Load
    def load_from_file(self, filename="books.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.__books = []

            for item in data:
                book = Book(item["title"], item["author"], item["year"])
                # ვაბრუნებთ რეალურ id-ს
                book._Book__id = item["id"]
                self.add_book(book)

            Book.next_id = max((b.id for b in self.__books), default=0) + 1

            print("ფაილი ჩატვირთულია.")
        except FileNotFoundError:
            print("ფაილი არ არსებობს — შეიქმნება ახალი.")


# ============================
#           MAIN
# ============================
def run():
    manager = BookManager()
    manager.load_from_file()

    while True:
        print("\n==== მენიუ ====")
        print("1. ახალი წიგნის დამატება")
        print("2. წიგნების სია")
        print("3. ძიება სათაურით")
        print("4. წაშლა")
        print("5. რედაქტირება")
        print("6. შენახვა")
        print("0. გამოსვლა")

        choice = input("აირჩიეთ: ").strip()

        # ---------- ADD ----------
        if choice == "1":
            title = input("სათაური: ").strip()
            if not title:
                print("სათაური ცარიელია.")
                continue

            author = input("ავტორი: ").strip()
            ok, result = validate_author(author)
            if not ok:
                print("!!!", result)
                continue
            author = result

            year_str = input("წელი: ").strip()
            ok, result = validate_year(year_str)
            if not ok:
                print("!!!", result)
                continue
            year = result

            try:
                manager.add_book(Book(title, author, year))
                print("დამატებულია.")
            except Exception as e:
                print("შეცდომა:", e)

        # ---------- SHOW ----------
        elif choice == "2":
            print("სორტირება: 1-სათაურის მიხედვით 2-ავტორის მიხედვით 3-წლის მიხედვით")
            sc = input("აირჩიეთ ან Enter: ").strip()
            if sc == "1":
                manager.sort_books("title")
            elif sc == "2":
                manager.sort_books("author")
            elif sc == "3":
                manager.sort_books("year")

            manager.show_books()

        # ---------- SEARCH ----------
        elif choice == "3":
            q = input("შეიყვანეთ წიგნის სათაური (ან მისი ნაწილი): ")
            res = manager.search_by_title(q)
            if not res:
                print("ვერ მოიძებნა.")
            else:
                for b in res:
                    print(b)

        # ---------- DELETE ----------
        elif choice == "4":
            q = input("შეიყვანეთ წიგნის სათაური (ან მისი ნაწილი): ").strip()
            res = manager.search_by_title(q)

            if not res:
                print("ასეთი წიგნი არ არის სიაში.")
                continue

            for i, b in enumerate(res, start=1):
                print(f"{i}. {b}")

            sel = input("რომელი წავშალოთ? (Enter — გაუქმება): ").strip()
            if not sel.isdigit():
                print("გაუქმდა.")
                continue

            idx = int(sel) - 1
            if idx < 0 or idx >= len(res):
                print("არასწორი არჩევანი.")
                continue

            book = res[idx]

            confirm = input("წავშალოთ? (დ/ა): ").strip().lower()
            if confirm != "დ":
                print("გაუქმებულია.")
                continue

            if manager.delete_book_by_id(book.id):
                print("წაიშალა.")
            else:
                print("შეცდომა.")

        # ---------- EDIT ----------
        elif choice == "5":
            q = input("ძიება: ").strip()
            res = manager.search_by_title(q)

            if not res:
                print("ვერ მოიძებნა.")
                continue

            for i, b in enumerate(res, start=1):
                print(f"{i}. {b}")

            sel = input("რომელი? (Enter — გაუქმება): ").strip()
            if not sel.isdigit():
                print("გაუქმდა.")
                continue

            idx = int(sel) - 1
            if idx < 0 or idx >= len(res):
                print("არასწორი არჩევანი.")
                continue

            book = res[idx]

            # --- new title ---
            new_title = input("ახალი სათაური (Enter — არ იცვლება): ").strip()
            if new_title:
                try:
                    book.title = new_title
                except Exception as e:
                    print("შეცდომა:", e)
                    continue

            # --- new author ---
            new_author = input("ახალი ავტორი (Enter — არ იცვლება): ").strip()
            if new_author:
                ok, result = validate_author(new_author)
                if not ok:
                    print("!!!", result)
                    continue
                book.author = result

            # --- new year ---
            new_year_str = input("ახალი წელი (Enter — არ იცვლება): ").strip()
            if new_year_str:
                ok, result = validate_year(new_year_str)
                if not ok:
                    print("!!!", result)
                    continue
                book.year = result

            print("განახლებულია.")

        # ---------- SAVE ----------
        elif choice == "6":
            manager.save_to_file()
            print("შენახულია.")

        # ---------- EXIT ----------
        elif choice == "0":
            print("ნახვამდის.")
            break

        else:
            print("არასწორი არჩევანი.")


run()
