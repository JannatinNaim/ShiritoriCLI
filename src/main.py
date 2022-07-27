import random
from settings import settings


command_prefix = settings["command_prefix"]

users = []


class User:
    def __init__(self, name):
        self.name = name
        self.used_words = []
        self.score = 0
        self.is_alive = True

    def add_word(self, word):
        self.used_words.append(word)
        self.score += 1

    def remove_word(self):
        if len(self.used_words):
            self.used_words.pop()
            self.score -= 1


while True:

    print("Who are playing this game?")
    print("Provide comma separated names i.e name, other name, some name.")

    usernames_input = input(":: ").strip().split(', ')

    user_count = len(usernames_input)
    last_user, second_to_last_user = user_count - 1, user_count - 2

    usernames = ""
    for i in range(user_count):
        username = usernames_input[i]

        if i == second_to_last_user:
            usernames += username + " and "

        elif i == last_user:
            usernames += username

        else:
            usernames += username + ", "

    print("Are you sure these people will be playing the game?")
    print("Y/N to continue.")
    print(usernames)

    user_confirmation_input = input(":: ").strip().lower()

    if user_confirmation_input == "y":
        for user in usernames_input:
            users.append(User(user))

        break


initial_word = settings["initial_word"]
used_words = [
    {
        "word": initial_word,
        "author": "base"
    }
]
used_words_ref = []

user_count = len(users)
current_user_index = random.choice(range(user_count))


while True:

    current_user = users[current_user_index]

    if not current_user.is_alive:
        if current_user_index == user_count - 1:
            current_user_index = 0

        else:
            current_user_index += 1

        continue

    last_word = used_words[-1]["word"]
    last_letter = last_word[-1]

    print(f"`{last_word}` was the previously used word.")
    print(f"Your word should start with `{last_letter}`.")

    user_word_input = input(f"[{current_user.name}] :: ").strip().lower()

    if user_word_input.startswith(command_prefix):
        command = user_word_input[user_word_input.index(command_prefix) + 1:]

        if command == "quit":
            print("Thanks for playing.")

            break

        elif command == "revert":
            if len(used_words_ref) > 1:
                if current_user_index == 0:
                    current_user_index = user_count - 1

                else:
                    current_user_index -= 1

                used_words.pop()
                removed_word = used_words_ref.pop()

                previous_user = users[current_user_index]
                previous_user.remove_word()

                print(f"`{removed_word['word']}` has been removed.")

            else:
                print(f"Already at the base word.")

            continue

        elif command == "kill":
            if current_user_index == user_count - 1:
                current_user_index = 0

            else:
                current_user_index += 1

            current_user.is_alive = False

            print(f"{current_user.name} was killed.")

            continue

        continue

    if user_word_input in used_words_ref:
        print(f"{user_word_input} has already been used.")

        continue

    if not user_word_input.startswith(last_letter):
        print(f"`{user_word_input}` doesn't start with {last_letter}.")

        continue

    used_words.append({
        "word": user_word_input,
        "author": current_user.name
    })
    used_words_ref.append(user_word_input)

    current_user.add_word(user_word_input)

    if current_user_index == user_count - 1:
        current_user_index = 0

    else:
        current_user_index += 1

for user in users:
    name = user.name
    score = user.score

    print(f"{name} scored {score} points.")
