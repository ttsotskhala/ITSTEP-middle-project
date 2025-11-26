import random
import sys

# --------------------------
# სიტყვების სია კატეგორიებად
# --------------------------
WORD_CATEGORIES = {
    "განათლება": [
        "წიგნი", "ბიბლიოთეკა", "მათემატიკა", "ფიზიკა", "ქიმია","ლიტერატურა", "ისტორია",
        "სკოლა",  "უნივერსიტეტი", "ნიშანი", "შუალედური", "ჩათვლა", "გამოცდა", "მასწავლებელი",
        "მოსწავლე", "ლექტორი", "სტუდენტი"
    ],
    "ცეკვები": [
        "პასადობლი", "სამბა", "ტანგო", "რუმბა", "ვალსი", "ჯაივი", "ფოქსტროტი",
        "რაჭული", "განდაგანა", "ხორუმი", "მთიულური", "კინტოური", "დავლური", "სამაია"
     ],
    "ჯუდო": [
        "ჯუდო", "კოდოკანი", "ნევაზა", "აშივაზა", "რანდორი", "მოგვერდი", 
        "ამოგლეჯილი", "ხაბარელი", "კოკა", "იუკო", "ვაზარი", "იპონი", "შიდო"
    ],
    "ფიგურული სრიალი": [
        "ციგურები", "ნაბიჯები", "სპირალი", "ტრიალი", "კასკადი", "ტოდესი",
        "ტულუპი", "სალხოვი", "რიტბერგერი", "ფლიპი", "ლუცი", "აქსელი"
    ],
    "ფეხბურთი": [
        "მეკარე", "მცველი", "ნახევარმცველი", "თავდამსხმელი", "ვინგერი", "თამაშგარე", 
        "კუთხური", "გოლი", "ავტოგოლი", "პასი", "პენალტი", "ჯარიმა", "დრიბლინგი"        
    ],
    "ტენისი": [
        "აუტი", "ბადე", "ბრეიკი", "ბრეიკ-პოინტი", "ბექჰენდი", "გეიმი", "გეიმბოლი", 
        "მატჩ-პოინტი", "სეტი", "სმეში", "ფორჰენდი", "ჩელენჯი", "ეისი"
    ]
}


