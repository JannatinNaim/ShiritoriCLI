from __future__ import annotations
import random
from typing import List
import word as _word


class User:
    def __init__(self, name: str) -> None:
        self.id: int = random.choice(range(1_000_000, 9_999_999))
        self.name: str = name
        self.used_words: List[_word.Word] = []
        self.score: int = 0
        self.is_alive: bool = True

    def add_word(self, word):
        self.used_words.append(word)
        self.score += 1

    def remove_word(self):
        if len(self.used_words):
            self.used_words.pop()
            self.score -= 1


class Users:
    def __init__(self, names: List[str] = []):
        self.users: List[User] = [User(name) for name in names]

        self.current_user_index: int = random.choice(range(self.user_count))
        self.current_user: User = self.users[self.current_user_index]

    def add_user(self, name: str):
        self.users.append(User(name))

    def kill_user(self, user: User) -> User:
        for current_user in self.users:

            if user.id == current_user.id:
                current_user.is_alive = False
                self.rotate_forward()

                return current_user

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
