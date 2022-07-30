from __future__ import annotations
from typing import List
from settings import settings
import user as _user


class Word:
    def __init__(self, word: str, user: _user.User) -> None:
        self.word: str = word
        self.last_letter: str = word[-1]
        self.user: _user.User = user


class Words:
    def __init__(self) -> None:
        self.used_words: List[Word] = []
        self.used_words_ref: List[str] = []

        initial_word = settings.initial_word
        self.used_words.append(Word(initial_word, _user.User("base")))
        self.used_words_ref.append(initial_word)

    def add_word(self, word: str, user: _user.User):
        created_word: Word = Word(word, user)

        self.used_words.append(created_word)
        self.used_words_ref.append(word)

        user.add_word(created_word)

    def remove_word(self) -> Word:
        removed_word: Word = self.used_words.pop()
        self.used_words_ref.pop()

        return removed_word

    def is_used(self, word: str) -> bool:
        return word in self.used_words_ref

    @property
    def last_word(self) -> Word:
        return self.used_words[-1]

    @property
    def can_revert(self) -> bool:
        if len(self.used_words_ref) > 1:
            return True
        else:
            return False
