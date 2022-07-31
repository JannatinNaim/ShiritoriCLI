import json
import word as _word
import user as _user
from command import Command

users: _user.Users = _user.Users()
words: _word.Words = _word.Words()
with open("./words_dictionary.json", "r", encoding="utf-8") as file:
    dictionary = json.load(file)


def menu():
    print()
    print("What would you like to do?")

    options = [
        ["play", "Play"],
        ["view_scores", "View Scores"],
        ["quit", "Quit"],
    ]

    for index, option in enumerate(options):
        option_number = index + 1

        print(f"{option_number}. {option[1]}")

    user_action_input = int(input(":: ").strip())
    return options[user_action_input - 1][0]


def generate_players():

    print()
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

    print()
    print("Are you sure these people will be playing the game?")
    print("Y/N to continue.")
    print(usernames)

    user_confirmation_input: str = input(":: ").strip().lower()

    if user_confirmation_input == "y":
        return usernames_input


def game():
    while True:
        current_user = users.current_user

        if users.only_one_alive:
            print()
            print(f"Congratulations! {current_user.name} has won the game.")

            break

        last_word = words.last_word.word
        last_letter = words.last_word.last_letter

        print()
        print(
            f"`{last_word}` was the previously used word by {words.last_word.user.name}."
        )
        print(f"Your word should start with `{last_letter}`.")

        user_word_input = input(f"[{current_user.name}] :: ").strip().lower()

        command = Command(user_word_input)

        if command.is_command:

            if command.action == "quit":
                print()
                print("Thanks for playing.")

                break

            elif command.action == "revert":
                if words.can_revert:
                    users.rotate_backward()

                    removed_word = words.remove_word()

                    print()
                    print(
                        f"`{removed_word.word}` by {removed_word.user.name} has been removed."
                    )

                else:
                    print()
                    print("Already at the base word.")

                continue

            elif command.action == "kill":
                users.kill_user(current_user)

                print()
                print(f"{current_user.name} was killed.")

                continue

            continue

        if words.is_used(user_word_input):

            print()
            print(f"{user_word_input} has already been used.")

            continue

        if not user_word_input.startswith(last_letter):
            print()
            print(f"`{user_word_input}` doesn't start with {last_letter}.")

            continue

        if not user_word_input in dictionary:
            print()

            print(f"`{user_word_input}` is not a valid word.")

            continue

        words.add_word(user_word_input, current_user)

        users.rotate_forward()


def view_scores():
    print()
    for user in users.users:
        name = user.name
        score = user.score

        print(f"{name} scored {score} points.")


def output_results():
    with open("./game_data.json", "w", encoding="utf-8") as game_result_file:
        data = {
            "users": [
                {
                    "name": user.name,
                    "words": [
                        word.word
                        for word in user.used_words
                    ],
                    "score": user.score
                }
                for user in users.users
            ]
        }
        json.dump(data, game_result_file)


def main():
    while True:
        user_action = menu()

        if user_action == "play":
            if users.user_count != 0:
                print("Do you want to use previously entered player names? Y / N")
                user_reuse_data_confirmation = input(":: ").strip().lower()

                if user_reuse_data_confirmation == "y":
                    for user in users.users:
                        user.is_alive = True
                else:
                    player_names = generate_players()
                    for player in player_names:
                        users.add_user(player)

            else:
                player_names = generate_players()
                for player in player_names:
                    users.add_user(player)

            game()
            view_scores()
            output_results()

        if user_action == "view_scores":
            view_scores()

        if user_action == "quit":
            break


if __name__ == "__main__":
    main()
