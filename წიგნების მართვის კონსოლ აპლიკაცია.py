import json
from datetime import datetime

# ---------------------------
#         Book class
# ---------------------------
class Book:
    next_id = 1

    def __init__(self, title, author, year, id=None):
        # თუ JSON-დან მოვიდა ID — გამოვიყენოთ
        if id is not None:
            self.id = id

            # next_id უნდა განახლდეს, რომ ID სწორად გაგრძელდეს
            if id >= Book.next_id:
                Book.next_id = id + 1
        else:
            # თუ ეს ახალი წიგნია — მივანიჭოთ ახალი ID
            self.id = Book.next_id
            Book.next_id += 1

        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"'{self.title}' — {self.author}, {self.year}"

# ---------------------------
#       Book Manager
# ---------------------------
class BookManager:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def show_books(self):
        if not self.books:
            print("!!! სიაში წიგნები არ არის.")
            return

        for i, book in enumerate(self.books, start=1):
            print(f"{i}. {book}")

    def sort_books(self, key):
        if key == "title":
            self.books.sort(key=lambda b: b.title.lower())
        elif key == "author":
            self.books.sort(key=lambda b: b.author.lower())
        elif key == "year":
            self.books.sort(key=lambda b: b.year)

    def search_by_title(self, title):
        title = title.lower()
        found = [b for b in self.books if title in b.title.lower()]
        return found

    def delete_book_by_id(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                return True
        return False

    def save_to_file(self, filename="books.json"):
        data = [
            {"id": b.id, "title": b.title, "author": b.author, "year": b.year}
            for b in self.books
        ]

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename="books.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.books = []  # ძველი მონაცემების გაასუფთავება

            for item in data:
                self.add_book(Book(
                    item["title"],
                    item["author"],
                    item["year"],
                    item.get("id")
                ))

            print("ფაილიდან ჩატვირთვა წარმატებულია.")

        except FileNotFoundError:
            print("!!! ფაილი არ არსებობს, შეიქმნება ახალი.")

# ---------------------------
#           VALIDATION
# ---------------------------
from datetime import datetime

def validate_author(name: str):
    #ამოწმებს ავტორის ველის სისწორეს. აბრუნებს: (True, cleaned_name) ან (False, error_message)    
    name = name.strip()
    if not name:
        return False, "ავტორის ველი არ უნდა იყოს ცარიელი."

    allowed = [" ", "-", "’", "'", "."]

    invalid_char = next((ch for ch in name if not (ch.isalpha() or ch in allowed)), None)
    if invalid_char:
        return False, f"ავტორის ველი არასწორია (არ უნდა შეიცავდეს ციფრებს)."

    return True, name


def validate_year(year_str: str):
    # ამოწმებს წლის ველის სისწორეს. აბრუნებს: (True, year_int) ან (False, error_message)
    year_str = year_str.strip()

    if not year_str:
        return False, "წელი არ უნდა იყოს ცარიელი."

    if not year_str.isdigit():
        return False, "წელი უნდა იყოს ნატურალური რიცხვი."

    year = int(year_str)

    current_year = datetime.now().year
    if year > current_year:
        return False, "წიგნის გამოცემის წელი არ შეიძლება იყოს მომავალში."
    return True, year

# ---------------------------
#           MAIN
# ---------------------------
def run():
    manager = BookManager()
    manager.load_from_file()

    while True:
        print("\n==== მენიუ ====")
        print("1. ახალი წიგნის დამატება")
        print("2. წიგნთა სიის ნახვა")
        print("3. ძიება სათაურით")
        print("4. წიგნის წაშლა")
        print("5. წიგნის რედაქტირება")
        print("6. ფაილში შენახვა")
        print("0. გამოსვლა")

        choice = input("აირჩიეთ: ").strip()

        # ---------------------- ADD ----------------------
        if choice == "1":
            title = input("სათაური: ").strip()
            if not title:
                print("!!! სათაური არ შეიძლება იყოს ცარიელი.")
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

            manager.add_book(Book(title, author, year))
            print("წიგნი დამატებულია.")

        # ---------------------- SHOW ----------------------
        elif choice == "2":
            print("სორტირება: 1. სათაურით  2. ავტორით  3. წლით")
            sort_choice = input("აირჩიეთ ან Enter: ").strip()

            if sort_choice == "1":
                manager.sort_books("title")
            elif sort_choice == "2":
                manager.sort_books("author")
            elif sort_choice == "3":
                manager.sort_books("year")

            manager.show_books()

        # ---------------------- SEARCH ----------------------
        elif choice == "3":
            title = input("შეიყვანეთ წიგნის სათაური ან მისი ნაწილი: ")
            results = manager.search_by_title(title)

            if not results:
                print("არაფერი მოიძებნა.")
            else:
                print("\nნაპოვნია:")
                for b in results:
                    print(b)

        # ---------------------- DELETE ----------------------
        elif choice == "4":
            title = input("შეიყვანეთ წიგნის სათაური ან მისი ნაწილი: ")
            results = manager.search_by_title(title)

            if not results:
                print("!!! ასეთი წიგნი არ არის სიაში.")
                continue

            # ერთზე მეტი ძიების შედეგის ჩვენება (დანომრვით)
            print("\nნავოპნი წიგნები:")
            for i, b in enumerate(results, start=1):
                print(f"{i}. {b}")
            #მომხმარებელი ირჩევს, რომლის წაშლა სსურს
            sel = input("მიუთითეთეთ წასაშლელი წიგნის ნომერი ან Enter — გაუქმება: ")
            if not sel.isdigit():
                print("წიგნის წაშლა გაუქმდა.")
                continue

            idx = int(sel) - 1
            if idx < 0 or idx >= len(results):
                print("არასწორი არჩევანი.")
                continue

            book_to_delete = results[idx]
            confirm = input(f"ნამდვილად წავშალოთ წიგნი? (დ/ა): ").strip().lower()
            if confirm != "დ":
                print("წაშლა გაუქმებულია.")
                continue

            if manager.delete_book_by_id(book_to_delete.id):
                print("წიგნი წაიშალა.")
            else:
                print("შეცდომა წაშლისას.")

        # ---------------------- EDIT ----------------------
        elif choice == "5":
            old = input("შეიყვანეთ წიგნის სათაური ან მისი ნაწილი: ").strip()
            results = manager.search_by_title(old)

            if not results:
                print("ასეთი წიგნი არ არის სიაში.")
                continue

            # თუ ნაპოვნია ერთზე მეტი წიგნი
            if len(results) >= 1:
                print("\nნაპოვნი წიგნი/წიგნები:")
                for i, b in enumerate(results, start=1):
                    print(f"{i}. {b}")

                sel = input("მიუთითეთ წიგნის ნომერი, რომლის რედაქტირებაც გსურთ ან Enter — გაუქმება: ").strip()
                if not sel.isdigit():
                    print("გაუქმდა.")
                    continue

                idx = int(sel) - 1
                if idx < 0 or idx >= len(results):
                    print("არასწორი არჩევანი.")
                    continue

                book = results[idx]
            else:
                book = results[0]

            # New values
            new_title = input("ახალი სათაური (Enter — არ შევცვალოთ): ").strip() or None

            new_author = input("ახალი ავტორი (Enter — არ შევცვალოთ): ").strip()
            if new_author == "":
                new_author = None
            else:
                ok, result = validate_author(new_author)
                if not ok:
                    print("!!!", result)
                    continue
                new_author = result
            
            new_year_str = input("ახალი წელი (Enter — არ შევცვალოთ): ").strip()         
            if new_year_str == "":
                new_year = None   # მომხმარებელი არ ცვლის წელს
            else:
                ok, result = validate_year(new_year_str)
                if not ok:
                    print("!!!", result)
                    continue   # უბრუნდება მენიუს
                new_year = result
            
            confirm = input("გნებავთ ცვლილებების შენახვა? (დ/ა): ").strip().lower()
            if confirm != "დ":
                print("რედაქტირება გაუქმებულია.")
                continue

            # Apply changes
            if new_title:
                book.title = new_title
            if new_author:
                book.author = new_author
            if new_year is not None:
                book.year = new_year

            print("წიგნი განახლებულია.")

        # ---------------------- SAVE ----------------------
        elif choice == "6":
            manager.save_to_file()
            print("შენახულია.")

        # ---------------------- EXIT ----------------------
        elif choice == "0":
            print("ნახვამდის.")
            break

        else:
            print("არასწორი არჩევანი.")

run()

