base_word = "soup"
used_words = [base_word]


while True:

    last_word = used_words[-1]
    last_letter = last_word[-1]

    print(f"`{last_word}` was the previously used word.")
    print(f"Your word should start with `{last_letter}`.")

    user_input = input(":: ").strip().lower()

    if user_input in used_words:
        print(f"{user_input} has already been used.")
        continue

    if not user_input.startswith(last_letter):
        print(f"`{user_input}` doesn't start with {last_letter}.")
        continue

    used_words.append(user_input)
