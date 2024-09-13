import sqlite3
from config import DATABASE_NAME


def main() -> None:
    """
    create database if doesn't exists
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arrays (
            id INTEGER PRIMARY KEY,
            array_elements VARCHAR(200) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def format_solution_for_db(solution: list[int]) -> str:
    return "".join([str(move) if move >= 10 else "0" + str(move) for move in solution])


def format_solution_from_db(solution: str) -> list[int]:
    return [int("".join(solution[i : i + 2])) for i in range(0, 100, 2)]


def insert_solutions(solutions: list[list[int]]) -> None:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    conn.execute("BEGIN TRANSACTION")

    for solution in solutions:
        formatted_solution = format_solution_for_db(solution)

        cursor.execute(
            """
            INSERT INTO arrays (array_elements)
            VALUES (?)
        """,
            (formatted_solution,),
        )

    conn.execute("COMMIT")
    conn.close()


def get_arrays_by_page(page: int, limit: int = 100):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    start_id = page * limit + 1
    end_id = (page + 1) * limit

    cursor.execute(
        """
        SELECT array_elements
        FROM arrays
        WHERE id BETWEEN ? AND ?
    """,
        (start_id, end_id),
    )

    results = cursor.fetchall()

    conn.close()

    return [row[0] for row in results]


if __name__ == "__main__":
    main()
