# Import library to connect game with database and save results
from __future__ import annotations

import sqlite3
from sqlite3 import Cursor
__all__ = ["get_best", "insert_result", "cursor"]
# Method returns the result of the top 3 players.
def get_best(count: int = 0) -> dict:
    try:
        assert -1 <= count <= 3
    except AssertionError as exc:
        msg = "Invalid argument count, must be no more than 3 and no less than -1"
        raise ValueError(msg) from exc
# creating a table
    cursor.execute(
        """
        SELECT name gamer, max(score) score FROM RECORDS
        GROUP by name
        ORDER by score DESC
        LIMIT 3
    """,
    )
# for request and receipt
    source = cursor.fetchall()
# to write it in format dictionary
    sparse_arr = [source[i] for i in range(len(source)) if len(source) >= 1] + [(None, -1)] * (3 - len(source))
    result: dict[int, dict] = {i: {"name": sparse_arr[i - 1][0], "score": sparse_arr[i - 1][1]} for i in range(1, 4)}
    return result if count == 0 else result[count]

# Inserts new data into the SQL table, saving it.
def insert_result(name: str | None, score: int) -> None:
    cursor.execute(
        """
        insert into RECORDS values ( ?, ?)
    """,
        (name, score),
    )
# Saving results
    BD.commit()
BD = sqlite3.connect("2048.sqlite")
cursor: Cursor = BD.cursor()
cursor.execute(
    """
create table if not exists RECORDS (
    name text,
    score integer
)""",
)