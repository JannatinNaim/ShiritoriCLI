import json
import word as _word
import user as _user
from command import Command

users: _user.Users = _user.Users()
words: _word.Words = _word.Words()
with open("./words_dictionary.json", "r", encoding="utf-8") as file:
    dictionary = json.load(file)


while True:

    print("Who are playing this game?")
    print("Provide comma separated names i.e name, other name, some name.")

    usernames_input: str = input(":: ").strip().split(', ')

    user_count: int = len(usernames_input)
    previous_user: int = user_count - 1
    second_to_last_user: int = user_count - 2

    usernames: str = ""
    for i in range(user_count):
        username: str = usernames_input[i]

        if i == second_to_last_user:
            usernames += username + " and "

        elif i == previous_user:
            usernames += username

        else:
            usernames += username + ", "

    print("Are you sure these people will be playing the game?")
    print("Y/N to continue.")
    print(usernames)

    user_confirmation_input: str = input(":: ").strip().lower()

    if user_confirmation_input == "y":
        for user in usernames_input:
            users.add_user(user)

        break


while True:
    current_user = users.current_user

    if users.only_one_alive:
        print(f"Congratulations! {current_user.name} has won the game.")
        break

    last_word = words.last_word.word
    last_letter = words.last_word.last_letter

    print(
        f"`{last_word}` was the previously used word by {words.last_word.user.name}."
    )
    print(f"Your word should start with `{last_letter}`.")

    user_word_input = input(f"[{current_user.name}] :: ").strip().lower()

    command = Command(user_word_input)

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
                print("Already at the base word.")

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

    if not user_word_input in dictionary:
        print(f"`{user_word_input}` is not a valid word.")

        continue

    words.add_word(user_word_input, current_user)

    users.rotate_forward()


for user in users.users:
    name = user.name
    score = user.score

    print(f"{name} scored {score} points.")