# Hangman ASCII სტადია — 7 სტადია
HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ======="""
]

MAX_ERRORS = len(HANGMAN_PICS) - 1  # მაქსიმალური შეცდომების რაოდენობა

# ---------------------------
#     დამხმარე ფუნქციები
# ---------------------------
def choose_category():
    # აძლევს მომხმარებელს კატეგორიის არჩევის უფლებას
    print("\n--- აირჩიეთ კატეგორია ---")
    categories = list(WORD_CATEGORIES.keys())

    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    print("0. დაბრუნება")

    while True:
        choice = input("თქვენი არჩევანი: ").strip()
        if choice == "0":
            return None

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]

        print("არასწორი არჩევანი, სცადეთ თავიდან.")

def choose_word(category):
    # შემთხვევითობის პრინციპით აირჩევს სიტყვას კატეგორიიდან
    return random.choice(WORD_CATEGORIES[category])


def mask_word(word, guessed_letters):
    # აბრუნებს სიტყვას, სადაც ჩანს მხოლოდ გამოცნობილი ასოები, ხოლო უცნობი ჩანს როგორც - "_"
    # (მაგ: "იპონი" + guessed = {'ი'} -> "ი _ _ _ ი")
    displayed = []
    for ch in word:
        if ch.lower() in guessed_letters or not ch.isalpha():
            displayed.append(ch)
        else:
            displayed.append("_")
    return " ".join(displayed)

def valid_input(s):
    # ვალიდაცია: არ იყოს ცარიელი; შედგება ანბანური სიმბოლოებისგან ან შეიცავს unicode სიმბოლოებს.
    s = s.strip()
    return len(s) > 0 and all(ch.isalpha() for ch in s)

# ---------------------------
#    მთავარი თამაშის ციკლი
# ---------------------------
def play_hangman(category):
    word = choose_word(category)
    word_lower = word.lower()
    guessed_letters = set()
    wrong_guesses = 0
    tried_words = set()

    print("\n---- Hangman ----")
    print(f"სიტყვა აირჩევა შემთხვევით. მაქსიმალური შეცდომა: {MAX_ERRORS}\n")

    # თამაშის ციკლი (loop)
    while True:
        print(HANGMAN_PICS[wrong_guesses])
        current_mask = mask_word(word, guessed_letters)
        print("\nსიტყვა:", current_mask)
        print(f"დარჩა {MAX_ERRORS - wrong_guesses} მცდელობა")
        if guessed_letters:
            print("გამოცნობილი ასოები:", " ".join(sorted(guessed_letters)))
        else:
            print("გამოცნობილი ასოები: —")

        # მომხმარებლს შეაქვს ან ასო ან მთელი სიტყვა
        guess = input("\nშეიყვანეთ ასო ან მთელი სიტყვა (0 - გამოსვლა): ").strip()
        if guess == "0":
            print("გაბრუნებთ მთავარ მენიუში...")
            return

        # ვალიდაცია
        if not valid_input(guess):
            print("შენიშვნა: შეიყვანეთ მხოლოდ ასოები (არა ციფრები/სიმბოლოები).")
            continue

        guess = guess.lower()

        # თუ მომხმარებელს შეყავს მთელ სიტყვა
        if len(guess) > 1:
            if guess in tried_words:
                print("ეს სიტყვის ცდა უკვე გაკეთდა.")
                continue

            tried_words.add(guess)
            if guess == word_lower:
                print("\n გამარჯვება! თქვენ სწორად გამოიცანით სიტყვა:", word)
                break
            else:
                wrong_guesses += 1
                print("\nსიტყვა არასწორია.")
                if wrong_guesses >= MAX_ERRORS:
                    print(HANGMAN_PICS[wrong_guesses])
                    print("\nGame over! სიტყვა იყო:", word)
                    break
                continue

        # თუ ეს ერთი ასოა
        letter = guess
        if letter in guessed_letters:
            print("გთხოვთ, არ გაიმეოროთ უკვე გამოცნობილი ასო:", letter)
            continue

        # შემოწმება არის თუ არა სიტყვაში ასო
        if letter in word_lower:
            guessed_letters.add(letter)
            print("ეს ასო არის სიტყვაში.")

            # თუ ყველა ასო მივიღეთ -> მოგება
            all_letters_in_word = {ch for ch in word_lower if ch.isalpha()}
            if all_letters_in_word.issubset(guessed_letters):
                print("\nთქვენ გამოიცანით მთელი სიტყვა:", word)
                break
        else:
            wrong_guesses += 1
            print("ეს ასობგერა არ არის სიტყვაში.")
            if wrong_guesses >= MAX_ERRORS:
                print(HANGMAN_PICS[wrong_guesses])
                print("\nGame over! გამოსაცნობი სიტყვა იყო:", word)
                break

    print("\n---- თამაში დასრულდა ----\n")

# ---------------------------
#       მთავარი მენიუ
# ---------------------------
def main():
    print("===== Hangman (ქართულად) ======")
    while True:
        print("\nმთავარი მენიუ:")
        print("1 - დაწყება")
        print("0 - გასვლა")

        choice = input("აირჩიეთ: ").strip()

        if choice == "0":
            print("ნახვამდის!")
            sys.exit(0)

        elif choice == "1":
            category = choose_category()
            if category is None:
                continue

            play_hangman(category)

            again = input("გსურთ კიდევ თამაში? (y/n): ").strip().lower()
            if again != "y":
                print("მადლობა თამაშისთვის. ნახვამდის!")
                sys.exit(0)

        else:
            print("არასწორი არჩევანი, სცადეთ თავიდან.")

main()
