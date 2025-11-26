import json

# ---------------------------
#         Book class
# ---------------------------
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"'{self.title}' — {self.author}, {self.year}"

# ---------------------------
#      BookManager class
# ---------------------------
class BookManager:
    def __init__(self):
        self.books = []

    #1 Add book
    def add_book(self, book):
        self.books.append(book)

    #2 Show all books
    def show_books(self):
        if not self.books:
            print("სიაში წიგნები არ არის.")
            return
        for i, book in enumerate(self.books, start=1):
            print(f"{i}. {book}")
    # 2.1 სორტირება
    def sort_books(self, key):
        if key == "title":
            self.books.sort(key=lambda b: b.title.lower())
        elif key == "author":
            self.books.sort(key=lambda b: b.author.lower())
        elif key == "year":
            self.books.sort(key=lambda b: b.year)

    #3 Search by title (partial match)
    def search_by_title(self, title):
        title = title.lower()
        found = [b for b in self.books if title in b.title.lower()]
        return found

    #4 Delete book
    def delete_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                return True
        return False

    #5 Edit book
    def edit_book(self, old_title, new_title=None, new_author=None, new_year=None):
        for book in self.books:
            if book.title.lower() == old_title.lower():
                if new_title:
                    book.title = new_title
                if new_author:
                    book.author = new_author
                if new_year:
                    book.year = new_year
                return True
        return False

    #6 Save to file
    def save_to_file(self, filename="books.json"):
        data = [{"title": b.title, "author": b.author, "year": b.year} for b in self.books]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"მონაცემები შენახულია {filename} ფაილში.")

    # Load from file
    def load_from_file(self, filename="books.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    self.add_book(Book(item["title"], item["author"], item["year"]))
            print("ფაილიდან ჩატვირთვა წარმატებულია.")
        except FileNotFoundError:
            print("!!! ფაილი არ არსებობს, შეიქმნება ახალი.")

# ---------------------------
#       User interface
# ---------------------------
def run():
    manager = BookManager()
    manager.load_from_file()

    while True:
        print("\n===== წიგნების მართვის სისტემა =====")
        print("1. ახალი წიგნის დამატება")
        print("2. წიგნების სიის ნახვა")
        print("3. ძიება სათაურით")
        print("4. წიგნის წაშლა")
        print("5. წიგნის რედაქტირება")
        print("6. შენახვა ფაილში")
        print("0. გამოსვლა")

        choice = input("აირჩიეთ მოქმედება: ").strip()

        if choice == "1":
            title = input("სათაური: ").strip()

            author = input("ავტორი: ").strip()
            allowed_symbols = [" ", "-", "’", "'", "."]
            if author.isdigit():
                print("!!! ავტორის ველი არ უნდა შეიცავდეს ციფრებს")
                continue
            else:
                valid = True
                for ch in author:
                    if ch.isdigit():             # აკრძალულია რიცხვი
                       valid = False
                       break
                    if not (ch.isalpha() or ch in allowed_symbols):
                       valid = False
                       break

            if not valid:
                print("!!! ავტორის ველი შეიძლება შეიცავდეს მხოლოდ ასოებს, 'დაშორებას', '-', '’', '.'")
            else:
                print("ავტორის სახელი მიღებულია:", author)

            year = input("გამოცემის წელი: ").strip()
            if not year.isdigit():
                print("!!! წელი უნდა იყოს რიცხვი.")
                continue

            manager.add_book(Book(title, author, int(year)))
            print("წიგნი დამატებულია.")

        elif choice == "2":
            if not manager.books:
                print("სიაში წიგნები არ არის.")
                continue

            print("\nსორტირება:")
            print("1. სათაურის მიხედვით")
            print("2. ავტორის მიხედვით")
            print("3. წლის მიხედვით")
            print("Enter — სორტირების გარეშე")
            
            sort_choice = input("აირჩიეთ: ").strip()
            if sort_choice == "1":
                manager.sort_books("title")
            elif sort_choice == "2":
                manager.sort_books("author")
            elif sort_choice == "3":
                manager.sort_books("year")
            
            print("\nწიგნების სია:")
            manager.show_books()

        elif choice == "3":
            title = input("შეიყვანეთ სათაური: ").strip()
            results = manager.search_by_title(title)
            if results:
                print("ნაპოვნი წიგნები:")
                for b in results:
                    print(b)
            else:
                print("!!! ასეთი წიგნი არ მოიძებნა.")

        elif choice == "4":
            title = input("წასაშლელი წიგნის სათაური: ").strip()
            if manager.delete_book(title):
                print("წიგნი წაშლილია.")
            else:
                print("!!! ასეთი წიგნი არ მოიძებნა სიაში.")

        elif choice == "5":
            old = input("შესაცვლელი წიგნის სათაური: ").strip()

            # შესაცვლელი სათაურის შეყვანისას მოწმდება წიგნის არსებობა წიგნთა სიაში
            exists = [b for b in manager.books if b.title.lower() == old.lower()]
            if not exists:
                print("!!! ასეთი წიგნი არ არის სიაში!")
                continue
    
            new_title = input("ახალი სათაური (ან Enter — არ შევცვალოთ): ").strip()
            new_title = new_title if new_title else None

            new_author = input("ახალი ავტორი (ან Enter — არ შევცვალოთ): ").strip()
            allowed_symbols = [" ", "-", "’", "'", "."]

            if new_author:
                valid = True
                for ch in new_author:
                    if ch.isdigit() or not (ch.isalpha() or ch in allowed_symbols):
                        valid = False
                        break

                if not valid:
                    print("!!! ავტორის ველი შეიძლება შეიცავდეს მხოლოდ ასოებს, დაშორებას, '-', '’', '.'")
                    continue
                else:
                    print("ავტორის სახელი მიღებულია:", new_author)

            new_author = new_author if new_author else None

            new_year = input("ახალი წელი (ან Enter — არ შევცვალოთ): ").strip()
            if new_year:
                if not new_year.isdigit():
                    print("!!! წელი უნდა იყოს რიცხვი.")
                    continue
                new_year = int(new_year)
            else:
                new_year = None

            if manager.edit_book(old, new_title, new_author, new_year):
                print("წიგნი განახლებულია.")
            else:
                print("!!! ასეთი წიგნი არ მოიძებნა.")

        elif choice == "6":
            manager.save_to_file()

        elif choice == "0":
            print("თქვენ გამოხვედით სისტემიდან.")
            break

        else:
            print("!!! არასწორი არჩევანი.")

run()
