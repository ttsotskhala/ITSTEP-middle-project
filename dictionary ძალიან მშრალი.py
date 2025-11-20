import json
import os
import platform

# JSON ლექსიკონის ფაილი
DICTIONARY_FILE = "dictionary.json"

# თარგმნადი ენის წყვილები
LANG_PAIRS = {
    "1": ("ka", "en", "ქართული → ინგლისური"),
    "2": ("ka", "ru", "ქართული → რუსული"),
    "3": ("en", "ka", "English → ქართული"),
    "4": ("ru", "ka", "Русский → ქართული"),
    "5": ("ru", "en", "Русский → Английский"),
    "6": ("en", "ru", "English → Russian")
}

# ----------------------- UTILS -----------------------

def clear_screen():
    """Очищает экран красиво на Windows/macOS/Linux"""
    os.system("cls" if platform.system() == "Windows" else "clear")


def pause():
    input("\nდასაბრუნებლად დააჭირეთ Enter...")

# ----------------------- JSON -----------------------

def create_default_dictionary():
    default_dict = {
        "ka-en": {"კატა": "cat", "ძაღლი": "dog"},
        "ka-ru": {"კატა": "кошка", "ძაღლი": "собака"},
        "en-ka": {"cat": "კატა", "dog": "ძაღლი"},
        "ru-ka": {"кошка": "კატა", "собака": "ძაღლი"},
        "ru-en": {"кошка": "cat", "собака": "dog"},
        "en-ru": {"cat": "кошка", "dog": "собака"}
    }

    with open(DICTIONARY_FILE, "w", encoding="utf-8") as f:
        json.dump(default_dict, f, ensure_ascii=False, indent=4)


def load_dictionary():
    if not os.path.exists(DICTIONARY_FILE):
        print("ლექსიკონი ვერ მოიძებნა, იქმნება ახალი...")
        create_default_dictionary()

    with open(DICTIONARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dictionary(data):
    with open(DICTIONARY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ----------------------- LOGIC -----------------------

def add_bidirectional(dictionary, pair_key, word, translation):
    """Добавляет слово в обе стороны: ka-en и en-ka"""
    dictionary[pair_key][word] = translation

    from_lang, to_lang = pair_key.split("-")
    reverse_key = f"{to_lang}-{from_lang}"

    if reverse_key not in dictionary:
        dictionary[reverse_key] = {}

    dictionary[reverse_key][translation] = word


def translate():
    dictionary = load_dictionary()

    clear_screen()
    print("========== თარგმანი ==========\n")
    print("აირჩიე თარგმნის მიმართულება:")
    for k, v in LANG_PAIRS.items():
        print(f"{k}. {v[2]}")
    print("0. გამოსვლა")
    print("===============================")

    choice = input("\n👉 შენი არჩევანი: ")

    if choice == "0":
        return

    if choice not in LANG_PAIRS:
        print("❗ არასწორი არჩევანი!")
        pause()
        return

    from_lang, to_lang, label = LANG_PAIRS[choice]
    pair_key = f"{from_lang}-{to_lang}"

    if pair_key not in dictionary:
        dictionary[pair_key] = {}

    clear_screen()
    print(f"🔄 არჩეული მიმართულება: {label}")
    print("შეიყვანე სიტყვა (0 - გამოსვლა)\n")

    word = input("👉 სიტყვა: ").strip().lower()

    if word == "0":
        return

    # Если слово уже есть
    if word in dictionary[pair_key]:
        clear_screen()
        print("======== შედეგი ========")
        print(f"➡️ თარგმანი: {dictionary[pair_key][word]}")
        print("========================")
        pause()
        return

    # Если нет — предложение добавить
    print("\n❗ სიტყვა ლექსიკონში ვერ მოიძებნა.")
    add = input("დამატება გსურთ? (y/n, 0 - გამოსვლა): ")

    if add == "0":
        return
    if add.lower() != "y":
        print("დამატება გაუქმდა.")
        pause()
        return

    translation = input("👉 შეიყვანე თარგმანი (0 - გამოსვლა): ").strip().lower()

    if translation == "0":
        return

    add_bidirectional(dictionary, pair_key, word, translation)
    save_dictionary(dictionary)

    print("\n✔ სიტყვა წარმატებით დაემატა ორმხრივად!")
    pause()

# ----------------------- MAIN -----------------------

def main():
    while True:
        clear_screen()
        print("=========== მენიუ ==========")
        print("1. თარგმნა")
        print("0. გამოსვლა")
        print("============================")

        choice = input("👉 აირჩიე: ")

        if choice == "1":
            translate()
        elif choice == "0":
            clear_screen()
            print("პროგრამა დასრულდა. 👋")
            break
        else:
            print("❗ არასწორი არჩევანი!")
            pause()


main()
