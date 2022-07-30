from word import Words
from user import Users
from command import Command
from settings import settings


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
