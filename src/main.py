from settings import settings

command_prefix = settings["command_prefix"]

initial_word = settings["initial_word"]
used_words = [initial_word]


while True:

    last_word = used_words[-1]
    last_letter = last_word[-1]

    print(f"`{last_word}` was the previously used word.")
    print(f"Your word should start with `{last_letter}`.")

    user_input = input(":: ").strip().lower()

    if user_input.startswith(command_prefix):
        command = user_input[user_input.index(command_prefix) + 1:]

        if command == "quit":
            print("Thanks for playing.")

            break

        elif command == "revert":
            if len(used_words) > 1:
                removed_word = used_words.pop()
                print(f"`{removed_word}` has been removed.")
            else:
                print(f"Already at the base word.")

            continue

        continue

    if user_input in used_words:
        print(f"{user_input} has already been used.")
        continue

    if not user_input.startswith(last_letter):
        print(f"`{user_input}` doesn't start with {last_letter}.")
        continue

    used_words.append(user_input)
