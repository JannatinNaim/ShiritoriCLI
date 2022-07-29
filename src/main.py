import random
from settings import settings


class User:
    def __init__(self, name):
        self.id = random.choice(range(1_000_000, 9_999_999))
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


class Users:
    def __init__(self, names=[]):
        self.users = [User(name) for name in names]

        self.current_user_index = random.choice(range(self.user_count))
        self.current_user = self.users[self.current_user_index]

    def add_user(self, name):
        self.users.append(User(name))

    def kill_user(self, user):
        for current_user in self.users:

            if user.id == current_user.id:
                current_user.is_alive = False
                self.rotate_forward()

                break

    def rotate_forward(self):
        if self.current_user_index == self.user_count - 1:
            self.current_user_index = 0

        else:
            self.current_user_index += 1

        self.current_user = self.users[self.current_user_index]

        if not self.current_user.is_alive:
            self.rotate_forward()

    def rotate_backward(self):
        if self.current_user_index == 0:
            self.current_user_index = self.user_count - 1

        else:
            self.current_user_index -= 1

        self.current_user = self.users[self.current_user_index]

        if not self.current_user.is_alive:
            self.rotate_backward()

    @property
    def only_one_alive(self):
        alive_users = 0

        for user in self.users:
            if user.is_alive:
                alive_users += 1

                if alive_users > 1:
                    return False

        return True

    @property
    def user_count(self):
        return len(self.users)

    @property
    def previous_user(self):
        return self.users[-1]


while True:

    print("Who are playing this game?")
    print("Provide comma separated names i.e name, other name, some name.")

    usernames_input = input(":: ").strip().split(', ')

    user_count = len(usernames_input)
    previous_user, second_to_last_user = user_count - 1, user_count - 2

    usernames = ""
    for i in range(user_count):
        username = usernames_input[i]

        if i == second_to_last_user:
            usernames += username + " and "

        elif i == previous_user:
            usernames += username

        else:
            usernames += username + ", "

    print("Are you sure these people will be playing the game?")
    print("Y/N to continue.")
    print(usernames)

    user_confirmation_input = input(":: ").strip().lower()

    if user_confirmation_input == "y":
        users = Users(usernames_input)

        break


class Word:
    def __init__(self, word, user):
        self.word = word
        self.last_letter = word[-1]
        self.user = user


class Words:
    def __init__(self, settings):
        self.used_words = []
        self.used_words_ref = []

        initial_word = settings.initial_word
        self.used_words.append(Word(initial_word, User("base")))
        self.used_words_ref.append(initial_word)

    def add_word(self, word, user):
        created_word = Word(word, user)

        self.used_words.append(created_word)
        self.used_words_ref.append(word)

        user.add_word(created_word)

    def remove_word(self):
        removed_word = self.used_words.pop()
        self.used_words_ref.pop()

        return removed_word

    def is_used(self, word):
        return word in self.used_words_ref

    @property
    def last_word(self):
        return self.used_words[-1]

    @property
    def can_revert(self):
        if len(self.used_words_ref) > 1:
            return True
        else:
            return False


class Command:
    def __init__(self, string, command_prefix):
        self.is_command = string.startswith(command_prefix)

        if self.is_command:
            self.action = string[string.index(command_prefix) + 1:]
        else:
            self.action = None


words = Words(settings)

initial_word = settings.initial_word
used_words = words.used_words
used_words_ref = words.used_words_ref

user_count = users.user_count


while True:
    current_user = users.current_user

    if users.only_one_alive:
        print(f"Congratulations! {current_user.name} has won the game.")
        break

    last_word = words.last_word.word
    last_letter = words.last_word.last_letter

    print(f"`{last_word}` was the previously used word by {words.last_word.user.name}.")
    print(f"Your word should start with `{last_letter}`.")

    user_word_input = input(f"[{current_user.name}] :: ").strip().lower()

    command_prefix = settings.command_prefix
    command = Command(user_word_input, command_prefix)

    if command.is_command:

        if command.action == "quit":
            print("Thanks for playing.")

            break

        elif command.action == "revert":
            if words.can_revert:
                users.rotate_backward()

                removed_word = words.remove_word()

                print(
                    f"`{removed_word.word}` entered by {removed_word.user.name} has been removed."
                )

            else:
                print(f"Already at the base word.")

            continue

        elif command.action == "kill":
            users.kill_user(current_user)

            print(f"{current_user.name} was killed.")

            continue

        continue

    if words.is_used(user_word_input):
        print(f"{user_word_input} has already been used.")

        continue

    if not user_word_input.startswith(last_letter):
        print(f"`{user_word_input}` doesn't start with {last_letter}.")

        continue

    words.add_word(user_word_input, current_user)

    users.rotate_forward()

for user in users.users:
    name = user.name
    score = user.score

    print(f"{name} scored {score} points.")
