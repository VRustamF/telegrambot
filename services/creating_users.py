from dataclasses import dataclass

USERS = {}

@dataclass
class User:
    total_games: int = 0
    wins: int = 0

async def add_user(user_id: int | str) -> None:
    USERS[user_id] = User()